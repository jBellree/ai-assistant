# Logos

Logo files used for hcti.io image generation. When passed to templates, logos are base64-encoded strings.

## Files needed

- `magnitude-logo-white.png` — white version on transparent background (for dark backgrounds)
- `magnitude-logo-colour.png` — full colour version (orange M + white/orange text)
- `magnitude-logo-white.svg` — SVG version if available
- `magnitude-icon-only.png` — just the M mark, no wordmark (for small spaces / watermarks)
- `dsg-logo.png` — DSG Financial Services logo (if used separately)

## Specs

- Minimum 500px wide for any logo file
- PNG with transparent background preferred
- Keep originals here — never compress or resize the source files

## Usage in hcti.io

Convert the logo file to a base64 string and pass it as an image variable to the hcti.io template.
Use `magnitude-logo-white.png` on all dark background templates.
