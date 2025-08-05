/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./webapp/templates/**/*.html",
    "./webapp/static/**/*.js" // Add this line to scan JS files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
