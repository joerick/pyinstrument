import type { SessionData } from "../dataTypes";
import Frame from "./Frame";

export default class Session {
    startTime: number;
    duration: number;
    minInterval: number;
    maxInterval: number;
    sampleCount: number;
    target_description: string;
    cpuTime: number;
    rootFrame: Frame;
    sysPath: string;
    sysPrefixes: string[];

    constructor(data: SessionData) {
        this.startTime = data.session.start_time;
        this.duration = data.session.duration;
        this.minInterval = data.session.min_interval;
        this.maxInterval = data.session.max_interval;
        this.sampleCount = data.session.sample_count;
        this.target_description = data.session.target_description;
        this.cpuTime = data.session.cpu_time;
        this.sysPath = data.session.sys_path;
        this.sysPrefixes = data.session.sys_prefixes
        this.rootFrame = new Frame(data.frame_tree, this)
    }

    _shortenPathCache: {[path: string]: string} = {}
    shortenPath(path: string): string {
        if (this._shortenPathCache[path]) {
            return this._shortenPathCache[path]
        }

        let result = path
        const pathParts = pathSplit(path)

        if (pathParts.length > 1) {
            for (const sysPathEntry of this.sysPath) {
                const candidate = getRelPath(path, sysPathEntry)
                if (pathSplit(candidate).length < pathSplit(result).length) {
                    result = candidate
                }
            }
        }

        this._shortenPathCache[path] = result
        return result
    }
}

function pathSplit(path: string): string[] {
    return path.split(/[/\\]/)
}

function getPathDrive(path: string): string | null {
    const parts = pathSplit(path)
    if (parts.length > 0 && parts[0].endsWith(":")) {
        return parts[0]
    } else {
        return null
    }
}

function getRelPath(path: string, start: string): string {
    // returns the relative path from start to path
    // e.g. getRelPath("/a/b/c", "/a") -> "b/c"
    // e.g. getRelPath("/a/b/c", "/a/d/e") -> "../../b/c"

    if (getPathDrive(path) != getPathDrive(start)) {
        // different drives, can't make a relative path
        return path
    }

    const parts = pathSplit(path)
    const startParts = pathSplit(start)
    let i = 0
    while (i < parts.length && i < startParts.length && parts[i] == startParts[i]) {
        i++
    }
    const relParts = startParts.slice(i).map(_ => "..")

    return relParts.concat(parts.slice(i)).join("/")
}
