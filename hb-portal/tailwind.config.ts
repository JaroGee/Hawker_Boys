import type { Config } from 'tailwindcss';
import plugin from 'tailwindcss/plugin';

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
    './styles/**/*.{ts,tsx,css}',
    './docs/**/*.{md,mdx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Segoe UI"', 'Helvetica Neue', 'Arial', 'sans-serif'],
        display: ['"Segoe UI"', 'Helvetica Neue', 'Arial', 'sans-serif']
      },
      colors: {
        brand: {
          DEFAULT: '#F26522',
          dark: '#C24E18',
          light: '#FF8B55'
        },
        ink: {
          DEFAULT: '#161616',
          subtle: '#4E4E4E'
        },
        surface: {
          DEFAULT: '#FFFFFF',
          muted: '#F6F2EE',
          dark: '#1F1A17'
        }
      },
      borderRadius: {
        xl: '1.5rem'
      },
      boxShadow: {
        card: '0 20px 50px rgba(17, 16, 14, 0.08)'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    plugin(({ addBase }) => {
      addBase({
        ':root': {
          colorScheme: 'light'
        },
        '.dark': {
          colorScheme: 'dark'
        }
      });
    })
  ]
};

export default config;
