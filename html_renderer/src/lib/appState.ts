import { writable } from 'svelte/store'
import type FrameGroup from './model/FrameGroup'

export const visibleGroups = writable<{[id: string]: boolean}>({})
export const timeFormat = writable<'absolute'|'proportion'>('absolute')
