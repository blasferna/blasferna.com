/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: ["./src/**/*.{html,js}"],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
      brightness: {
        '900': '9',
      },
    },
  },
  variants: {
    extend: {
      brightness: ['dark'],
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

