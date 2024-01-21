/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/preline/dist/*.js",
  ],
  important: true,
  theme: {
    extend: {
      colors: {
        'self_darkPurple': '#1D1D3F',
        'self_blue': "#4F7AFF",
        'self_blueWhite': "#F4F6FA"
      }
    },

  },
  plugins: [
    require('preline/plugin'),
    require('@tailwindcss/forms'),
    require("daisyui")
  ],
  // daisyui:{
  //   styled:false,
  //   base: false,
  //   prefix: "daisy-"
  // }
}