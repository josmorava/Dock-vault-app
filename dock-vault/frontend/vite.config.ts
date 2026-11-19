import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
  },
  build: {
    outDir: "../backend/static/assets",
    manifest: true,
    rollupOptions: {
      input: "src/main.ts",
    },
  },
});
