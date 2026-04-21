import tailwindcss from "@tailwindcss/vite";
import { devtools } from "@tanstack/devtools-vite";

import { tanstackRouter } from "@tanstack/router-plugin/vite";

import viteReact from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const config = defineConfig(({ command }) => ({
  resolve: { tsconfigPaths: true },
  plugins: [
    devtools(),
    tailwindcss(),
    tanstackRouter({ target: "react", autoCodeSplitting: true }),
    viteReact(),
  ],
  server: {
    proxy:
      command === "serve"
        ? {
            "/api": {
              rewrite: (path) => path.replace(/^\/api/, ""),
              target: process.env.VITE_BACKEND_URL ?? "http://localhost:8080",
              changeOrigin: true,
            },
          }
        : {},
  },
}));

export default config;