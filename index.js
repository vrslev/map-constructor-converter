async function readFile(file) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.addEventListener("load", (event) => {
      resolve(event.target.result);
    });
    reader.readAsText(file);
  });
}

function downloadBlob(blob, filename) {
  return new Promise((resolve) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.addEventListener(
      "click",
      () =>
        setTimeout(() => {
          URL.revokeObjectURL(url);
          resolve(a);
        }, 150),
      false
    );
    a.click();
  });
}

document.getElementById("input")?.addEventListener(
  "change",
  async (event) => {
    const file = event.target.files[0];
    const content = await readFile(file);
    const geoJson = await getGeojson(apiKey, content);
    const blob = new Blob([geoJson], { type: "application/geo+json" });
    await downloadBlob(blob, getOutputPath());
  },
  false
);
