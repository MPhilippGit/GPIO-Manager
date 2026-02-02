import { defineConfig } from "vite";
import react from '@vitejs/plugin-react';
import path from "path";

export default defineConfig({
   base: "/static/",
   plugins: [react()],
   root: ".", // kein eigenes Root, da du index.html nicht nutzt
   build: {
      manifest: "manifest.json",
      outDir: path.resolve(__dirname, './static'),
      emptyOutDir: true,
      rollupOptions: {
         input: path.resolve(__dirname, "frontend/index.js"),
         output: {
            entryFileNames: "assets/[name]-bundle.js",
            assetFileNames: "assets/[name].[ext]",
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
