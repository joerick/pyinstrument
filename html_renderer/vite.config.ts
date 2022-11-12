import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { visualizer } from "rollup-plugin-visualizer";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte(), visualizer()],
  build: {
    assetsInlineLimit: 1e100,
    cssCodeSplit: false,
    lib: {
      entry: 'src/main.ts',
      name: 'pyinstrumentHTMLRenderer',
      fileName: 'pyinstrument-html',
      formats: ['iife'],
    }
  }
})
