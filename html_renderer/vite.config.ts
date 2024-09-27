import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig(env => {
    if (env.mode === 'preview') {
        return {
            plugins: [svelte()],
            base: './'
        }
    } else {
        return {
            plugins: [svelte()],
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
        }
    }
})
