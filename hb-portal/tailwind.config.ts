import type { Config } from 'tailwindcss';
import { fontFamily } from 'tailwindcss/defaultTheme';

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
    './styles/**/*.{ts,tsx}',
    './docs/**/*.{md,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#c0392b',
          secondary: '#f39c12',
          dark: '#8e1b0e',
          muted: '#fdf3e7'
        }
      },
      fontFamily: {
        display: ['\"Source Sans 3\"', ...fontFamily.sans],
        body: ['\"Source Sans 3\"', ...fontFamily.sans]
      }
    }
  },
  plugins: [require('tailwindcss-animate')]
};

export default config;
