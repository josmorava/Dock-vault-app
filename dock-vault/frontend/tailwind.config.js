/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{vue,ts,js}"],
  theme: {
    extend: {
      colors: {
        base: { light: "#F7F8FA", dark: "#0F1115" },
        surface: { light: "#FFFFFF", dark: "#1A1D23" },
        accent: { DEFAULT: "#4F46E5", dark: "#818CF8" },
        accent2: { DEFAULT: "#0EA5A4", dark: "#2DD4BF" },
      },
    },
  },
  plugins: [],
};
