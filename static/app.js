const input = document.querySelector("#file-input");
const dropzone = document.querySelector("#dropzone");
const fileList = document.querySelector("#file-list");
const fileCount = document.querySelector("#file-count");
const summaryCount = document.querySelector("#summary-count");
const summarySize = document.querySelector("#summary-size");
const mergeButton = document.querySelector("#merge-button");
const buttonHint = document.querySelector(".button-hint");
const errorMessage = document.querySelector("#error-message");
const progress = document.querySelector("#progress");

let files = [];
let draggedIndex = null;

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function renderFiles() {
  fileList.replaceChildren();
  if (!files.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.innerHTML = '<span class="empty-rule"></span><p>รายการของคุณจะปรากฏตรงนี้</p>';
    fileList.append(empty);
  }

  files.forEach((file, index) => {
    const row = document.createElement("div");
    row.className = "file-row";
    row.draggable = true;
    row.addEventListener("dragstart", () => { draggedIndex = index; });
    row.addEventListener("dragover", (event) => event.preventDefault());
    row.addEventListener("drop", (event) => {
      event.preventDefault();
      if (draggedIndex === null || draggedIndex === index) return;
      const [moved] = files.splice(draggedIndex, 1);
      files.splice(index, 0, moved);
      draggedIndex = null;
      renderFiles();
    });

    const mark = document.createElement("span");
    mark.className = "pdf-mark";
    mark.textContent = "PDF";
    mark.setAttribute("aria-hidden", "true");

    const info = document.createElement("div");
    info.className = "file-info";
    const name = document.createElement("div");
    name.className = "file-name";
    name.textContent = file.name;
    name.title = file.name;
    const size = document.createElement("div");
    size.className = "file-size";
    size.textContent = formatSize(file.size);
    info.append(name, size);

    const actions = document.createElement("div");
    actions.className = "row-actions";
    actions.append(
      makeAction("↑", "เลื่อนขึ้น", index === 0, () => moveFile(index, -1)),
      makeAction("↓", "เลื่อนลง", index === files.length - 1, () => moveFile(index, 1)),
      makeAction("×", "นำไฟล์ออก", false, () => {
        files.splice(index, 1);
        renderFiles();
      }, true),
    );
    row.append(mark, info, actions);
    fileList.append(row);
  });

  const totalBytes = files.reduce((total, file) => total + file.size, 0);
  fileCount.textContent = `${files.length} ไฟล์`;
  summaryCount.textContent = String(files.length);
  summarySize.textContent = totalBytes ? formatSize(totalBytes) : "0 KB";
  mergeButton.disabled = files.length < 2;
  buttonHint.hidden = files.length >= 2;
  buttonHint.textContent = files.length >= 2
    ? "พร้อมดาวน์โหลดหลังรวมไฟล์"
    : "เลือกอย่างน้อย 2 ไฟล์เพื่อเริ่ม";
}

function makeAction(symbol, label, disabled, action, remove = false) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `icon-button${remove ? " remove" : ""}`;
  button.textContent = symbol;
  button.title = label;
  button.setAttribute("aria-label", label);
  button.disabled = disabled;
  button.addEventListener("click", action);
  return button;
}

function moveFile(index, offset) {
  const target = index + offset;
  if (target < 0 || target >= files.length) return;
  [files[index], files[target]] = [files[target], files[index]];
  renderFiles();
}

function addFiles(selected) {
  const pdfs = [...selected].filter((file) => file.name.toLowerCase().endsWith(".pdf"));
  const rejected = selected.length - pdfs.length;
  files.push(...pdfs);
  errorMessage.hidden = !rejected;
  errorMessage.textContent = rejected ? "ข้ามไฟล์ที่ไม่ใช่ PDF แล้ว" : "";
  renderFiles();
}

input.addEventListener("change", () => {
  addFiles(input.files);
  input.value = "";
});

for (const eventName of ["dragenter", "dragover"]) {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("is-over");
  });
}
for (const eventName of ["dragleave", "drop"]) {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove("is-over");
  });
}
dropzone.addEventListener("drop", (event) => addFiles(event.dataTransfer.files));

mergeButton.addEventListener("click", async () => {
  if (files.length < 2) return;
  errorMessage.hidden = true;
  mergeButton.disabled = true;
  progress.hidden = false;
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file, file.name));

  try {
    const response = await fetch("/merge", { method: "POST", body: formData });
    if (!response.ok) {
      const result = await response.json();
      throw new Error(result.error || "เกิดข้อผิดพลาดในการรวมไฟล์");
    }
    const url = URL.createObjectURL(await response.blob());
    const link = document.createElement("a");
    link.href = url;
    link.download = "merged.pdf";
    link.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    errorMessage.textContent = error.message || "ไม่สามารถรวมไฟล์ได้ โปรดลองอีกครั้ง";
    errorMessage.hidden = false;
  } finally {
    progress.hidden = true;
    mergeButton.disabled = files.length < 2;
  }
});

renderFiles();