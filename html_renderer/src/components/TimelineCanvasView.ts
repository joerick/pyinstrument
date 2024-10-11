import CanvasView from "../lib/CanvasView";
import type Frame from "../lib/model/Frame";
import { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
import { hash, map, parseColor, sampleGradient } from "../lib/utils";
import TimelineCanvasViewTooltip, { estimateWidth, type TooltipFrameInfo } from "./TimelineCanvasViewTooltip.svelte";
import type { ComponentProps } from 'svelte';

const BACKGROUND_COLOR = '#212325'

const FRAME_PITCH = 18
const FRAME_HEIGHT = 17

const X_MARGIN = 28
const Y_MARGIN = 17
const Y_FRAME_INSET = 29 // vertical space between y margin and first frame, where the axis markers are drawn

const GRADIENT_STR = ['#3475BA','#318DBC','#47A298','#8AAE5D','#C1A731','#C07210','#B84210','#B53134','#9A3586','#4958B5','#3475BA']
const GRADIENT = GRADIENT_STR.map(parseColor)

export interface TimelineFrame {
    frame: Frame
    depth: number
    // also cache some computed properties that are used in rendering
    isApplicationCode: boolean
    library: string | null
    className: string
    filePathShort: string | null
}
export default class TimelineCanvasView extends CanvasView {
    zoom: number = 1 // pixels per second
    startT: number = 0 // seconds
    yOffset: number = 0 // pixels
    frames: TimelineFrame[] = []
    isZoomedIn: boolean = false

    tooltipContainer: HTMLElement
    tooltipComponent: TimelineCanvasViewTooltip | null = null

    constructor(container: HTMLElement) {
        super(container)

        this.onWheel = this.onWheel.bind(this)
        this.onMouseMove = this.onMouseMove.bind(this)
        this.onMouseLeave = this.onMouseLeave.bind(this)
        this.onMouseDown = this.onMouseDown.bind(this)
        this.windowMouseUp = this.windowMouseUp.bind(this)
        this.onTouchstart = this.onTouchstart.bind(this)
        this.onTouchmove = this.onTouchmove.bind(this)
        this.onTouchend = this.onTouchend.bind(this)
        this.onTouchcancel = this.onTouchend.bind(this)
        this.canvas.addEventListener('wheel', this.onWheel)
        this.canvas.addEventListener('mousemove', this.onMouseMove)
        this.canvas.addEventListener('mouseleave', this.onMouseLeave)
        this.canvas.addEventListener('mousedown', this.onMouseDown)
        this.canvas.addEventListener('touchstart', this.onTouchstart)
        this.canvas.addEventListener('touchmove', this.onTouchmove)
        this.canvas.addEventListener('touchend', this.onTouchend)
        this.canvas.addEventListener('touchcancel', this.onTouchcancel)

        this.tooltipContainer = document.createElement('div')
        this.tooltipContainer.style.position = 'absolute'
        this.tooltipContainer.style.pointerEvents = 'none'
        this.container.appendChild(this.tooltipContainer)
    }
    destroy(): void {
        this.canvas.removeEventListener('wheel', this.onWheel)
        this.canvas.removeEventListener('mousemove', this.onMouseMove)
        this.canvas.removeEventListener('mouseleave', this.onMouseLeave)
        this.canvas.removeEventListener('mousedown', this.onMouseDown)
        this.canvas.removeEventListener('touchstart', this.onTouchstart)
        this.canvas.removeEventListener('touchmove', this.onTouchmove)
        this.canvas.removeEventListener('touchend', this.onTouchend)
        this.canvas.removeEventListener('touchcancel', this.onTouchcancel)
        this.tooltipContainer.remove()
        super.destroy()
    }

    _rootFrame: Frame | null = null
    maxDepth = 0
    setRootFrame(rootFrame: Frame) {
        this._rootFrame = rootFrame
        this.frames = []
        this._frameMaxT = undefined
        this.maxDepth = 0
        this._collectFrames(rootFrame, 0)
        this.fitContents()
        this.setNeedsRedraw()
    }

    _collectFrames(frame: Frame, depth: number) {
        this.frames.push({
            frame,
            depth,
            isApplicationCode: frame.isApplicationCode,
            library: frame.library,
            className: frame.className,
            filePathShort: frame.filePathShort,
        })
        this.maxDepth = Math.max(this.maxDepth, depth)
        for (const child of frame.children) {
            if (child.identifier !== SELF_TIME_FRAME_IDENTIFIER) {
                // we don't render self time frames
                this._collectFrames(child, depth + 1)
            }
        }
    }

    tooltipLocation: { x: number; y: number } | null = null

    updateTooltip(ctx: CanvasRenderingContext2D, timelineFrame: TimelineFrame | null) {
        // update the content
        if (timelineFrame) {
            const frameInfo: TooltipFrameInfo = {
                name: this.frameName(timelineFrame),
                time: timelineFrame.frame.time,
                selfTime: this.frameSelfTime(timelineFrame),
                totalTime: this._rootFrame?.time ?? 1e-12,
                location: `${timelineFrame.filePathShort}:${timelineFrame.frame.lineNo}`,
                locationColor: this.colorForFrame(timelineFrame),
            }

            if (!this.tooltipComponent) {
                this.tooltipComponent = new TimelineCanvasViewTooltip({
                    target: this.tooltipContainer,
                    props: {f: frameInfo},
                })
            } else {
                this.tooltipComponent.$set({f: frameInfo})
            }

            // update the position
            if (this.tooltipLocation) {
                const position = {x: this.tooltipLocation.x + 12, y: this.tooltipLocation.y + 12}

                // rather than reading the width from the DOM, we estimate it
                // using canvas APIs. this tends to result in faster and more
                // predictable results. Also the DOM is very inefficient at
                // getting the size of something - it often has to relayout
                // the entire page.
                const tooltipWidth = estimateWidth(ctx, frameInfo)
                const maxX = this.width - 10 - tooltipWidth
                if (position.x > maxX) {
                    position.x = maxX
                }
                // note, this is a guess, but clipping off bottom will be rare, as will be wrapping tooltips
                const tooltipHeight = 60
                const maxY = this.height - 10 - tooltipHeight
                if (position.y > maxY) {
                    position.y = maxY
                }

                this.tooltipContainer.style.left = `${position.x}px`
                this.tooltipContainer.style.top = `${position.y}px`
            }
        }

        if (!timelineFrame) {
            if (this.tooltipComponent) {
                this.tooltipComponent.$destroy()
                this.tooltipComponent = null
            }
        }
    }

    //   /$$$$$$$                                    /$$
    //  | $$__  $$                                  |__/
    //  | $$  \ $$  /$$$$$$   /$$$$$$  /$$  /$$  /$$ /$$ /$$$$$$$   /$$$$$$
    //  | $$  | $$ /$$__  $$ |____  $$| $$ | $$ | $$| $$| $$__  $$ /$$__  $$
    //  | $$  | $$| $$  \__/  /$$$$$$$| $$ | $$ | $$| $$| $$  \ $$| $$  \ $$
    //  | $$  | $$| $$       /$$__  $$| $$ | $$ | $$| $$| $$  | $$| $$  | $$
    //  | $$$$$$$/| $$      |  $$$$$$$|  $$$$$/$$$$/| $$| $$  | $$|  $$$$$$$
    //  |_______/ |__/       \_______/ \_____/\___/ |__/|__/  |__/ \____  $$
    //                                                             /$$  \ $$
    //                                                            |  $$$$$$/
    //                                                             \______/

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

        const canDrag = this.maxYOffset > 0 || this.isZoomedIn
        const mouseDown = !!this.mouseDownLocation
        this.canvas.style.cursor = (mouseDown && canDrag) ? 'grabbing' : 'initial'

        // debug
        ctx.fillStyle = 'red'
        ctx.font = `23px "Source Sans Pro", sans-serif`
        // ctx.fillText(`startT: ${this.startT}`, 10, 10)
        // ctx.fillText(`zoom: ${this.zoom}`, 10, 50)
        // ctx.fillText(`width/zoom: ${this.width / this.zoom}`, 10, 50)

        let hoverFrame: TimelineFrame | null = null
        if (!mouseDown && this.tooltipLocation) {
            hoverFrame = this.hitTest(this.tooltipLocation)
        }
        this.updateTooltip(ctx, hoverFrame)
    }

    drawAxes(ctx: CanvasRenderingContext2D) {
        // const viewportDuration = this.width / this.zoom
        // clamp the width here to min 800 px, so that we don't draw too many
        // axes on small screens
        const viewportDuration = Math.max(800, this.width) / this.zoom

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
        const alphaForAxis = (a: number) => map(a, {from: [axisScale, axisScale-3], to: [0.71, 0], clamp: true})
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
        const startT = Math.floor(this.startT / increment) * increment
        const endT = this.startT + this.width / this.zoom
        const numDecimals = Math.max(0, Math.ceil(-Math.log10(increment)))

        for (let t = startT; t < endT; t += increment) {
            const x = this.xForT(t)
            const drawnByAHigherIncrement = Math.round(t / increment) % 10 === 0
            if (drawnByAHigherIncrement && !dontSkip) {
                continue
            }
            ctx.globalAlpha = alpha
            const y = Y_MARGIN - this.yOffset
            ctx.fillRect(x, y, 1, this.height - y)

            const textAlpha = map(alpha, {from: [0.12, 0.25], to: [0, 0.5], clamp: true})
            if (textAlpha > 0.01) {
                ctx.globalAlpha = textAlpha
                ctx.font = `13px "Source Sans Pro", sans-serif`
                let text = t.toFixed(numDecimals)
                if (text == '0') {
                    text = '0s'
                }
                let topY = y + 10
                ctx.fillText(text, x + 3, topY)
                let bottomY = this.height + Y_MARGIN + 10 - this.yOffset
                if (bottomY < this.height - 3) {
                    bottomY = this.height - 3
                }
                ctx.fillText(text, x + 3, bottomY)
            }
            ctx.globalAlpha = 1
        }
    }

    drawFrame(ctx: CanvasRenderingContext2D, timelineFrame: TimelineFrame) {
        const { x, y, w, h } = this.frameDims(timelineFrame)
        const endX = x + w
        if (endX < 0 || x > this.width) {
            // offscreen
            return
        }

        ctx.fillStyle = this.colorForFrame(timelineFrame)
        ctx.globalAlpha = timelineFrame.isApplicationCode ? 1 : 0.5

        if (w < 2) {
            // fast path
            ctx.fillRect(x, y, w, h)
            return
        }

        let name = this.frameName(timelineFrame)

        // the minimum width per character is 3.3px (that's an 'l')
        // no point in drawing more characters than that, it'll be clipped
        const maxChars = Math.floor(w / 3.3)
        if (name.length > maxChars) {
            name = name.substring(0, maxChars)
        }
        if (name.length == 0) {
            // fast path
            ctx.fillRect(x, y, w, h)
            return
        }

        ctx.save()
        ctx.beginPath()
        ctx.rect(x, y, w, h)
        ctx.fill()
        ctx.clip()

        ctx.font = `13px "Source Sans Pro", sans-serif`
        ctx.fillStyle = 'white'
        let textX = x
        if (textX < 0) {
            textX = 0
        }
        ctx.fillText(name, textX + 2, y + 13)

        ctx.restore()
    }

    // the library order controls which color is assigned. More common
    // libraries get colors further apart from each other
    _libraryOrder: string[] | null = null
    _assignLibraryOrder() {
        const librariesTotalTime: Record<string, number> = {}

        for (const timelineFrame of this.frames) {
            const frame = timelineFrame.frame
            const library = frame.library ?? ''
            librariesTotalTime[library] = (librariesTotalTime[library] || 0) + timelineFrame.frame.time
        }

        const libraries = Object.keys(librariesTotalTime)
        libraries.sort((a, b) => librariesTotalTime[b] - librariesTotalTime[a])
        this._libraryOrder = libraries
    }

    _colors: string[] = []
    colorForLibraryIndex(libraryIndex: number) {
        if (this._colors[libraryIndex] !== undefined) {
            return this._colors[libraryIndex]
        }
        // assign colors using color gradient and library order, gradually
        // bisecting a color wheel - this gives the top libraries the most
        // distinct colors
        const denominator = Math.pow(2,Math.ceil(Math.log2(libraryIndex+1)))
        const numerator = 2*libraryIndex - denominator + 1
        const gradientLocation = numerator/denominator
        const result = sampleGradient(GRADIENT, gradientLocation)
        this._colors[libraryIndex] = result
        return result
    }

    libraryIndexForFrame(timelineFrame: TimelineFrame) {
        if (!this._libraryOrder) {
            this._assignLibraryOrder()
        }

        const library = timelineFrame.library || ''
        let result = this._libraryOrder!.indexOf(library)

        if (result === -1) {
            // we haven't seen this one before, add it to the list to give it an index
            result = this._libraryOrder!.length
            this._libraryOrder!.push(library)
        }

        return result
    }

    colorForFrame(timelineFrame: TimelineFrame) {
        const libraryIndex = this.libraryIndexForFrame(timelineFrame)
        const color = this.colorForLibraryIndex(libraryIndex)
        return color
    }

    //   /$$                                                 /$$
    //  | $$                                                | $$
    //  | $$        /$$$$$$  /$$   /$$  /$$$$$$  /$$   /$$ /$$$$$$
    //  | $$       |____  $$| $$  | $$ /$$__  $$| $$  | $$|_  $$_/
    //  | $$        /$$$$$$$| $$  | $$| $$  \ $$| $$  | $$  | $$
    //  | $$       /$$__  $$| $$  | $$| $$  | $$| $$  | $$  | $$ /$$
    //  | $$$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$/|  $$$$$$/  |  $$$$/
    //  |________/ \_______/ \____  $$ \______/  \______/    \___/
    //                       /$$  | $$
    //                      |  $$$$$$/
    //                       \______/

    _frameMaxT: number|undefined
    get frameMaxT() {
        if (this._frameMaxT === undefined) {
            this._frameMaxT = this.frames.reduce((max, frame) => Math.max(max, frame.frame.startTime + frame.frame.time), 0)
        }
        return this._frameMaxT
    }

    get maxYOffset() {
        return Math.max(0, (this.maxDepth+1) * FRAME_PITCH + Y_MARGIN*2 + Y_FRAME_INSET - this.height)
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

        if (this.yOffset < 0) {
            this.yOffset = 0
        }
        if (this.yOffset > this.maxYOffset) {
            this.yOffset = this.maxYOffset
        }
    }

    frameDims(timelineFrame: TimelineFrame): { x: number; y: number; w: number; h: number } {
        const y = timelineFrame.depth * FRAME_PITCH + Y_MARGIN + Y_FRAME_INSET - this.yOffset
        const h = FRAME_HEIGHT
        let x = this.xForT(timelineFrame.frame.startTime)
        const endX = this.xForT(timelineFrame.frame.startTime + timelineFrame.frame.time)
        let w = endX - x

        if (w < 1) {
            w = 1
        }
        if (w > 1) {
            // add a little gap between frames
            w -= map(w, {from: [1,3], to: [0, 1], clamp: true})
        }
        return { x, y, w, h }
    }

    xForT(t: number): number {
        return (t - this.startT) * this.zoom + X_MARGIN
    }

    tForX(x: number): number {
        return (x - X_MARGIN) / this.zoom + this.startT
    }

    frameName(timelineFrame: TimelineFrame): string {
        let name: string
        if (timelineFrame.className) {
            name = `${timelineFrame.className}.${timelineFrame.frame.function}`
        } else if (timelineFrame.frame.function == '<module>'){
            name = timelineFrame.filePathShort ?? timelineFrame.frame.filePath ?? ''
        } else {
            name = timelineFrame.frame.function
        }
        return name
    }

    frameSelfTime(timelineFrame: TimelineFrame): number {
        let selfTime = timelineFrame.frame.time;
        const renderedChildren = timelineFrame.frame.children.filter(child => !child.isSynthetic);

        for (const child of renderedChildren) {
            selfTime -= child.time;
        }

        return selfTime;
    }

    hitTest(loc: {x: number, y: number}): TimelineFrame | null {
        for (const frame of this.frames) {
            const { x: frameX, y: frameY, w, h } = this.frameDims(frame)
            if (loc.x >= frameX && loc.x <= frameX + w && loc.y >= frameY && loc.y <= frameY + h) {
                return frame
            }
        }
        return null
    }

    //   /$$      /$$
    //  | $$$    /$$$
    //  | $$$$  /$$$$  /$$$$$$  /$$   /$$  /$$$$$$$  /$$$$$$
    //  | $$ $$/$$ $$ /$$__  $$| $$  | $$ /$$_____/ /$$__  $$
    //  | $$  $$$| $$| $$  \ $$| $$  | $$|  $$$$$$ | $$$$$$$$
    //  | $$\  $ | $$| $$  | $$| $$  | $$ \____  $$| $$_____/
    //  | $$ \/  | $$|  $$$$$$/|  $$$$$$/ /$$$$$$$/|  $$$$$$$
    //  |__/     |__/ \______/  \______/ |_______/  \_______/
    //
    //
    //
    onWheel(event: WheelEvent) {
        const isPinchGestureOrCmdWheel = event.ctrlKey || event.metaKey

        // zooming
        const zoomSpeed = isPinchGestureOrCmdWheel ? 0.01 : 0.0023
        const mouseT = this.tForX(event.offsetX)
        this.zoom *= 1 - event.deltaY * zoomSpeed
        // an extra clamp to clamp this.zoom before the startT is adjusted
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
    mouseDownLocation: { x: number; y: number } | null = null
    onMouseMove(event: MouseEvent): void {
        const mouseLocation = { x: event.offsetX, y: event.offsetY }
        const prevMouseLocation = this.mouseLocation
        this.mouseLocation = mouseLocation
        if (prevMouseLocation && this.mouseDownLocation) {
            const dLocation = {x: mouseLocation.x - prevMouseLocation.x, y: mouseLocation.y - prevMouseLocation.y}
            this.startT -= dLocation.x / this.zoom
            this.yOffset -= dLocation.y
            this.clampViewport()
        }
        this.tooltipLocation = mouseLocation
        this.setNeedsRedraw()
    }
    onMouseLeave(event: MouseEvent): void {
        this.mouseLocation = null
        this.tooltipLocation = null
        this.setNeedsRedraw()
    }
    onMouseDown(event: MouseEvent): void {
        if (!(event.button === 0 || event.button === 1)) {
            return
        }
        this.mouseDownLocation = { x: event.offsetX, y: event.offsetY }
        window.addEventListener('mouseup', this.windowMouseUp)
        this.setNeedsRedraw()
    }
    windowMouseUp(event: MouseEvent): void {
        window.removeEventListener('mouseup', this.windowMouseUp)
        this.mouseDownLocation = null
        this.setNeedsRedraw()
    }

    //   /$$$$$$$$                               /$$
    //  |__  $$__/                              | $$
    //     | $$     /$$$$$$  /$$   /$$  /$$$$$$$| $$$$$$$
    //     | $$    /$$__  $$| $$  | $$ /$$_____/| $$__  $$
    //     | $$   | $$  \ $$| $$  | $$| $$      | $$  \ $$
    //     | $$   | $$  | $$| $$  | $$| $$      | $$  | $$
    //     | $$   |  $$$$$$/|  $$$$$$/|  $$$$$$$| $$  | $$
    //     |__/    \______/  \______/  \_______/|__/  |__/

    touches: { [key: number]: { x: number; y: number, downT: number, startDate: number, downX: number, downY: number } } = {}
    onTouchstart(event: TouchEvent) {
        event.preventDefault()
        event.stopPropagation()

        for (const touch of Array.from(event.changedTouches)) {
            this.touches[touch.identifier] = {
                x: touch.clientX,
                y: touch.clientY,
                downT: this.tForX(touch.clientX),
                startDate: Date.now(),
                downX: touch.clientX,
                downY: touch.clientY,
            }
        }
    }
    onTouchmove(event: TouchEvent) {
        event.preventDefault()
        event.stopPropagation()

        let yMotionSum = 0
        for (const touch of Array.from(event.changedTouches)) {
            const prevTouch = this.touches[touch.identifier]
            if (!prevTouch) {
                continue
            }
            yMotionSum += touch.clientY - prevTouch.y
            this.touches[touch.identifier] = {
                ...prevTouch,
                x: touch.clientX,
                y: touch.clientY
            }
        }
        const yMotion = yMotionSum / Object.keys(this.touches).length
        this.yOffset -= yMotion
        this.adjustXAxisForTouches()
        this.setNeedsRedraw()
    }
    onTouchend(event: TouchEvent) {
        event.preventDefault()
        event.stopPropagation()

        for (const touch of Array.from(event.changedTouches)) {
            delete this.touches[touch.identifier]
        }
        this.setNeedsRedraw()
    }
    onTouchcancel(event: TouchEvent) {
        event.preventDefault()
        event.stopPropagation()

        for (const touch of Array.from(event.changedTouches)) {
            delete this.touches[touch.identifier]
        }
        this.setNeedsRedraw()
    }
    adjustXAxisForTouches() {
        const touchIds = Object.keys(this.touches).map(Number)
        if (touchIds.length == 0) {
            return
        }
        if (touchIds.length == 1) {
            const touch = this.touches[touchIds[0]]
            this.startT = touch.downT - (touch.x - X_MARGIN) / this.zoom
        }
        if (touchIds.length >= 2) {
            const touch1 = this.touches[touchIds[0]]
            const touch2 = this.touches[touchIds[1]]
            const newZoom = (touch2.x - touch1.x) / (touch2.downT - touch1.downT)
            const newStartT = touch1.downT - (touch1.x - X_MARGIN) / newZoom
            this.startT = newStartT
            this.zoom = newZoom
        }
        this.clampViewport()
    }
}
