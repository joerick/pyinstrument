import { deleteFrameFromTree } from "./frameOps";
import { describe, it, expect } from "vitest";
import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "./Frame";

const context = {shortenPath: (a:string) => a};

describe("deleteFrameFromTree", () => {
  it("should replace the frame with its children", () => {
    const parent = new Frame({ identifier: "parent" }, context);
    const frame = new Frame({ identifier: "frame" }, context);
    const child1 = new Frame({ identifier: "child1" }, context);
    const child2 = new Frame({ identifier: "child2" }, context);
    frame.addChild(child1);
    frame.addChild(child2);
    parent.addChild(frame);

    deleteFrameFromTree(frame, { replaceWith: "children" });

    expect(parent.children).toContain(child1);
    expect(parent.children).toContain(child2);
    expect(parent.children).not.toContain(frame);
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
