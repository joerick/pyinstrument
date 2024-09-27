
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

interface OnClickOutsideOptions {
  ignore?: (HTMLElement | string)[];
  capture?: boolean;
}

type OnClickOutsideHandler = (evt: MouseEvent) => void;

/**
 * Listen for clicks outside of an element.
 *
 * Translated from
 * https://github.com/vueuse/vueuse/blob/798077d678a2a8cd50cc3c3b85a722befb6087d4/packages/core/onClickOutside/index.ts
 * License: MIT
 * https://github.com/vueuse/vueuse/blob/798077d678a2a8cd50cc3c3b85a722befb6087d4/LICENSE
 *
 * @param target - The target element to watch for outside clicks.
 * @param handler - The function to call when a click outside the target is detected.
 * @param options - Optional configurations.
 * @returns A cleanup function that removes the event listeners.
 */
export function onClickOutside(
  target: HTMLElement,
  handler: OnClickOutsideHandler,
  options: OnClickOutsideOptions = {}
) {
  const { ignore = [], capture = true } = options;
  const windowObj = window;

  if (!windowObj) return () => {};

  let shouldListen = true;
  let isProcessingClick = false;

  const shouldIgnore = (event: MouseEvent) => {
    return ignore.some((target) => {
      if (typeof target === "string") {
        return Array.from(document.querySelectorAll(target)).some(
          (el) => el === event.target || event.composedPath().includes(el)
        );
      } else {
        return target && (event.target === target || event.composedPath().includes(target));
      }
    });
  };

  const listener = (event: MouseEvent) => {
    if (!target || target === event.target || event.composedPath().includes(target)) return;

    if (event.detail === 0) shouldListen = !shouldIgnore(event);

    if (!shouldListen) {
      shouldListen = true;
      return;
    }

    handler(event);
  };

  const clickListener = (event: MouseEvent) => {
    if (!isProcessingClick) {
      isProcessingClick = true;
      setTimeout(() => {
        isProcessingClick = false;
      }, 0);
      listener(event);
    }
  };

  const pointerDownListener = (event: PointerEvent) => {
    shouldListen = !shouldIgnore(event) && !!(target && !event.composedPath().includes(target));
  };

  windowObj.addEventListener("click", clickListener, { passive: true, capture });
  windowObj.addEventListener("pointerdown", pointerDownListener, { passive: true });

  const stop = () => {
    windowObj.removeEventListener("click", clickListener, { capture });
    windowObj.removeEventListener("pointerdown", pointerDownListener);
  };

  return stop;
}

export function escapeForHtml(str: string) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

export function htmlForStringWithWBRAtSlashes(str: string) {
    let result = escapeForHtml(str);
    return result.replace(/(\/|\\)/g, s => `${s}<wbr>`);
}

export function maxBy<T>(list: readonly T[], keyFunc: (a:T) => number): T|null {
    if (list.length == 0) return null

    let maxResult = list[0]
    let maxResultScore = keyFunc(maxResult)

    for (const el of list) {
        const elScore = keyFunc(el)
        if (elScore > maxResultScore) {
            maxResult = el
            maxResultScore = elScore
        }
    }

    return maxResult
}

/**
 * Provides 56 bits of randomness as a neat 11-character string.
 */
export function randomId() {
    return Math.random().toString(36).substring(2);
}
