import { describe, expect, it, vi } from 'vitest'
import Frame from '../lib/model/Frame'
import TimelineCanvasView from './TimelineCanvasView'

const context = {shortenPath: (path: string) => path, sysPrefixes: ['/lib'], precision: 3}

function makeRoot() {
    return new Frame({
        identifier: '<module>\x00/demo.py\x001', time: 1,
        children: [
            {identifier: 'read\x00/demo.py\x002', time: 0.3},
            {identifier: 'read\x00/lib/io.py\x003', time: 0.3},
            {identifier: 'fetch\x00/demo.py\x004', attributes: {cClient: 0.2}, time: 0.2},
            {identifier: 'parse[one]\x00/demo.py\x005', time: 0.1},
            {identifier: '[self]', time: 0.1},
        ],
    }, context)
}

function makeView() {
    // Exercise the canvas controller without requiring browser layout in unit tests.
    const view = Object.create(TimelineCanvasView.prototype) as TimelineCanvasView
    Object.defineProperty(view, 'width', {value: 800})
    view.searchQuery = ''
    view.matchingFrames = new Set()
    view.setNeedsRedraw = vi.fn()
    view.setRootFrame(makeRoot())
    return view
}

describe('timeline search', () => {
    it('finds every occurrence, including library frames, without changing the viewport', () => {
        const view = makeView()
        view.zoom = 2000
        view.startT = 0.25
        view.yOffset = 40
        const frames = view.frames.slice()
        expect(view.setSearchQuery(' READ ')).toBe(2)
        expect([...view.matchingFrames].map(f => f.isApplicationCode)).toEqual([true, false])
        expect([view.zoom, view.startT, view.yOffset]).toEqual([2000, 0.25, 40])
        expect(view.frames).toEqual(frames)
        expect(view.setNeedsRedraw).toHaveBeenCalled()
    })

    it('searches displayed class and module names and treats punctuation literally', () => {
        const view = makeView()
        expect(view.setSearchQuery('client.fetch')).toBe(1)
        expect(view.setSearchQuery('demo.py')).toBe(1)
        expect(view.setSearchQuery('[one]')).toBe(1)
        expect(view.setSearchQuery('.*')).toBe(0)
        expect(view.setSearchQuery('[self]')).toBe(0)
    })

    it('clears highlights for empty queries and queries with no matches', () => {
        const view = makeView()
        expect(view.setSearchQuery('read')).toBe(2)
        expect(view.setSearchQuery('missing')).toBe(0)
        expect(view.matchingFrames.size).toBe(0)
        expect(view.setSearchQuery('read')).toBe(2)
        expect(view.setSearchQuery(' \t ')).toBe(0)
        expect(view.searchQuery).toBe('')
    })

    it('recomputes matches when the displayed frame tree changes', () => {
        const view = makeView()
        view.setSearchQuery('read')
        const oldMatches = [...view.matchingFrames]
        view.setRootFrame(new Frame({identifier: 'read\x00/other.py\x001', time: 1}, context))
        expect(view.matchingFrames.size).toBe(1)
        expect([...view.matchingFrames].some(f => oldMatches.includes(f))).toBe(false)
        view.setRootFrame(new Frame({identifier: 'other\x00/other.py\x001', time: 1}, context))
        expect(view.matchingFrames.size).toBe(0)
    })

    it.each([1, 120])('highlights matching bars and restores original colors at width %s', (width) => {
        const view = makeView()
        view.frameDims = () => ({x: 0, y: 0, w: width, h: 17})
        view.colorForFrame = () => '#123456'
        const paints: [string, number][] = []
        const ctxStub = {
            fillStyle: '', globalAlpha: 1,
            fill() { paints.push([this.fillStyle, this.globalAlpha]) },
            fillRect() { this.fill() },
            save() {}, restore() {}, beginPath() {}, rect() {}, clip() {}, fillText() {},
        }
        const ctx = ctxStub as unknown as CanvasRenderingContext2D

        const libraryFrame = view.frames[2]
        view.setSearchQuery('read')
        view.drawFrame(ctx, libraryFrame)
        view.drawFrame(ctx, view.frames[0])
        view.setSearchQuery('')
        view.drawFrame(ctx, libraryFrame)
        expect(paints).toEqual([
            ['#cf35e8', 1], ['#123456', 0.18], ['#123456', 0.5],
        ])
    })
})
