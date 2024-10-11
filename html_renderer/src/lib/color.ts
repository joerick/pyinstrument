export function colorForFrameProportionOfTotal(proportion: number): string {
    if (proportion > 0.6) {
        return '#FF4159'
    } else if (proportion > 0.3) {
        return '#F5A623'
    } else if (proportion > 0.15) {
        return '#D8CB2A'
    } else if (proportion > 0.05) {
        return '#7ED321'
    } else {
        return '#58984f'
    }
}
