
export class UnreachableCaseError extends Error {
    constructor(value: never) {
        super(`Unreachable case: ${value}`)
    }
}

export function sampleGradient(gradient: number[][], location: number) {
    const index = location * (gradient.length - 1)
    const lowerIndex = Math.floor(index)
    const upperIndex = Math.ceil(index)
    const lowerColor = gradient[lowerIndex]
    const upperColor = gradient[upperIndex]
    const ratio = index - lowerIndex
    return mapRGBColor(ratio, { to: [lowerColor, upperColor] })
}

export function clamp(value: number, min: number, max: number): number {
    if (value === Infinity) {
        console.warn('clamp: value is Infinity, returning `max`', value);
        return max;
    }
    if (value === -Infinity) {
        console.warn('clamp: value is -Infinity, returning `min`', value);
        return min;
    }
    if (!Number.isFinite(value)) {
        console.warn('clamp: value isn\'t finite, returning `min`', value);
        return min
    }

    if (value < min) return min;
    if (value > max) return max;
    return value;
}

export function map(x: number, options: {
    from?: [number, number],
    to?: [number, number],
    clamp?: boolean
}): number {
    const { from = [0, 1], to = [0, 1] } = options;
    const shouldClamp = options.clamp || false;

    let result = (x - from[0]) / (from[1] - from[0]) * (to[1] - to[0]) + to[0]
    if (shouldClamp) {
        result = clamp(result, Math.min(to[0], to[1]), Math.max(to[0], to[1]));
    }

    return result;
}

export function mapRGBColor(x: number, options: {
    from?: [number, number],
    to: [number[], number[]],
    clamp?: boolean
}): string {
    return `rgb(
      ${map(x, { from: options.from, to: [options.to[0][0], options.to[1][0]], clamp: options.clamp })},
      ${map(x, { from: options.from, to: [options.to[0][1], options.to[1][1]], clamp: options.clamp })},
      ${map(x, { from: options.from, to: [options.to[0][2], options.to[1][2]], clamp: options.clamp })}
    )`
}

export function mapColor(x: number, options: {
    from?: [number, number],
    to: [string, string],
    clamp?: boolean
}): string {
    return mapRGBColor(x, {
        from: options.from,
        to: [parseColor(options.to[0]), parseColor(options.to[1])],
        clamp: options.clamp
    })
}

/**
 * @returns  A color string in the format "rgb(r, g, b)", where r, g, and b
 * are integers in the range [0, 255].
 */
export function parseColor(input: string) {
    if (input.substr(0, 1) == "#") {
        var collen = (input.length - 1) / 3;
        var fact = [17, 1, 0.062272][collen - 1];
        return [
            Math.round(parseInt(input.substr(1, collen), 16) * fact),
            Math.round(parseInt(input.substr(1 + collen, collen), 16) * fact),
            Math.round(parseInt(input.substr(1 + 2 * collen, collen), 16) * fact)
        ];
    }
    else return input.split("(")[1].split(")")[0].split(",").map(x => +x);
}

/**
 * returns a hash of the string, as an integer with 2^53 possible values.
 */
export function cyrb53(str: string, seed: number = 0) {
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for(let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1  = Math.imul(h1 ^ (h1 >>> 16), 2246822507);
    h1 ^= Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2  = Math.imul(h2 ^ (h2 >>> 16), 2246822507);
    h2 ^= Math.imul(h1 ^ (h1 >>> 13), 3266489909);

    return 4294967296 * (2097151 & h2) + (h1 >>> 0);
};

export function hash(str: string) {
    return cyrb53(str, 21) / 2**53;
}
