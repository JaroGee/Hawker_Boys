# Hawker Boys Brand Notes

The TMS UI inherits the cadence and colour story from hawkerboys.com while keeping the build lightweight (system fonts only, no remote assets).

## Tokens

| Token | Light | Dark | Notes |
| --- | --- | --- | --- |
| `--hb-surface-base` | `#f4efe9` | `#0d0b08` | Matches the creamy backgrounds used on marketing pages and the near-black hero bands. |
| `--hb-surface-card` | `#fffefc` | `#16120e` | Card colour for shells/drawers. Keeps text legible and avoids stark whites. |
| `--hb-border-subtle` | `#e2d8cd` | `#342c23` | Soft dividers that mirror the tan outlines in brand collateral. |
| `--hb-text-primary` | `#19120c` | `#f3ece3` | High-contrast body colour anchored to the warm browns of the wordmark. |
| `--hb-text-muted` | `#73685c` | `#c4b8aa` | Secondary copy colour that still clears WCAG AA on both surfaces. |
| `--hb-accent` | `#f2643d` | `#ff8a3d` | Flame orange used on CTA buttons, focus rings, and badges. Derived from the icon PNGs. |
| `--hb-accent-soft` | `rgba(242,100,61,0.15)` | `rgba(255,138,61,0.15)` | Tint for chips/badges to avoid solid fills. |
| `--hb-positive` | `#1d8f66` | `#3dd19b` | Pairs with the teal accents on hawkerboys.com for success states. |
| `--hb-danger` | `#d3554c` | `#ff7f73` | Harmonised with the accent orange to keep alerts on brand. |
| Radius scale | 6px / 10px / 16px | same | Matches the rounded cards and pill buttons on the public site. |

Spacing uses modular steps (`0.25rem`, `0.5rem`, `1rem`, `1.5rem`, `2.25rem`) to keep rhythm consistent with the hero typography on the marketing site. Shadows stay soft (`var(--hb-shadow-soft)`) to echo the floating recipe cards from hawkerboys.com.

## Icons & favicons

- Source: `/Hawkerboyslogos` directory in the repo.
- Header uses `Icon.png` (flame) plus `Hawker_Boys_logo_h.PNG` (wordmark) so the in-app shell mirrors the landing page masthead.
- Favicons and touch icons are generated from `icon_bgr.png` to guarantee a pure black square background. Sizes shipped: `favicon-32.png`, `favicon-48.png`, `apple-touch-icon-180.png`, and `favicon.svg`.
- The SVG favicon recreates the flame colours so Safari’s dark tabs avoid the white halo that previous builds showed.

## Usage guidance

- Keep CTA buttons in the accent gradient (`--hb-accent` → `--hb-accent-strong`).
- Use `--hb-surface-muted` blocks for tables/forms to mimic the section dividers on hawkerboys.com.
- Status badges rely on `StatusBadge` component (accent/success/danger) to keep consistent contrast and rounded shapes.
