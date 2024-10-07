export default class DevicePixelRatioObserver {
    mediaQueryList: MediaQueryList | null = null

    constructor(readonly onDevicePixelRatioChanged: () => void) {
        this._onChange = this._onChange.bind(this)
        this.createMediaQueryList()
    }

    createMediaQueryList() {
        this.removeMediaQueryList()
        let mqString = `(resolution: ${window.devicePixelRatio}dppx)`;

        this.mediaQueryList = matchMedia(mqString);
        this.mediaQueryList.addEventListener('change', this._onChange)
    }
    removeMediaQueryList() {
        this.mediaQueryList?.removeEventListener('change', this._onChange)
        this.mediaQueryList = null
    }
    _onChange(event: MediaQueryListEvent) {
        this.onDevicePixelRatioChanged()
        this.createMediaQueryList()
    }
    destroy() {
        this.removeMediaQueryList()
    }
}
