export default class Group {
  frames = []

  constructor(id, rootFrame) {
    this.id = id;
    this.rootFrame = rootFrame;
  }

  addFrame(frame) {
    this.frames.push(frame);
  }

  get exitFrames() {
    // exit frames are frames inside this group that have children outside the group.
    const exitFrames = []

    for (const frame of this.frames) {
      let isExit = false;
      for (const child of frame.children) {
        if (child.group != this) {
          isExit = true;
          break;
        }
      }

      if (isExit) {
        exitFrames.push(frame);
      }
    }

    return exitFrames;
  }

  get libraries() {
    const libraries = [];

    for (const frame of this.frames) {
      const library = /^[^\\/.]*/.exec(frame.filePathShort)[0]
      if (!libraries.includes(library)) {
        libraries.push(library);
      }
    }

    return libraries;
  }
}
