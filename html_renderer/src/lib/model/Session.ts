import type { SessionData } from "../dataTypes";
import Frame from "./Frame";

export default class Session {
    startTime: number;
    duration: number;
    sampleCount: number;
    program: string;
    cpuTime: number | null;
    rootFrame: Frame | null;

    constructor(data: SessionData) {
        this.startTime = data.start_time;
        this.duration = data.duration;
        this.sampleCount = data.sample_count;
        this.program = data.program;
        this.cpuTime = data.cpu_time;
        this.rootFrame = data.root_frame ? new Frame(data.root_frame) : null;
    }
}
