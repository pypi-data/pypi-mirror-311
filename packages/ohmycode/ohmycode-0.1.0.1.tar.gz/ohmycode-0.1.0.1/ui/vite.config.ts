import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../src/ohmyprompt/web/static",
    // emptyOutDir: true,
    // sourcemap: true,
    rollupOptions: {
      output: {
        entryFileNames: "index.js",
        assetFileNames: '[name].[ext]',
        manualChunks: () => 'index',
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
