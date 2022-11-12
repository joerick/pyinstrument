import Group from './Group';
import type {FrameData} from '../dataTypes';

export default class Frame {
  function: string;
  filePath: string;
  filePathShort: string;
  lineNo: number;
  time: number;
  totalTime: number;
  awaitTime: number;
  isApplicationCode: boolean;
  groupId: string | null;
  className: string | null;

  parent: Frame | null;
  children: Frame[];

  group: Group | null;

  constructor(jsonObject: FrameData, parent: Frame|null = null, context: FrameContext = {groups:{}}) {
    this.parent = parent
    this.function = jsonObject.function;
    this.filePath = jsonObject.file_path;
    this.filePathShort = jsonObject.file_path_short;
    this.lineNo = jsonObject.line_no;
    this.time = jsonObject.time;
    this.totalTime = this.parent ? this.parent.totalTime : this.time;
    this.awaitTime = jsonObject.await_time;
    this.isApplicationCode = jsonObject.is_application_code;
    this.groupId = jsonObject.group_id ?? null;
    this.className = jsonObject.class_name ?? null;

    if (jsonObject.group_id) {
      const groupId = jsonObject.group_id;
      let group = context.groups[groupId]
      if (!group) {
        group = context.groups[groupId] = new Group(groupId, this);
      }
      group.addFrame(this);
      this.group = context.groups[groupId];
    } else {
      this.group = null;
    }

    this.children = jsonObject.children.map(f => new Frame(f, this, context));
  }

  get identifier() {
    return `${this.function}:${this.filePath}:${this.lineNo}`;
  }

  get proportionOfTotal() {
    return this.time / this.totalTime;
  }
}

interface FrameContext {
  groups: {[id: string]: Group};
}
