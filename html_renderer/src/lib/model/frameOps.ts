import { UnreachableCaseError } from "../utils";
import Frame from "./Frame";
import { SELF_TIME_FRAME_IDENTIFIER } from "./Frame";

export function deleteFrameFromTree(frame: Frame, options: {replaceWith: 'children'|'self_time'|'nothing'}) {
    const {replaceWith} = options
    const parent = frame.parent
    if (!parent) {
        throw new Error('Cannot delete the root frame')
    }

    if (replaceWith == 'children') {
        parent.addChildren(frame.children, {after: frame})
    } else if (replaceWith == 'self_time') {
        parent.addChild(
            new Frame({
                identifier: SELF_TIME_FRAME_IDENTIFIER,
                time: frame.time,
            }, parent.context),
            {after: frame}
        )
    } else if (replaceWith == 'nothing') {
        parent.absorbedTime += frame.time
    } else {
        throw new UnreachableCaseError(replaceWith)
    }

    frame.removeFromParent()
    removeFrameFromGroups(frame, true)
}

/**
 * Combines two frames into one. The frames must have the same parent.
 *
 * @param frame The frame to remove.
 * @param into The frame to combine into.
 */
export function combineFrames(frame: Frame, into: Frame): void {
    if (frame.parent !== into.parent) {
        throw new Error("Both frames must have the same parent.");
    }

    into.absorbedTime += frame.absorbedTime;
    into.time += frame.time;

    Object.entries(frame.attributes).forEach(([attribute, time]) => {
        if (into.attributes[attribute] !== undefined) {
            into.attributes[attribute] += time;
        } else {
            into.attributes[attribute] = time;
        }
    });

    into.addChildren(frame.children);
    frame.removeFromParent();
    removeFrameFromGroups(frame, false);
}

/**
 * Removes a frame from any groups that it is a member of. Should be used when
 * removing a frame from a tree, so groups don't keep references to removed frames.
 *
 * @param frame The frame to be removed from groups.
 * @param recursive Whether to also remove all child frames from their groups.
 */
export function removeFrameFromGroups(frame: Frame, recursive: boolean): void {
    if (recursive && frame.children) {
        frame.children.forEach(child => {
            removeFrameFromGroups(child, true);
        });
    }

    if (frame.group) {
        const group = frame.group;
        group.removeFrame(frame);

        if (group.frames.length === 1) {
            // A group with only one frame is meaningless; remove it entirely.
            group.removeFrame(group.frames[0]);
        }
    }
}
