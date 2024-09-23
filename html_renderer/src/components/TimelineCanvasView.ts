import CanvasView from "../lib/CanvasView";
import type Frame from "../lib/model/Frame";
import { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
import { hash, map, parseColor, sampleGradient } from "../lib/utils";

const BACKGROUND_COLOR = '#212325'

const FRAME_PITCH = 18
const FRAME_HEIGHT = 17

const X_MARGIN = 28
const Y_MARGIN = 17
const Y_FRAME_INSET = 29 // vertical space between y margin and first frame, where the axis markers are drawn

const GRADIENT_STR = ['#47A298','#9FC175','#C1A731','#C07210','#B84210','#B53134','#9A3586','#4958B5','#3475BA','#318DBC','#47A298']
const GRADIENT = GRADIENT_STR.map(parseColor)

export interface TimelineFrame {
    frame: Frame
    depth: number
}
export default class TimelineCanvasView extends CanvasView {
    zoom: number = 1 // pixels per second
    startT: number = 0 // seconds
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
        this._frameMaxT = undefined
        this._collectFrames(rootFrame, 0)
        this.fitContents()
        this.setNeedsRedraw()
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

    _frameMaxT: number|undefined
    get frameMaxT() {
        if (this._frameMaxT === undefined) {
            this._frameMaxT = this.frames.reduce((max, frame) => Math.max(max, frame.frame.startTime + frame.frame.time), 0)
        }
        return this._frameMaxT
    }

    get minZoom() {
        return (this.width - 2*X_MARGIN) / this.frameMaxT
    }

    get maxZoom() {
        // 150 ns is the python function calling overhead.
        // 150 ns per 10 pixels seems the smallest that makes sense to me
        return 10 / 150e-9
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

        if (this.zoom > this.maxZoom) {
            this.zoom = this.maxZoom
        }

        if (this.startT < 0) {
            this.startT = 0
        }
        const maxStartT = this.frameMaxT - (this.width - 2*X_MARGIN) / this.zoom
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
        this.drawAxes(ctx)

        // draw frames
        for (const frame of this.frames) {
            this.drawFrame(ctx, frame)
        }

        ctx.globalAlpha = 1

        // debug
        ctx.fillStyle = 'red'
        ctx.font = `23px "Source Sans Pro", sans-serif`
        // ctx.fillText(`startT: ${this.startT}`, 10, 10)
        // ctx.fillText(`zoom: ${this.zoom}`, 10, 50)
        // ctx.fillText(`width/zoom: ${this.width / this.zoom}`, 10, 50)
    }

    drawAxes(ctx: CanvasRenderingContext2D) {
        const viewportDuration = this.width / this.zoom
        if (viewportDuration == 0) {
            // avoid log of 0
            return
        }
        const axisScale = Math.log10(viewportDuration)
        let highestAxis = Math.ceil(axisScale) + 2
        if (highestAxis < 0) {
            // ensures that we always draw whole number axes, stops numbers
            // like '0' from changing precision to '0.0' as we zoom in
            highestAxis = 0
        }
        const smallestAxis = Math.ceil(axisScale) - 3
        const alphaForAxis = (a: number) => map(a, {from: [axisScale, axisScale-3], to: [0.71, 0]})
        for (let a = smallestAxis; a < highestAxis; a++) {
            let alpha = alphaForAxis(a)
            alpha = Math.max(0, Math.min(1, alpha))
            alpha = Math.pow(alpha, 2)
            this.drawAxis(ctx, Math.pow(10, a), alpha)
        }
        // highest axis - set the flag to never skip as there are no higher increments
        this.drawAxis(ctx, Math.pow(10, highestAxis), alphaForAxis(highestAxis), true)
    }

    drawAxis(ctx: CanvasRenderingContext2D, increment: number, alpha: number, dontSkip: boolean = false) {
        ctx.fillStyle = 'white'
        const startT = Math.ceil(this.startT / increment) * increment
        const endT = this.startT + this.width / this.zoom
        const decimals = Math.max(0, Math.ceil(-Math.log10(increment)))

        for (let t = startT; t < endT; t += increment) {
            const x = this.xForT(t)
            const drawnByAHigherIncrement = Math.round(t / increment) % 10 === 0
            if (drawnByAHigherIncrement && !dontSkip) {
                continue
            }
            ctx.globalAlpha = alpha
            ctx.fillRect(x, Y_MARGIN, 1, this.height - Y_MARGIN)

            const textAlpha = map(alpha, {from: [0.12, 0.25], to: [0, 0.5], clamp: true})
            if (textAlpha > 0.01) {
                ctx.globalAlpha = textAlpha
                ctx.font = `13px "Source Sans Pro", sans-serif`
                let text = t.toFixed(decimals)
                if (text == '0') {
                    text = '0s'
                }
                ctx.fillText(text, x + 3, Y_MARGIN+10)
            }
            ctx.globalAlpha = 1
        }
    }

    drawFrame(ctx: CanvasRenderingContext2D, timelineFrame: TimelineFrame) {
        const y = timelineFrame.depth * FRAME_PITCH + Y_MARGIN + Y_FRAME_INSET
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
            // add a little gap between frames
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
            // the minimum width per character is 3.3px (that's an 'l')
            // no point in drawing more characters than that, it'll be clipped
            const maxChars = Math.floor(width / 3.3)
            if (name.length > maxChars) {
                name = name.substring(0, maxChars)
            }
            ctx.fillText(name, x + 2, y + 13)
        }
        ctx.restore()
    }

    xForT(t: number): number {
        return (t - this.startT) * this.zoom + X_MARGIN
    }

    tForX(x: number): number {
        return (x - X_MARGIN) / this.zoom + this.startT
    }

    onWheel(event: WheelEvent) {
        const isPinchGestureOrCmdWheel = event.ctrlKey || event.metaKey

        // zooming
        const zoomSpeed = isPinchGestureOrCmdWheel ? 0.01 : 0.0023
        const mouseT = this.tForX(event.offsetX)
        this.zoom *= 1 - event.deltaY * zoomSpeed
        this.clampViewport()
        this.startT = mouseT - (event.offsetX - X_MARGIN) / this.zoom

        // scroll to pan
        if (!isPinchGestureOrCmdWheel) {
            this.startT += event.deltaX / this.zoom
        }
        this.clampViewport()
        this.setNeedsRedraw()
        event.preventDefault()
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
