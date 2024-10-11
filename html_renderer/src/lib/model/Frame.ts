import type FrameGroup from './FrameGroup';
import { randomId } from '../utils';
// import type { FrameData } from '../dataTypes';

export interface FrameData {
    identifier: string,
    time?: number // duration in seconds
    startTime?: number
    attributes?: {[name: string]: number},
    children?: readonly FrameData[],
}


const IDENTIFIER_SEP = "\x00"
const ATTRIBUTES_SEP = "\x01"

export const AWAIT_FRAME_IDENTIFIER = "[await]"
export const SELF_TIME_FRAME_IDENTIFIER = "[self]"
export const OUT_OF_CONTEXT_FRAME_IDENTIFIER = "[out-of-context]"
export const DUMMY_ROOT_FRAME_IDENTIFIER = "[root]"

export const SYNTHETIC_FRAME_IDENTIFIERS = [
    AWAIT_FRAME_IDENTIFIER,
    SELF_TIME_FRAME_IDENTIFIER,
    OUT_OF_CONTEXT_FRAME_IDENTIFIER,
    DUMMY_ROOT_FRAME_IDENTIFIER,
]

export const SYNTHETIC_LEAF_IDENTIFIERS = [
    AWAIT_FRAME_IDENTIFIER,
    SELF_TIME_FRAME_IDENTIFIER,
    OUT_OF_CONTEXT_FRAME_IDENTIFIER,
]

const ATTRIBUTE_MARKER_CLASS_NAME = "c"
const ATTRIBUTE_MARKER_LINE_NUMBER = "l"
const ATTRIBUTE_MARKER_TRACEBACKHIDE = "h"

export default class Frame {
    uuid: string = randomId()
    identifier: string
    _identifierParts: string[]
    startTime: number
    time: number = 0
    absorbedTime: number = 0
    group: FrameGroup|null = null
    attributes: {[name: string]: number}
    _children: Frame[] = []
    parent: Frame | null = null

    context: FrameContext

    constructor(
        data: FrameData,
        context: FrameContext,
    ) {
        this.identifier = data.identifier
        this._identifierParts = this.identifier.split(IDENTIFIER_SEP)
        this.startTime = data.startTime ?? 0
        this.time = data.time ?? 0
        this.attributes = data.attributes ?? {}
        this.context = context

        let childStartTime = this.startTime
        const children = data.children?.map(f => {
            if (f.startTime === undefined) {
                f = {...f, startTime: childStartTime}
                childStartTime += f.time ?? 0
            }
            childStartTime = f.startTime! + (f.time ?? 0)
            return new Frame(f, context)
        });
        if (children) {
            this.addChildren(children)
        }
    }

    cloneDeep(): Frame {
        return new Frame(this, this.context)
    }

    get children(): readonly Frame[] {
        return this._children
    }

    addChild(frame: Frame, options: {after?: Frame} = {}) {
        frame.removeFromParent()
        frame.parent = this
        if (options.after) {
            const index = this._children.indexOf(options.after)
            if (index == -1) {
                throw new Error("After frame not found")
            }
            this._children.splice(index+1, 0, frame)
        } else {
            this._children.push(frame)
        }
    }

    addChildren(frames: readonly Frame[], options: {after?: Frame} = {}) {
        frames = frames.slice()
        if (options.after) {
            const reversed = frames.slice()
            reversed.reverse()
            frames.forEach(f => this.addChild(f, options))
        } else {
            frames.forEach(f => this.addChild(f, options))
        }
    }

    removeFromParent() {
        if (this.parent) {
            const idx = this.parent._children.indexOf(this)
            this.parent._children.splice(idx, 1)
            this.parent = null
        }
    }

    getAttributes(marker: string): {data: string, time: number}[] {
        const keys = Object.keys(this.attributes).filter(k => k.startsWith(marker))
        return keys.map(k => (
            {data: k.slice(1), time: this.attributes[k]}
        ))
    }

    getAttributeValue(marker: string) {
        const attributes = this.getAttributes(marker)
        if (!attributes) return null
        if (attributes.length == 0) return null

        let maxIdx = 0
        for (let i = 0; i < attributes.length; i++) {
            if (attributes[i].time > attributes[maxIdx].time) {
                maxIdx = i
            }
        }

        return attributes[maxIdx].data
    }

    get hasTracebackHide(): boolean {
        return this.getAttributeValue(ATTRIBUTE_MARKER_TRACEBACKHIDE) == '1'
    }

    get function(): string {
        return this._identifierParts[0]
    }

    get filePath(): string | null {
        return this._identifierParts[1] ?? null
    }

    get lineNo(): number | null {
        const lineNo = this._identifierParts[2]
        return lineNo ? parseInt(lineNo) : null
    }

    get isSynthetic(): boolean {
        return SYNTHETIC_FRAME_IDENTIFIERS.includes(this.identifier)
    }

    get filePathShort(): string | null {
        if (this.isSynthetic && this.parent) {
            return this.parent.filePathShort
        }

        if (!this.filePath) return null

        return this.context.shortenPath(this.filePath)
    }

    get isApplicationCode(): boolean {
        if (this.isSynthetic) {
            return false;
        }

        const filePath = this.filePath;

        if (!filePath) {
            return false;
        }

        const prefixes = this.context.sysPrefixes
        if (prefixes.some(path => filePath.startsWith(path))) {
            // this code lives in the Python installation dir or a virtualenv
            return false;
        }

        if (filePath.startsWith("<")) {
            if (filePath.startsWith("<ipython-input-")) {
                // Lines typed at a console or in a notebook are considered application code
                return true;
            } else if (filePath == "<string>" || filePath == "<stdin>") {
                // eval/exec is app code if started by a parent frame that is app code
                if (this.parent) {
                    return this.parent.isApplicationCode
                } else {
                    // if this is the root frame, it must have been started
                    // with -c, so it's app code
                    return true
                }
            } else {
                // Otherwise, this is likely some form of library-internal code generation
                return false;
            }
        }

        return true;
    }

    get proportionOfParent(): number {
        if (!this.parent) {
            return 1;
        }

        return this.time / this.parent.time;
    }

    get className(): string {
        return this.getAttributeValue(ATTRIBUTE_MARKER_CLASS_NAME) ?? ""
    }

    get library(): string|null {
        const filePathShort = this.filePathShort;
        if (!filePathShort) {
            return null;
        }
        // return the first part of the path that isn't slashes or dots
        return /^[\\/.]*[^\\/.]*/.exec(filePathShort)![0] ?? ''
    }
}

interface FrameContext {
    shortenPath(path: string): string
    sysPrefixes: string[]
}
