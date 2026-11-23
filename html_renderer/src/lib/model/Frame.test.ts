import { describe, it, expect } from "vitest";
import Frame, { pathIsInside } from "./Frame";

function makeFrame(filePath: string, sysPrefixes: string[]) {
    const context = {
        shortenPath: (a: string) => a,
        sysPrefixes,
        precision: 3,
    };
    return new Frame({ identifier: `work\x00${filePath}\x001` }, context);
}

describe("Frame.isApplicationCode", () => {
    it("classifies files inside a sys_prefix as library", () => {
        const frame = makeFrame(
            "/tmp/env/lib/python3.12/site-packages/foo.py",
            ["/tmp/env"],
        );
        expect(frame.isApplicationCode).toBe(false);
    });

    it("classifies unrelated files as application", () => {
        const frame = makeFrame("/home/user/project/main.py", ["/tmp/env"]);
        expect(frame.isApplicationCode).toBe(true);
    });

    it("classifies a sibling directory as application (regression)", () => {
        // Plain-prefix matching would treat /tmp/env-project as inside
        // /tmp/env. It is not.
        const frame = makeFrame("/tmp/env-project/main.py", ["/tmp/env"]);
        expect(frame.isApplicationCode).toBe(true);
    });

    it("respects a trailing-slash sys_prefix for inside paths", () => {
        const frame = makeFrame("/tmp/env/lib/foo.py", ["/tmp/env/"]);
        expect(frame.isApplicationCode).toBe(false);
    });

    it("respects a trailing-slash sys_prefix for sibling paths", () => {
        const frame = makeFrame("/tmp/env-project/main.py", ["/tmp/env/"]);
        expect(frame.isApplicationCode).toBe(true);
    });

    it("treats a path equal to the prefix as library", () => {
        const frame = makeFrame("/tmp/env", ["/tmp/env"]);
        expect(frame.isApplicationCode).toBe(false);
    });

    it("handles Windows-style separators inside a prefix", () => {
        const frame = makeFrame("C:\\env\\Lib\\foo.py", ["C:\\env"]);
        expect(frame.isApplicationCode).toBe(false);
    });

    it("handles Windows-style separators for a sibling", () => {
        // Windows-shaped paths come up for profiles saved on Windows and
        // rendered elsewhere.
        const frame = makeFrame("C:\\env-project\\main.py", ["C:\\env"]);
        expect(frame.isApplicationCode).toBe(true);
    });

    it("accepts cross-OS separators after a prefix", () => {
        const frame = makeFrame("/tmp/env\\lib\\foo.py", ["/tmp/env"]);
        expect(frame.isApplicationCode).toBe(false);
    });
});

describe("pathIsInside", () => {
    it("matches a file inside the directory", () => {
        expect(pathIsInside("/tmp/env/lib/foo.py", "/tmp/env")).toBe(true);
    });

    it("matches an exact-equal path", () => {
        expect(pathIsInside("/tmp/env", "/tmp/env")).toBe(true);
    });

    it("rejects a sibling with a matching name prefix", () => {
        expect(pathIsInside("/tmp/env-project/main.py", "/tmp/env")).toBe(false);
    });

    it("rejects an unrelated path", () => {
        expect(pathIsInside("/home/user/main.py", "/tmp/env")).toBe(false);
    });

    it("respects trailing-slash directories", () => {
        expect(pathIsInside("/tmp/env/lib/foo.py", "/tmp/env/")).toBe(true);
        expect(pathIsInside("/tmp/env-project/main.py", "/tmp/env/")).toBe(
            false,
        );
    });
});
