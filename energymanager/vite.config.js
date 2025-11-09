import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
   root: ".", // kein eigenes Root, da du index.html nicht nutzt
   build: {
      outDir: "static/dist",
      emptyOutDir: true,
      rollupOptions: {
         input: path.resolve(__dirname, "frontend/index.js"),
         output: {
            entryFileNames: "assets/[name].js",
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
