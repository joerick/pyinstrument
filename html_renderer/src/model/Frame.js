import Group from './Group';

export default class Frame {
  constructor(jsonObject, parent = null, context = {groups:{}}) {
    this.parent = parent;
    this.function = jsonObject.function;
    this.filePathShort = jsonObject.file_path_short;
    this.filePath = jsonObject.file_path;
    this.lineNo = jsonObject.line_no;
    this.time = jsonObject.time;
    this.totalTime = this.parent ? this.parent.totalTime : this.time;
    this.isApplicationCode = jsonObject.is_application_code
    this.className = jsonObject.class_name;

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

  get proportionOfTotal() {
    return this.time / this.totalTime;
  }
}
