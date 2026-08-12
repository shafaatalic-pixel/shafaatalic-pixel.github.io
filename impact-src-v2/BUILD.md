# Impact map v2 — build & deploy

Polished source of the impact experience (4 tabs: System map, T-shaped atlas, Career journey, Two markets).
Standing rules applied: dash-free, "#1 globally for growth", light+dark themes (styles.css is tokenized:
:root = dark, :root[data-theme="light"] = derived light), analytics + SEO crawlable layer injected at deploy.

## Deploy to live /impact/
1. npm ci
2. npx vite build --base=/impact/
3. python3 scripts/inject_seo.py dist/client/index.html ../impact/index.html dynamic index
   (injects theme bootstrap, SEO head, 3x JSON-LD, analytics.js, hidden crawlable section)
4. rsync -a --delete dist/client/ ../impact/
5. commit + push (GitHub Pages)

## Preview build
- base=/impact-v2-preview/ ; inject mode 'dynamic' 'noindex'

Note: scripts/tokenize.py already applied to styles.css (do not re-run on tokenized file).
Verify on a real mobile device before/after major layout changes.
