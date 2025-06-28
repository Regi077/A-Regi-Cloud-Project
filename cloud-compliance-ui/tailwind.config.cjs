/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  safelist: [
    // Allow all color utilities for bubbles
    { pattern: /^(bg|border)-(gray|yellow|green|red)-(400|500|300)/ }
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}