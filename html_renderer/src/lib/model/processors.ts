import { maxBy } from "../utils";
import type Frame from "./Frame";
import { SELF_TIME_FRAME_IDENTIFIER } from "./Frame";
import FrameGroup from "./FrameGroup";
import { combineFrames, deleteFrameFromTree } from './frameOps'

export interface ProcessorOptions {
    filterThreshold?: number // used by remove_irrelevant_nodes
    hideRegex?: string // used by group_library_frames_processor
    showRegex?: string // used by group_library_frames_processor
}
export type ProcessorFunction = (frame: Frame | null, options: ProcessorOptions) => Frame | null

export interface Processor {
    name: string
    description: string
    function: ProcessorFunction
    optionsSpec: {
        key: string,
        name: string,
        value: {
            type: 'string',
            default: string
        } | {
            type: 'number',
            default: number
            min?: number
            max?: number
            sliderMin?: number
            sliderMax?: number
            sliderLogarithmic?: boolean
        } | {
            type: 'boolean',
            default: boolean
        }
    }[],
    category: 'normal' | 'advanced'
}

export const allProcessors: Processor[] = []

/**
 * Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
 */
export function remove_importlib(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null
    }

    for (const child of frame.children) {
        remove_importlib(child, options)

        if (child.filePath && child.filePath.includes("<frozen importlib._bootstrap")) {
            deleteFrameFromTree(child, { replaceWith: "children" })
        }
    }

    return frame
}
allProcessors.push({
    name: "remove_importlib",
    description: "Removes <frozen importlib._bootstrap frames that clutter the output.",
    function: remove_importlib,
    optionsSpec: [],
    category: 'normal',
})

/**
 * Removes frames that have set a local `__traceback_hide__` (e.g.
 * `__traceback_hide__ = True`), to remove them from the output.
 */
export function remove_tracebackhide(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null
    }

    for (const child of frame.children) {
        remove_tracebackhide(child, options)

        if (child.hasTracebackHide) {
            deleteFrameFromTree(child, { replaceWith: "children" })
        }
    }

    return frame
}
allProcessors.push({
    name: "remove_tracebackhide",
    description: "Removes frames that have set a local __traceback_hide__ (e.g. __traceback_hide__ = True), to remove them from the output.",
    function: remove_tracebackhide,
    optionsSpec: [],
    category: 'advanced',
})

/**
 * Converts a timeline into a time-aggregate summary.
 *
 * Adds together calls along the same call stack, so that repeated calls
 * appear as the same frame. Removes time-linearity - frames are sorted
 * according to total time spent.
 *
 * Useful for outputs that display a summary of execution (e.g., text and HTML
 * outputs).
 */
export function aggregate_repeated_calls(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null;
    }

    const childrenByIdentifier: Record<string, Frame> = {};

    for (const child of frame.children.slice()) {
        if (childrenByIdentifier[child.identifier]) {
            const aggregateFrame = childrenByIdentifier[child.identifier];
            combineFrames(child, aggregateFrame);
        } else {
            childrenByIdentifier[child.identifier] = child;
        }
    }

    frame.children.forEach(child => aggregate_repeated_calls(child, options));
    frame._children.sort((a, b) => b.time - a.time);

    return frame;
}
allProcessors.push({
    name: "aggregate_repeated_calls",
    description: "Converts a timeline into a time-aggregate summary. Adds together calls along the same call stack, so that repeated calls appear as the same frame. Removes time-linearity - frames are sorted according to total time spent.",
    function: aggregate_repeated_calls,
    optionsSpec: [],
    category: 'normal',
})

/**
 * Groups frames that should be hidden into FrameGroup objects,
 * according to `remove_regex` and `show_regex` in the options dictionary.
 */
export function group_library_frames_processor(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null;
    }

    const hideRegex = options.hideRegex;
    const showRegex = options.showRegex;

    function shouldHide(frame: Frame): boolean {
        const filePath = frame.filePath || "";
        const show = showRegex && new RegExp(showRegex).test(filePath);
        const hide = hideRegex && new RegExp(hideRegex).test(filePath);

        if (show) {
            return false;
        }
        if (hide) {
            return true;
        }
        return !frame.isApplicationCode
    }

    function addFramesToGroup(frame: Frame, group: FrameGroup): void {
        group.addFrame(frame);
        frame.children.forEach(child => {
            if (shouldHide(child)) {
                addFramesToGroup(child, group);
            }
        });
    }

    frame.children.forEach(child => {
        if (!child.group && shouldHide(child) && child.children.some(shouldHide)) {
            const group = new FrameGroup(child);
            addFramesToGroup(child, group);
        }

        group_library_frames_processor(child, options);
    });

    return frame;
}
allProcessors.push({
    name: "Group library frames",
    description: "Groups frames that should be hidden.",
    function: group_library_frames_processor,
    optionsSpec: [
        {
            key: "hideRegex",
            name: "Hide regex",
            value: {
                type: "string",
                default: ""
            }
        },
        {
            key: "showRegex",
            name: "Show regex",
            value: {
                type: "string",
                default: ""
            }
        }
    ],
    category: 'normal',
})

/**
 * Combines consecutive 'self time' frames.
 */
export function merge_consecutive_self_time(frame: Frame | null, options: ProcessorOptions, recursive: boolean = true): Frame | null {
    if (!frame) {
        return null;
    }

    let previousSelfTimeFrame: Frame | null = null;

    for (const child of frame.children) {
        if (child.identifier === SELF_TIME_FRAME_IDENTIFIER) {
            if (previousSelfTimeFrame) {
                previousSelfTimeFrame.time += child.time;
                child.removeFromParent();
            } else {
                previousSelfTimeFrame = child;
            }
        } else {
            previousSelfTimeFrame = null;
        }
    }

    if (recursive) {
        frame.children.forEach(child => merge_consecutive_self_time(child, options, true));
    }

    return frame;
}
allProcessors.push({
    name: "Merge consecutive self time",
    description: "Combines consecutive 'self time' frames.",
    function: merge_consecutive_self_time,
    optionsSpec: [],
    category: 'advanced',
})

/**
 * Removes unnecessary self-time nodes.
 */
export function remove_unnecessary_self_time_nodes(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null;
    }

    if (frame.children.length === 1 && frame.children[0].identifier === SELF_TIME_FRAME_IDENTIFIER) {
        deleteFrameFromTree(frame.children[0], { replaceWith: "nothing" });
    }

    frame.children.forEach(child => remove_unnecessary_self_time_nodes(child, options));

    return frame;
}
allProcessors.push({
    name: "Remove unnecessary self time nodes",
    description: "Removes unnecessary self-time nodes.",
    function: remove_unnecessary_self_time_nodes,
    optionsSpec: [],
    category: 'advanced',
})

/**
 * Removes nodes that represent less than a certain percentage of the output.
 */
export function remove_irrelevant_nodes(frame: Frame | null, options: ProcessorOptions, totalTime: number | null = null): Frame | null {
    if (!frame) {
        return null;
    }

    if (totalTime === null) {
        totalTime = frame.time;
        if (totalTime <= 0) {
            totalTime = 1e-44;  // Prevent divide by zero
        }
    }

    const filterThreshold = options.filterThreshold ?? 0.01;

    for (const child of frame.children.slice()) {
        const proportionOfTotal = child.time / totalTime;
        if (proportionOfTotal < filterThreshold) {
            deleteFrameFromTree(child, { replaceWith: "nothing" });
        }
    }

    frame.children.forEach(child => remove_irrelevant_nodes(child, options, totalTime));

    return frame;
}
allProcessors.push({
    name: "Remove irrelevant nodes",
    description: "Removes nodes that represent less than a certain percentage of the output.",
    function: remove_irrelevant_nodes,
    optionsSpec: [
        {
            key: "filterThreshold",
            name: "Filter threshold",
            value: {
                type: "number",
                default: 0.01,
                min: 0,
                max: 1,
                sliderMin: 0.0001,
                sliderMax: 1
            }
        }
    ],
    category: 'normal',
})

/**
 * Removes the initial frames specific to the command line use of pyinstrument.
 */
export function remove_first_pyinstrument_frames_processor(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null;
    }

    const longestFrame = (frames: readonly Frame[]) => maxBy(frames, f => f.time)

    const isInitialPyinstrumentFrame = (f: Frame) =>
        f.filePath?.includes("pyinstrument/__main__.py") && f.children.length > 0;

    const isExecFrame = (f: Frame) =>
        f.proportionOfParent > 0.8 && f.filePath?.includes("<string>") && f.children.length > 0;

    const isRunpyFrame = (f: Frame) =>
        f.proportionOfParent > 0.8 && (new RegExp(".*runpy.py").test(f.filePath ?? '') || f.filePath?.includes("<frozen runpy>")) && f.children.length > 0;

    let result = frame;

    if (!isInitialPyinstrumentFrame(result)) return frame;

    result = longestFrame(result.children)!

    if (!isExecFrame(result)) return frame;

    result = longestFrame(result.children)!

    if (!isRunpyFrame(result)) return frame;

    while (isRunpyFrame(result)) {
        result = longestFrame(result.children)!
    }

    result.removeFromParent();

    return result;
}

export function remove_useless_groups_processor(frame: Frame | null, options: ProcessorOptions): Frame | null {
    if (!frame) {
        return null;
    }

    frame.children.forEach(child => remove_useless_groups_processor(child, options));

    // a group with only two frames is meaningless, you still print the root
    // frame, so you're just collapsing the single child frame with a group,
    // which is better printed as just a single frame
    if (frame.group && frame.group.frames.length < 3) {
        frame.group.removeFrame(frame);
    }

    return frame;
}

allProcessors.push({
    name: "Remove first pyinstrument frames",
    description: "Removes the initial frames specific to the command line use of pyinstrument.",
    function: remove_first_pyinstrument_frames_processor,
    optionsSpec: [],
    category: 'advanced',
})
