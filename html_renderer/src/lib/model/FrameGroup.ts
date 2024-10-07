import { randomId } from '../utils';
import type Frame from './Frame';

export default class FrameGroup {
    id: string;
    rootFrame: Frame;
    _frames: Frame[] = []

    constructor(rootFrame: Frame) {
        this.id = randomId()
        this.rootFrame = rootFrame;
    }

    addFrame(frame: Frame) {
        if (frame.group) {
            frame.group.removeFrame(frame);
        }
        this._frames.push(frame);
        frame.group = this;
    }

    removeFrame(frame: Frame) {
        if (frame.group !== this) {
            throw new Error("Frame not in group.");
        }

        const index = this._frames.indexOf(frame);
        if (index === -1) {
            throw new Error("Frame not found in group.");
        }
        this._frames.splice(index, 1);
        frame.group = null;
    }

    get frames(): readonly Frame[] {
        return this._frames;
    }

    get exitFrames() {
        // exit frames are frames inside this group that have children outside the group.
        const exitFrames = []

        for (const frame of this.frames) {
            let isExit = false;
            for (const child of frame.children) {
                if (child.group != this) {
                    isExit = true;
                    break;
                }
            }

            if (isExit) {
                exitFrames.push(frame);
            }
        }

        return exitFrames;
    }

    get libraries() {
        const libraries: string[] = [];

        for (const frame of this.frames) {
            const library = frame.library
            if (!library) {
                continue
            }

            if (!libraries.includes(library)) {
                libraries.push(library);
            }
        }

        return libraries;
    }
}
