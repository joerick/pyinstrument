import DevicePixelRatioObserver from "./DevicePixelRatioObserver"

export default abstract class CanvasView {
    canvas: HTMLCanvasElement
    _size_observer: ResizeObserver
    _devicePixelRatioObserver: DevicePixelRatioObserver

    constructor(readonly container: HTMLElement) {
        if (getComputedStyle(container).position != "absolute") {
            container.style.position = 'relative'
        }

        this.canvas = document.createElement('canvas')
        this.canvas.style.position = 'absolute'
        this.canvas.style.left = '0'
        this.canvas.style.top = '0'
        this.canvas.style.width = '100%'
        this.canvas.style.height = '100%'
        this.container.appendChild(this.canvas)

        this.setCanvasSize = this.setCanvasSize.bind(this);

        this._size_observer = new ResizeObserver(this.setCanvasSize)
        this._size_observer.observe(container);

        this._devicePixelRatioObserver = new DevicePixelRatioObserver(this.setCanvasSize)

        // set the canvas size on the next redraw - avoids problems with window
        // size changing during the first paint because of the scroll bar
        window.requestAnimationFrame(() => {
            this.setCanvasSize();
        });
    }

    destroy() {
        this._size_observer.disconnect()
        this._devicePixelRatioObserver.destroy()
        this.canvas.remove();
        if (this.drawAnimationRequest !== null) {
            window.cancelAnimationFrame(this.drawAnimationRequest);
            this.drawAnimationRequest = null
        }
    }

    drawAnimationRequest: any = null

    setNeedsRedraw() {
        if (this.drawAnimationRequest !== null) {
            return
        }

        this.drawAnimationRequest = window.requestAnimationFrame(() => {
            this.drawAnimationRequest = null;
            this.canvasViewRedraw()
        })
    }

    redrawIfNeeded() {
        if (this.drawAnimationRequest !== null) {
            window.cancelAnimationFrame(this.drawAnimationRequest);
            this.drawAnimationRequest = null;
            this.canvasViewRedraw()
        }
    }

    canvasViewRedraw() {
        const ctx = this.canvas.getContext('2d')
        if (!ctx) return

        ctx.resetTransform()
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio)

        this.redraw(ctx, {
            width: this.canvas.width / window.devicePixelRatio,
            height: this.canvas.height / window.devicePixelRatio
        });
    }
    abstract redraw(ctx: CanvasRenderingContext2D, extra: { width: number, height: number }): void

    get width() { return this.canvas.width / window.devicePixelRatio }
    get height() { return this.canvas.height / window.devicePixelRatio }

    setCanvasSize() {
        const ratio = window.devicePixelRatio
        this.canvas.height = this.container.clientHeight * ratio;
        this.canvas.width = this.container.clientWidth * ratio;
        this.canvasViewRedraw()
    }
}
