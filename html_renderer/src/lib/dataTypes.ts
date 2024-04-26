export interface SessionData {
    session: {
        start_time: number;
        duration: number;
        sample_count: number;
        start_call_stack: string[],
        program: string;
        cpu_time: number;
        sys_path: string;
    };
    frame_tree: FrameData;
}

export interface FrameData {
    identifier: string;
    time: number;
    attributes: {[name: string]: number};
    children: FrameData[];
}
