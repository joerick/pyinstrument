import CanvasView from "../lib/CanvasView";
import type Frame from "../lib/model/Frame";

const BACKGROUND_COLOR = '#212325'

export default class TimelineCanvasView extends CanvasView {
    zoom: number = 1
    startT: number = 0
    frames: Frame[] = []

    constructor(container: HTMLElement) {
        super(container)

        this.onWheel = this.onWheel.bind(this)
        this.canvas.addEventListener('wheel', this.onWheel)
    }
    destroy(): void {
        // TODO: call super?
        this.canvas.removeEventListener('wheel', this.onWheel)
    }
    redraw(ctx: CanvasRenderingContext2D, extra: { width: number; height: number; }): void {
        const { width, height } = extra
        ctx.fillStyle = BACKGROUND_COLOR
        ctx.fillRect(0, 0, width, height)

        // draw scale
        // TODO

        // draw frames
        for (const frame of this.frames) {

        }
    }

    onWheel(event: WheelEvent) {

    }

    // the library order controls which color is assigned. More common colors
    // are
    _libraryOrder: string[] | null = null
    _assignLibraryOrder() {
        const librariesOccurenceCounts: Record<string, number> = {}

        for (const frame of this.frames) {
            frame.
        }
    }
    colorForFrame(frame: Frame) {

    }
}
