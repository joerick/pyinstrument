import type FrameGroup from './FrameGroup';
// import type { FrameData } from '../dataTypes';

export interface FrameData {
    identifier: string,
    time?: number
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
    uuid: string = crypto.randomUUID()
    identifier: string
    _identifierParts: string[]
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
        this.time = data.time ?? 0
        this.attributes = data.attributes ?? {}
        this.context = context

        const children = data.children?.map(f => new Frame(f, context));
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
            this._children.splice(index+1, 0, frame)
        } else {
            this._children.push(frame)
        }
    }

    addChildren(frames: readonly Frame[], options: {after?: Frame} = {}) {
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

    get hasTracebackhide(): boolean {
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

        const libPaths = ["/lib/", "\\lib\\"];
        if (libPaths.some(path => filePath.includes(path))) {
            return false;
        }

        if (filePath.startsWith("<")) {
            if (filePath.startsWith("<ipython-input-")) {
                // Lines typed at a console or in a notebook are considered application code
                return true;
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
}

interface FrameContext {
    shortenPath(path: string): string
}
