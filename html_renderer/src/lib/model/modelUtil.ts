import type Frame from "./Frame"
import type { Processor, ProcessorFunction, ProcessorOptions } from "./processors"

export function applyProcessors(rootFrame: Frame, processors: ProcessorFunction[], options: ProcessorOptions) {
    let frame: Frame | null = rootFrame
    for (const processor of processors) {
        frame = processor(frame, options)
        if (!frame) {
            return null
        }
    }
    return frame
}
