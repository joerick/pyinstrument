import { persisted } from "svelte-persisted-store"

export interface ViewOptionsCallStack {
    collapseMode: 'non-application'|'disabled'|'custom'
    collapseCustomHide: string
    collapseCustomShow: string
    removeImportlib: boolean
    removeTracebackHide: boolean
    removePyinstrument: boolean
    removeIrrelevant: boolean
    removeIrrelevantThreshold: number
    timeFormat: 'absolute'|'proportion'
}

export function CallStackViewOptionsDefaults(): ViewOptionsCallStack {
    return {
        collapseMode: 'non-application',
        collapseCustomHide: '',
        collapseCustomShow: '',
        removeImportlib: true,
        removeTracebackHide: true,
        removePyinstrument: true,
        removeIrrelevant: true,
        removeIrrelevantThreshold: 0.001,
        timeFormat: 'absolute',
    }
}

export const viewOptionsCallStack = persisted<ViewOptionsCallStack>(
    'pyinstrument:viewOptionsCallStack',
    CallStackViewOptionsDefaults(),
    {
        syncTabs: true,
        beforeRead(val) {
            // fill in any missing values with defaults
            return {
                ...CallStackViewOptionsDefaults(),
                ...val
            }
        }
    }
)
export const viewOptions = persisted(
    'pyinstrument:viewOptions',
    {viewMode: 'call-stack' as 'call-stack'|'timeline'},
    {syncTabs: false}
)

export interface ViewOptionsTimeline {
    removeImportlib: boolean,
    removeTracebackHide: boolean,
    removePyinstrument: boolean,
    removeIrrelevant: boolean,
    removeIrrelevantThreshold: number,
}
export const viewOptionsTimeline = persisted<ViewOptionsTimeline>(
    'pyinstrument:viewOptionsTimeline',
    {
        removeImportlib: true,
        removeTracebackHide: true,
        removePyinstrument: true,
        removeIrrelevant: true,
        removeIrrelevantThreshold: 0.0001,
    },
    {syncTabs: true}
)
