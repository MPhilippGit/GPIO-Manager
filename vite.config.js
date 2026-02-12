import { defineConfig } from "vite";

import react from '@vitejs/plugin-react';
import path from "path";

export default defineConfig({
   base: "/dist/",
   plugins: [react()],
   assetsInclude: ['**/*.svg'],
   root: ".",
   build: {
      manifest: "manifest.json",
      outDir: path.resolve(__dirname, './dist'),
      emptyOutDir: true,
      rollupOptions: {
         input: {
            main: path.resolve(__dirname, "./frontend/main.jsx"),
         },
         output: {
            entryFileNames: "[name]-bundles.js",
            assetFileNames: "[name].[ext]",
         },
      },
   }
});
