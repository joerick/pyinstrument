import type Frame from "./Frame"
import type { Processor, ProcessorOptions } from "./processors"

export function applyProcessors(rootFrame: Frame, processors: Processor[], options: ProcessorOptions) {
    let frame: Frame | null = rootFrame
    for (const processor of processors) {
        frame = processor.function(frame, options)
        if (!frame) {
            return null
        }
    }
    return frame
}
