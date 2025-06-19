import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true // <--- This enables listening on 0.0.0.0
  }
})
// This configuration file sets up a Vite project with React support and configures the development server to listen on all network interfaces.
// This allows the application to be accessible from other devices on the same network, which is useful for testing on mobile devices or other computers.
// The `host: true` option allows the server to be accessed via the local network IP address or hostname, making it easier to test the application in different environments.
// The `react` plugin is included to enable React support, allowing the use of JSX and other React features in the project.
// This setup is commonly used for developing modern web applications with Vite and React, providing a fast and efficient development experience.
// The configuration is minimal and straightforward, focusing on enabling React support and making the development server accessible
