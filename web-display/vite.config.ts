import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    proxy: {
      "/socket.io": {
        target: "ws://127.0.0.1:3000",
        // target: "ws://rpi:5000",
        ws: true,
        rewriteWsOrigin: true,
      },
      "/api": {
        target: "http://127.0.0.1:5000/",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
