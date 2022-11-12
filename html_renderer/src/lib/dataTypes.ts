export interface SessionData {
    start_time: number;
    duration: number;
    sample_count: number;
    program: string;
    cpu_time: number | null;
    root_frame: FrameData | null;
}

export interface FrameData {
    function: string;
    file_path: string;
    file_path_short: string;
    line_no: number;
    time: number;
    await_time: number;
    is_application_code: boolean;
    children: FrameData[];
    group_id?: string;
    class_name?: string;
}
