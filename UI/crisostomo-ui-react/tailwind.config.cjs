module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'jenkins-dark': 'red',
        'jenkins-light': '#E6E6E6',
        'jenkins-hover': '#D0D0D0',
        'jenkins-accent': '#F0AD4E',
      },
    },
  },
  plugins: [],
};
