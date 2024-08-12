import CanvasView from "../lib/CanvasView";
import type Frame from "../lib/model/Frame";
import { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
import { hash, parseColor, sampleGradient } from "../lib/utils";

const BACKGROUND_COLOR = '#212325'

const FRAME_PITCH = 18
const FRAME_HEIGHT = 17


const GRADIENT_STR = ['#47A298','#9FC175','#C1A731','#C07210','#B84210','#B53134','#9A3586','#4958B5','#3475BA','#318DBC','#47A298']
const GRADIENT = GRADIENT_STR.map(parseColor)

export interface TimelineFrame {
    frame: Frame
    depth: number
}
export default class TimelineCanvasView extends CanvasView {
    zoom: number = 1
    startT: number = 0
    frames: TimelineFrame[] = []
    isZoomedIn: boolean = false

    constructor(container: HTMLElement) {
        super(container)

        this.onWheel = this.onWheel.bind(this)
        this.canvas.addEventListener('wheel', this.onWheel)
    }
    destroy(): void {
        super.destroy()
        this.canvas.removeEventListener('wheel', this.onWheel)
    }

    setRootFrame(rootFrame: Frame) {
        this.frames = []
        this._collectFrames(rootFrame, 0)
        this.fitContents()
    }

    _collectFrames(frame: Frame, depth: number) {
        this.frames.push({ frame, depth })
        for (const child of frame.children) {
            if (child.identifier !== SELF_TIME_FRAME_IDENTIFIER) {
                // we don't render self time frames
                this._collectFrames(child, depth + 1)
            }
        }
    }

    get frameMaxT() {
        return this.frames.reduce((max, frame) => Math.max(max, frame.frame.startTime + frame.frame.time), 0)
    }

    get minZoom() {
        return this.width / this.frameMaxT
    }

    fitContents() {
        this.startT = 0
        this.zoom = this.minZoom
        this.isZoomedIn = false
    }

    clampViewport() {
        if (this.zoom < this.minZoom) {
            this.zoom = this.minZoom
            this.isZoomedIn = false
        } else {
            this.isZoomedIn = true
        }

        if (this.startT < 0) {
            this.startT = 0
        }
        const maxStartT = this.frameMaxT - this.width / this.zoom
        if (this.startT > maxStartT) {
            this.startT = maxStartT
        }
    }

    lastDrawWidth: number = 0
    lastDrawHeight: number = 0

    redraw(ctx: CanvasRenderingContext2D, extra: { width: number; height: number; }): void {
        const { width, height } = extra

        if (width !== this.lastDrawWidth || height !== this.lastDrawHeight) {
            if (!this.isZoomedIn) {
                this.fitContents()
            } else {
                this.clampViewport()
            }
        }
        this.lastDrawWidth = width
        this.lastDrawHeight = height

        ctx.fillStyle = BACKGROUND_COLOR
        ctx.fillRect(0, 0, width, height)

        // draw scale
        // TODO

        // draw frames
        for (const frame of this.frames) {
            this.drawFrame(ctx, frame)
        }

        ctx.globalAlpha = 1

        // debug
        ctx.fillStyle = 'red'
        ctx.fillText(`startT: ${this.startT}`, 10, 10)
        ctx.fillText(`zoom: ${this.zoom}`, 10, 20)
    }

    drawFrame(ctx: CanvasRenderingContext2D, timelineFrame: TimelineFrame) {
        const y = timelineFrame.depth * FRAME_PITCH
        const h = FRAME_HEIGHT
        let x = this.xForT(timelineFrame.frame.startTime)
        const endX = this.xForT(timelineFrame.frame.startTime + timelineFrame.frame.time)
        let width = endX - x

        if (endX < 0 || x > this.width) {
            // offscreen
            return
        }

        if (width < 1) {
            width = 1
        }
        if (width > 2) {
            // add a little margin
            width -= 1
        }

        ctx.fillStyle = this.colorForFrame(timelineFrame)
        ctx.globalAlpha = timelineFrame.frame.isApplicationCode ? 1 : 0.5

        if (width < 2) {
            // fast path
            ctx.fillRect(x, y, width, h)
            return
        }

        ctx.save()
        ctx.beginPath()
        ctx.rect(x, y, width, h)
        ctx.fill()
        ctx.clip()

        if (width > 2) {
            ctx.font = `13px "Source Sans Pro", sans-serif`
            ctx.fillStyle = 'white'
            let name: string
            if (timelineFrame.frame.className) {
                name = `${timelineFrame.frame.className}.${timelineFrame.frame.function}`
            } else if (timelineFrame.frame.function == '<module>'){
                name = timelineFrame.frame.filePathShort ?? timelineFrame.frame.filePath ?? ''
            } else {
                name = timelineFrame.frame.function
            }
            if (x < 0) {
                x = 0
            }
            ctx.fillText(name, x + 2, y + 13)
        }
        ctx.restore()
    }

    xForT(t: number): number {
        return (t - this.startT) * this.zoom
    }

    onWheel(event: WheelEvent) {
        // pinch to zoom & cmd+wheel to zoom
        if (event.ctrlKey || event.metaKey) {
            const mouseT = this.startT + event.offsetX / this.zoom
            this.zoom *= 1 - event.deltaY / 100
            this.startT = mouseT - event.offsetX / this.zoom
            this.clampViewport()
            this.setNeedsRedraw()
            event.preventDefault()
            return
        }
        // scroll to pan
        this.startT += event.deltaX / this.zoom
        this.clampViewport()
        this.setNeedsRedraw()
        event.preventDefault()

        // this.setNeedsRedraw()
    }
    mouseLocation: { x: number; y: number } | null = null
    onMouseMove(event: MouseEvent): void {
        this.mouseLocation = { x: event.offsetX, y: event.offsetY }
        this.setNeedsRedraw()
    }
    onMouseLeave(event: MouseEvent): void {
        // console.log('mouse leave', event)
        this.mouseLocation = null
        this.setNeedsRedraw()
    }

    // the library order controls which color is assigned. More common
    // libraries get colors further apart from each other
    _libraryOrder: string[] | null = null
    _assignLibraryOrder() {
        const librariesOccurenceCounts: Record<string, number> = {}

        for (const timelineFrame of this.frames) {
            const frame = timelineFrame.frame
            const library = frame.library ?? ''
            librariesOccurenceCounts[library] = (librariesOccurenceCounts[library] || 0) + 1
        }

        const libraries = Object.keys(librariesOccurenceCounts)
        libraries.sort((a, b) => librariesOccurenceCounts[b] - librariesOccurenceCounts[a])
        this._libraryOrder = libraries
    }

    _colors: string[] = []
    colorForLibraryIndex(libraryIndex: number) {
        if (this._colors[libraryIndex] !== undefined) {
            return this._colors[libraryIndex]
        }
        // assign colors using color gradient and library order,
        // gradually bisecting a color wheel
        const denominator = Math.pow(2,Math.ceil(Math.log2(libraryIndex+1)))
        const numerator = 2*libraryIndex - denominator + 1
        const gradientLocation = numerator/denominator
        const result = sampleGradient(GRADIENT, gradientLocation)
        this._colors[libraryIndex] = result
        return result
    }

    colorForFrame(frame: TimelineFrame) {
        if (!this._libraryOrder) {
            this._assignLibraryOrder()
        }

        let libraryIndex = this._libraryOrder?.indexOf(frame.frame.library || '') ?? 0
        if (libraryIndex === -1) {
            libraryIndex = 0
        }
        const color = this.colorForLibraryIndex(libraryIndex)
        return color
        // return sampleGradient(GRADIENT, hash(frame.frame.library ?? ''))
    }
}
