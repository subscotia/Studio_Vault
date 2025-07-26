/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  // This glob pattern correctly tells Tailwind to scan all .html files
  // within the webapp/templates directory, including index.html and test.html.
  content: [
    "./webapp/templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
