import { defineConfig } from "vitest/config";

export default defineConfig({
  base: "/map-constructor-converter/",
  define: {
    "import.meta.vitest": "undefined",
  },
  test: {
    globals: true,
    includeSource: ["src/**/*.{js,ts}"],
  },
});
