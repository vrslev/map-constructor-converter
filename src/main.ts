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
      false
    );
    a.click();
  });
}

async function to(file: File): Promise<void> {
  const routes = await readFile(file);
  const geoJson = await toGeojson(routes, import.meta.env.VITE_YANDEX_GEODECODE_API_KEY);
  const blob = new Blob([geoJson], { type: "application/geo+json" });
  const name = `${new Date().toJSON()}.geojson`;
  await downloadBlob(blob, name);
}

async function from_(file: File): Promise<void> {
  const routes = await readFile(file);
  const geoJson = await fromGeojson(routes);
  const blob = new Blob([geoJson], { type: "text/plain" });
  const name = `${new Date().toJSON()}.txt`;
  await downloadBlob(blob, name);
}

{
  const to_el = document.getElementById(
    "routes-to-geojson"
  ) as HTMLInputElement;
  to_el?.addEventListener("change", () => {
    if (to_el.files != null) to(to_el.files[0]);
  });
}

{
  const from_el = document.getElementById(
    "geojson-to-routes"
  ) as HTMLInputElement;
  from_el?.addEventListener("change", () => {
    if (from_el.files != null) from_(from_el.files[0]);
  });
}
