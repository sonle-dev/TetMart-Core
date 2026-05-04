(() => {
  const input = document.getElementById("productImages");
  const dropzone = document.getElementById("uploadDropzone");
  const errorBox = document.getElementById("uploadError");
  const previewGrid = document.getElementById("previewGrid");

  if (!input || !dropzone || !errorBox || !previewGrid) return;

  const MAX_FILES = 5;
  const MAX_SIZE = 2 * 1024 * 1024; // 2MB
  const ALLOWED_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);

  let selectedFiles = [];

  const showError = (msg) => {
    errorBox.textContent = msg;
    errorBox.classList.remove("d-none");
  };

  const clearError = () => {
    errorBox.textContent = "";
    errorBox.classList.add("d-none");
  };

  const formatSize = (bytes) => {
    const mb = bytes / (1024 * 1024);
    return mb >= 1 ? `${mb.toFixed(2)} MB` : `${(bytes / 1024).toFixed(0)} KB`;
  };

  const syncInputFiles = () => {
    const dt = new DataTransfer();
    selectedFiles.forEach((f) => dt.items.add(f));
    input.files = dt.files;
  };

  const renderPreviews = () => {
    previewGrid.innerHTML = "";
    selectedFiles.forEach((file, idx) => {
      const col = document.createElement("div");
      col.className = "col-6 col-md-4 col-lg-3 preview-item";

      const img = document.createElement("img");
      img.className = "preview-img";
      img.alt = file.name;
      img.src = URL.createObjectURL(file);
      img.onload = () => URL.revokeObjectURL(img.src);

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "preview-remove";
      btn.innerHTML = "&times;";
      btn.title = "Xóa ảnh";
      btn.addEventListener("click", () => {
        selectedFiles.splice(idx, 1);
        syncInputFiles();
        renderPreviews();
      });

      const meta = document.createElement("div");
      meta.className = "preview-meta";
      meta.textContent = `${file.name} • ${formatSize(file.size)}`;

      col.appendChild(img);
      col.appendChild(btn);
      col.appendChild(meta);
      previewGrid.appendChild(col);
    });
  };

  const validateAndAddFiles = (files) => {
    clearError();
    const incoming = Array.from(files || []);
    if (incoming.length === 0) return;

    let merged = [...selectedFiles, ...incoming];

    if (merged.length > MAX_FILES) {
      showError(`Chỉ được chọn tối đa ${MAX_FILES} ảnh.`);
      merged = merged.slice(0, MAX_FILES);
    }

    const valid = [];
    for (const file of merged) {
      if (!ALLOWED_TYPES.has(file.type)) {
        showError("Chỉ cho phép ảnh PNG / JPG / WEBP.");
        continue;
      }
      if (file.size > MAX_SIZE) {
        showError("Mỗi ảnh tối đa 2MB. Vui lòng chọn ảnh nhỏ hơn.");
        continue;
      }
      valid.push(file);
    }

    selectedFiles = valid;
    syncInputFiles();
    renderPreviews();
  };

  // click dropzone -> open picker
  dropzone.addEventListener("click", () => input.click());

  // choose
  input.addEventListener("change", (e) => validateAndAddFiles(e.target.files));
})();