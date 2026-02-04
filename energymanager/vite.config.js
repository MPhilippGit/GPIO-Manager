import { defineConfig } from "vite";
import react from '@vitejs/plugin-react';
import path from "path";

export default defineConfig({
   base: "/static/",
   plugins: [react()],
   root: ".",
   build: {
      manifest: "manifest.json",
      outDir: path.resolve(__dirname, './static'),
      emptyOutDir: true,
      rollupOptions: {
         input: path.resolve(__dirname, "frontend/main.jsx"),
         output: {
            entryFileNames: "frontend/[name]-bundle.js",
            assetFileNames: "frontend/[name].[ext]",
         },
      },
   },
   css: {
      preprocessorOptions: {
         scss: {
            silenceDeprecations: [
               'import',
               'mixed-decls',
               'color-functions',
               'global-builtin',
            ],
         },
      },
   },
});
