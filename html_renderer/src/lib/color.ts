export function colorForFrameProportionOfTotal(proportion: number): string {
    if (proportion > 0.6) {
        return '#FF4159'
    } else if (proportion > 0.3) {
        return '#F5A623'
    } else if (proportion > 0.2) {
        return '#D8CB2A'
    } else {
        return '#7ED321'
    }
}
