import { combineRepeatedChildren, deleteFrameFromTree } from "./frameOps";
import { describe, it, expect } from "vitest";
import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "./Frame";
import { remove_importlib, remove_tracebackhide } from "./processors";

const context = {shortenPath: (a:string) => a, sysPrefixes: [], precision: 0.001};

describe("deleteFrameFromTree", () => {
  it("should replace the frame with its children", () => {
    const parent = new Frame({ identifier: "parent" }, context);
    const frame = new Frame({ identifier: "frame" }, context);
    const child1 = new Frame({ identifier: "child1" }, context);
    const child2 = new Frame({ identifier: "child2" }, context);
    const before = new Frame({ identifier: "before" }, context);
    const after = new Frame({ identifier: "after" }, context);
    frame.addChild(child1);
    frame.addChild(child2);
    parent.addChild(before);
    parent.addChild(frame);
    parent.addChild(after);

    deleteFrameFromTree(frame, { replaceWith: "children" });

    expect(parent.children).toEqual([before, child1, child2, after]);
    expect(child1.parent).toBe(parent);
    expect(child2.parent).toBe(parent);
    expect(frame.children).toEqual([]);
    expect(frame.parent).toBeNull();
  });

  it("should add a self-time frame as a replacement", () => {
    const parent = new Frame({ identifier: "parent" }, context);
    const frame = new Frame({ identifier: "frame" }, context);
    parent.addChild(frame);

    deleteFrameFromTree(frame, { replaceWith: "self_time" });

    expect(parent.children).toHaveLength(1);
    expect(parent.children[0].identifier).toBe(SELF_TIME_FRAME_IDENTIFIER);
  });

  it("should absorb the frame's time into the parent", () => {
    const parent = new Frame({ identifier: "parent" }, context);
    const frame = new Frame({ identifier: "frame", time: 10 }, context);
    parent.addChild(frame);

    deleteFrameFromTree(frame, { replaceWith: "nothing" });

    expect(parent.absorbedTime).toBe(10);
  });

  it("should throw an error if trying to delete the root frame", () => {
    const frame = new Frame({ identifier: "frame" }, context);

    expect(() => {
      deleteFrameFromTree(frame, { replaceWith: "children" });
    }).toThrowError("Cannot delete the root frame");
  });
});

describe("removing hidden frames", () => {
  it.each([
    ["importlib", remove_importlib, "load\x00<frozen importlib._bootstrap>\x001", {}],
    ["tracebackhide", remove_tracebackhide, "hidden", {h1: 2}],
  ] as const)("preserves child order and timing when removing %s", (_name, processor, identifier, attributes) => {
    const root = new Frame({
      identifier: "root",
      time: 4,
      children: [
        {identifier: "before", time: 1},
        {identifier, time: 2, attributes, children: [
          {identifier: "first", time: 1},
          {identifier: "second", time: 1},
        ]},
        {identifier: "after", time: 1},
      ],
    }, context);

    processor(root, {});

    expect(root.children.map(frame => frame.identifier)).toEqual(["before", "first", "second", "after"]);
    expect(root.children.map(frame => frame.startTime)).toEqual([0, 1, 2, 3]);
    expect(root.children.every(frame => frame.parent === root)).toBe(true);
  });
});

describe("combineRepeatedChildren", () => {
  it("should combine children with the same identifier into the first", () => {
    const parent = new Frame({ identifier: "parent" }, context);
    const a1 = new Frame({ identifier: "a", time: 1, children: [{ identifier: "x", time: 1 }] }, context);
    const b = new Frame({ identifier: "b", time: 2 }, context);
    const a2 = new Frame({ identifier: "a", time: 3, children: [{ identifier: "y", time: 3 }] }, context);
    parent.addChildren([a1, b, a2]);

    combineRepeatedChildren(parent);

    expect(parent.children).toEqual([a1, b]);
    expect(a1.time).toBe(4);
    expect(a1.children.map(c => c.identifier)).toEqual(["x", "y"]);
    expect(a1.children.every(c => c.parent === a1)).toBe(true);
    expect(a2.parent).toBeNull();
  });
});
