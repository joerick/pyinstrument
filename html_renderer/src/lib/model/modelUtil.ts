import type Frame from "./Frame"
import type { Processor, ProcessorFunction, ProcessorOptions } from "./processors"

export function applyProcessors(rootFrames: Frame[] | null,
                                processors: ProcessorFunction[], options: ProcessorOptions) {
    let frames: Frame[] | null = rootFrames
    if (frames != null) {
        for (const thread_id of Object.keys(rootFrames)) {
            let frame = rootFrames[thread_id]
            for (const processor of processors) {
                frame = processor(frame, options)
                if (!frame) {
                    delete frames[thread_id]
                    break
                }
            }
            frames[thread_id] = frame
        }
    }
    return frames
}
