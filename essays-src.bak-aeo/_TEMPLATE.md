---
slug: your-essay-slug
title: Your essay title, as it appears on the page and card
lens: ai
date: 2026-07-16
dek: One or two sentences that sell the essay. Shows on the hub card and as the meta description.
og: /assets/og/your-essay-slug.png
figure: /assets/essays/your-essay-slug.jpg
figureAlt: Alt text describing the in-article infographic.
figureCaption: The idea at a glance, click to enlarge.
keywords: comma, separated, seo, keywords
readmin: 5
search: extra searchable keywords for the hub filter box
---

Open with a concrete scene or a sharp claim. This first paragraph automatically becomes the lede (larger text), and the figure image is inserted right after it.

Keep writing in normal paragraphs. Separate paragraphs with a blank line. Use **bold** for emphasis and [links](https://example.com) inline.

## Use "## " for section headings

Each section is just a heading line followed by paragraphs.

> Lines beginning with "> " become a teal pull-quote, use one memorable line per essay.

## The short version

- Lines beginning with "- " become a boxed bullet list.
- Great for a "key takeaways" recap.
- Use **bold** at the start of each for a scannable summary.

Close with one honest question to the reader in **bold**.

<!--
HOW TO USE THIS FILE
1. Copy this file to essays-src/<your-slug>.md and fill it in.
2. Set lens to one of: ai | public-health | healthtech | growth
3. Drop the OG card at the `og` path (assets/og/) and, if used, the wide infographic at the `figure` path (assets/essays/).
4. Run: node build-essays.js
 -> generates <slug>.html, rebuilds essays.html + sitemap.xml.
5. Upload the changed files to GitHub, then Request Indexing in Search Console.
Fields figure/figureAlt/figureCaption/keywords/readmin/search are optional.
To register a hand-built bespoke page in the hub WITHOUT generating it, set `generate: false` and omit the body.
-->
