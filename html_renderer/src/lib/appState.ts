import { writable } from 'svelte/store'
import type Group from './model/Group'

export const visibleGroups = writable<{[id: string]: boolean}>({})
export const timeFormat = writable<'absolute'|'proportion'>('absolute')
