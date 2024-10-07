import { writable } from 'svelte/store'

export const visibleGroups = writable<{[id: string]: boolean}>({})
export const collapsedFrames = writable<{[id: string]: boolean}>({})
