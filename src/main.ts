import { fromGeojson, toGeojson } from "./lib";
import "./style.css";

async function readFile(file: File): Promise<string> {
  return await new Promise((resolve) => {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
      resolve(reader.result as string);
    });
    reader.readAsText(file);
  });
}

async function downloadBlob(blob: Blob, filename: string): Promise<void> {
  return await new Promise((resolve) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.addEventListener(
      "click",
      () =>
        setTimeout(() => {
          URL.revokeObjectURL(url);
          resolve();
        }, 150),
      false,
    );
    a.click();
  });
}

async function to(file: File): Promise<void> {
  const routes = await readFile(file);
  const geoJson = await toGeojson(
    routes,
    import.meta.env.VITE_YANDEX_GEODECODE_API_KEY,
  );
  const blob = new Blob([geoJson], { type: "application/geo+json" });
  const name = `${new Date().toJSON()}.geojson`;
  await downloadBlob(blob, name);
}

async function from_(file: File): Promise<void> {
  const routes = await readFile(file);
  const geoJson = fromGeojson(routes);
  const blob = new Blob([geoJson], { type: "text/plain" });
  const name = `${new Date().toJSON()}.txt`;
  await downloadBlob(blob, name);
}

function withShowingError(promise: Promise<void>): void {
  const el = document.getElementById("error") as HTMLElement;
  el.innerHTML = "";

  promise.catch((reason) => {
    el.innerHTML = reason;
  });
}

{
  const el = document.getElementById("routes-to-geojson") as HTMLInputElement;
  el.addEventListener("change", () => {
    if (el.files != null) withShowingError(to(el.files[0]));
  });
}

{
  const el = document.getElementById("geojson-to-routes") as HTMLInputElement;
  el.addEventListener("change", () => {
    if (el.files != null) withShowingError(from_(el.files[0]));
  });
}

