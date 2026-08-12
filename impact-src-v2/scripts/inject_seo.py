import io, re, sys

# usage: inject_seo.py <built_index> <impact_src_index> <mode: lockdark|dynamic> <robots: noindex|index>
built_path, src_path, mode, robots = sys.argv[1:5]

src = io.open(src_path, encoding='utf-8').read()
built = io.open(built_path, encoding='utf-8').read()

# --- extract SEO head block from current /impact/ head:
# from the favicon <link rel="icon" ...> up to (not including) the first asset <script type="module"
h0 = src.index('<link rel="icon"')
h1 = src.index('<script type="module"')
head_seo = src[h0:h1].rstrip()

# drop the theme bootstrap script from head_seo; we re-add per mode
head_seo = re.sub(r'<script>\(function\(\)\{try\{var t=localStorage.*?\}\)\(\);</script>\s*', '', head_seo, flags=re.S)

# --- extract hidden crawlable body section
b0 = src.index('<section class="visually-hidden"')
b1 = src.index('</section>', b0) + len('</section>')
body_section = src[b0:b1]

# --- theme bootstrap per mode
if mode == 'lockdark':
    boot = '<script>document.documentElement.setAttribute("data-theme","dark");</script>'
else:
    boot = ("<script>(function(){try{var t=localStorage.getItem('shafaat_theme');"
            "if(!t){t=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';}"
            "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>")

robots_tag = '<meta name="robots" content="noindex,nofollow" />' if robots == 'noindex' else ''

# --- remove placeholder <title>Prototype</title>
built = built.replace('<title>Prototype</title>', '')

inject_head = boot + '\n' + robots_tag + '\n' + head_seo + '\n<script src="/assets/analytics.js"></script>\n'
built = built.replace('</head>', inject_head + '</head>', 1)

# --- inject hidden section after root div
built = built.replace('<div id="root"></div>', '<div id="root"></div>\n' + body_section, 1)

io.open(built_path, 'w', encoding='utf-8').write(built)
# report
checks = {
  'title': '<title>Impact System Map' in built,
  'canonical': 'rel="canonical"' in built,
  'og:image': 'og:image' in built,
  'ld+json x': built.count('application/ld+json'),
  'analytics': 'analytics.js' in built,
  'hidden section': 'visually-hidden' in built,
  'robots': ('noindex' in built) if robots=='noindex' else True,
  'theme boot': 'data-theme' in built,
}
print(checks)
