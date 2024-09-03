/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: "#297a7d",
        secondary: "#f67600",
      },
      fontFamily: {
        rawline: ["Rawline", "sans-serif"],
      },
    },
  },
  plugins: [],
}
