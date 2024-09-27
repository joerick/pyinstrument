export interface SessionData {
    session: {
        start_time: number;
        duration: number;
        min_interval: number;
        max_interval: number;
        sample_count: number;
        start_call_stack: string[],
        target_description: string;
        cpu_time: number;
        sys_path: string;
        sys_prefixes: string[];
    };
    frame_tree: FrameData;
}

export interface FrameData {
    identifier: string;
    time: number;
    attributes: {[name: string]: number};
    children: FrameData[];
}
