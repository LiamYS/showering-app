/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        'main': '#2c5f78',
        'main-light': '#51acc5',
        'main-dark': '#1c3d52',
      }
    },
  },
  plugins: [],
}
