import { UnreachableCaseError } from "../utils";
import Frame from "./Frame";
import { SELF_TIME_FRAME_IDENTIFIER } from "./Frame";

export function deleteFrameFromTree(frame: Frame, options: {replaceWith: 'children'|'self_time'|'nothing'}) {
    const {replaceWith} = options
    const parent = frame.parent
    if (!parent) {
        throw new Error('Cannot delete the root frame')
    }

    if (replaceWith == 'children') {
        parent.addChildren(frame.children, {after: frame})
    } else if (replaceWith == 'self_time') {
        parent.addChild(
            new Frame({
                identifier: SELF_TIME_FRAME_IDENTIFIER,
                time: frame.time,
            }, parent.context),
            {after: frame}
        )
    } else if (replaceWith == 'nothing') {
        parent.absorbedTime += frame.time
    } else {
        throw new UnreachableCaseError(replaceWith)
    }

    frame.removeFromParent()
    removeFrameFromGroups(frame, true)
}

/**
 * Combines the children of `frame` that share an identifier into the first of
 * them, removing the others from the tree.
 */
export function combineRepeatedChildren(frame: Frame): void {
    const firstByIdentifier = new Map<string, Frame>();
    const repeats: Frame[] = [];

    for (const child of frame.children.slice()) {
        const into = firstByIdentifier.get(child.identifier);
        if (!into) {
            firstByIdentifier.set(child.identifier, child);
            continue;
        }

        into.absorbedTime += child.absorbedTime;
        into.time += child.time;

        Object.entries(child.attributes).forEach(([attribute, time]) => {
            if (into.attributes[attribute] !== undefined) {
                into.attributes[attribute] += time;
            } else {
                into.attributes[attribute] = time;
            }
        });

        into.addChildren(child.children);
        repeats.push(child);
    }

    // one pass over the children, removing them one by one is quadratic
    frame.removeChildren(repeats);
    repeats.forEach(repeat => removeFrameFromGroups(repeat, false));
}

/**
 * Removes a frame from any groups that it is a member of. Should be used when
 * removing a frame from a tree, so groups don't keep references to removed frames.
 *
 * @param frame The frame to be removed from groups.
 * @param recursive Whether to also remove all child frames from their groups.
 */
export function removeFrameFromGroups(frame: Frame, recursive: boolean): void {
    if (recursive && frame.children) {
        frame.children.forEach(child => {
            removeFrameFromGroups(child, true);
        });
    }

    if (frame.group) {
        const group = frame.group;
        group.removeFrame(frame);

        if (group.frames.length === 1) {
            // A group with only one frame is meaningless; remove it entirely.
            group.removeFrame(group.frames[0]);
        }
    }
}
