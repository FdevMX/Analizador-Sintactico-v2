/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{js,ts,jsx,tsx}', // Asegúrate de que esta ruta incluye tus componentes
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'dark-gray': '#09090B', // This is the very dark gray color for the main background
        'dark-gray-800': '#1E1E1E', // This is a slightly lighter gray for elements like textareas and output boxes
        'dark-line-table': '#24242b',
      },
    },
  },
  plugins: [],
}
