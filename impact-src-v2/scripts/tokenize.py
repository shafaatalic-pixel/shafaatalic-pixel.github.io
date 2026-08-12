import io, re, colorsys, sys

CSS='/tmp/ismap2/src/styles.css'
s = io.open(CSS, encoding='utf-8').read()

# backup
io.open('/tmp/styles.dark.bak.css','w',encoding='utf-8').write(s)

def hex_to_rgb(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

def rgb_to_hex(r,g,b):
    return '#%02x%02x%02x' % (round(r*255),round(g*255),round(b*255))

def light_value(hexv):
    r,g,b = hex_to_rgb(hexv)
    hue,l,sat = colorsys.rgb_to_hls(r,g,b)   # note: hls order
    deg = hue*360
    # --- accents (saturated): keep hue, make readable on light ---
    if sat >= 0.55 and 0.30 <= l <= 0.82:
        # brand-specific anchors
        if 150 <= deg <= 200:      # teal
            return '#0a7373'
        if 20 <= deg <= 45:        # amber/orange
            return '#b5651c'
        if 200 <= deg <= 235:      # blue
            return '#2f6fb0'
        if deg < 20 or deg > 340:  # ember/red
            return '#b23a20'
        # generic accent: darken for light bg
        nl = min(l, 0.46); ns = max(sat, 0.5)
        rr,gg,bb = colorsys.hls_to_rgb(hue, nl, ns)
        return rgb_to_hex(rr,gg,bb)
    # --- structural (navy/gray): flip by luminance to warm ivory ramp ---
    if l < 0.18:                    # deep backgrounds -> light cream
        nl = 0.955 - l*0.25
        h2, s2 = (40/360), 0.16
    elif l < 0.45:                  # surfaces/borders -> soft warm
        nl = 0.90 - (l-0.18)*0.55
        h2, s2 = (40/360), 0.12
    else:                           # light grays used as text -> dark ink
        nl = max(0.40 - (l-0.45)*0.28, 0.28)
        h2, s2 = (210/360), 0.06
    rr,gg,bb = colorsys.hls_to_rgb(h2, nl, s2)
    return rgb_to_hex(rr,gg,bb)

# collect distinct opaque hex (3 or 6 digits), NOT hex8 (alpha kept as-is)
pat = re.compile(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b')
order=[]; seen={}
def scan(m):
    h=m.group(0)
    if len(h.lstrip('#'))==8:   # keep alpha colors untouched
        return h
    if h.lower() not in seen:
        seen[h.lower()]=None; order.append(h)
    return h
pat.sub(scan, s)

# assign tokens
tokmap={}
for i,h in enumerate(order, 1):
    tokmap[h.lower()] = '--ct-%02d' % i

# replace opaque hex with var()
def rep(m):
    h=m.group(0)
    if len(h.lstrip('#'))==8: return h
    return 'var(%s)' % tokmap[h.lower()]
s2 = pat.sub(rep, s)

# build dark + light token blocks
dark_lines = []; light_lines=[]
for h in order:
    t = tokmap[h.lower()]
    dark_lines.append('  %s: %s;' % (t, h))
    light_lines.append('  %s: %s;' % (t, light_value(h)))

header = ':root{\n' + '\n'.join(dark_lines) + '\n}\n'
light  = ':root[data-theme="light"]{\n  color-scheme: light;\n' + '\n'.join(light_lines) + '\n}\n'

out = header + light + s2
io.open(CSS,'w',encoding='utf-8').write(out)
print('distinct opaque colors tokenized:', len(order))
print('sample light mappings:')
for h in order[:14]:
    print('  ', h, '->', light_value(h))
