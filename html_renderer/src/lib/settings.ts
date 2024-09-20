import { persisted } from "svelte-persisted-store"

export interface ViewOptionsCallStack {
    collapseMode: 'non-application'|'disabled'|'custom'
    collapseCustomHide: string
    collapseCustomShow: string
    hideImportlib: boolean
    hideTracebackHide: boolean
    hidePyinstrument: boolean
    hideIrrelevant: boolean
    hideIrrelevantThreshold: number
    timeFormat: 'absolute'|'proportion'
}

export function CallStackViewOptionsDefaults(): ViewOptionsCallStack {
    return {
        collapseMode: 'non-application',
        collapseCustomHide: '',
        collapseCustomShow: '',
        hideImportlib: true,
        hideTracebackHide: true,
        hidePyinstrument: true,
        hideIrrelevant: true,
        hideIrrelevantThreshold: 0.001,
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
    hideImportlib: boolean,
    hideTracebackHide: boolean,
    hidePyinstrument: boolean,
    hideIrrelevant: boolean,
    hideIrrelevantThreshold: number,
}
export const viewOptionsTimeline = persisted<ViewOptionsTimeline>(
    'pyinstrument:viewOptionsTimeline',
    {
        hideImportlib: true,
        hideTracebackHide: true,
        hidePyinstrument: true,
        hideIrrelevant: true,
        hideIrrelevantThreshold: 0.0001,
    },
    {syncTabs: true}
)
