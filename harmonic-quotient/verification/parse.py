"""Parse the harmonic-quotient manuscript into structured data."""
import re, json, sys

TEX = sys.argv[1] if len(sys.argv) > 1 else '../archive/regular-graph-harmonic-quotient-examples_2023-03-26.tex'
tex = open(TEX).read()
tex = tex[:tex.index('\\end{document}')]
# strip comments (but keep "% d3reg8a" style markers after \begin{example})
lines = []
for ln in tex.split('\n'):
    m = re.match(r'(\\begin\{example\}%\s*\w+)', ln)
    if m:
        lines.append(m.group(1)); continue
    # remove % comments not escaped
    out = re.sub(r'(?<!\\)%.*$', '', ln)
    lines.append(out)
src = '\n'.join(lines)

PAIR = re.compile(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)')

def edge_sets(chunk):
    """Return list of (label, edges, pos) for each \\{ ... \\} span containing pairs."""
    res = []
    for m in re.finditer(r'\\\{(.*?)\\\}', chunk, re.S):
        body = m.group(1)
        prs = [(int(a), int(b)) for a, b in PAIR.findall(body)]
        if len(prs) < 3:
            continue
        pre = chunk[max(0, m.start() - 60):m.start()]
        lab = 'E1' if re.search(r'E_1|E1', pre) else 'E2'
        res.append((lab, prs, m.start()))
    return res

def perms(s):
    gens = []
    for g in re.split(r',\s*(?=\()', s.strip()):
        cyc = [tuple(int(x) for x in c.split(',')) for c in re.findall(r'\(([\d,\s]+)\)', g)]
        if cyc:
            gens.append(cyc)
    return gens

def parse_gens(body):
    # body between \langle and \rangle; generators separated by '),' followed by ' (' starting new gen?
    # cycles inside a generator are juxtaposed; generators separated by comma between ')' and '('
    body = body.replace('\n', ' ')
    parts = re.split(r'\)\s*,\s*\(', body)
    # re-split: a comma between ')' and '(' separates generators
    gens = []
    cur = body
    tokens = re.split(r'(?<=\))\s*,\s*(?=\()', body)
    for t in tokens:
        cyc = [tuple(int(x) for x in c.split(',')) for c in re.findall(r'\(([\d,\s]+)\)', t)]
        if cyc:
            gens.append(cyc)
    return gens

def tables(chunk):
    res = []
    for m in re.finditer(r'\\begin\{tabular\}\{c\|c\|c\|c\}(.*?)\\end\{tabular\}', chunk, re.S):
        rows = []
        for r in m.group(1).split('\\\\'):
            cells = [c.strip() for c in r.split('&')]
            if len(cells) == 4 and re.fullmatch(r'\d+', cells[0].replace('\\hline', '').strip()):
                rows.append(tuple(int(c.replace('\\hline', '').strip()) for c in cells))
        res.append((rows, m.start(), m.end()))
    return res

data = {'examples': [], 'items': []}

for m in re.finditer(r'\\begin\{example\}%\s*(\w+)(.*?)\\end\{example\}', src, re.S):
    name, body = m.group(1), m.group(2)
    ex = {'name': name, 'line': src[:m.start()].count('\n') + 1}
    ex['edges'] = [(l, e) for l, e, p in edge_sets(body)]
    ex['groups'] = []
    for g in re.finditer(r'G(?:_\d)?\s*=\s*\\langle(.*?)\\rangle', body, re.S):
        ex['groups'].append({'gens': parse_gens(g.group(1)), 'pos': g.start(),
                             'line': ex['line'] + body[:g.start()].count('\n')})
    ex['tables'] = []
    tbs = tables(body)
    for i, (rows, s, e) in enumerate(tbs):
        nxt = tbs[i + 1][1] if i + 1 < len(tbs) else len(body)
        after = body[e:nxt]
        g1 = re.search(r'genus\}?\(\\Gamma_1\)\s*=\s*(\d+)', after)
        g2 = re.search(r'genus\}?\(\\Gamma_2\)\s*=\s*(\d+)', after)
        d = re.search(r'deg\(\\phi\)\s*=\s*(\d+)', after)
        ex['tables'].append({'rows': rows, 'pos': s, 'line': ex['line'] + body[:s].count('\n'),
                             'g1': int(g1.group(1)) if g1 else None,
                             'g2': int(g2.group(1)) if g2 else None,
                             'deg': int(d.group(1)) if d else None})
    # E1 sets with positions for association
    ex['E1'] = [(p, e) for l, e, p in edge_sets(body) if l == 'E1']
    data['examples'].append(ex)

# list items
for m in re.finditer(r'\\item\s*\{\\tt\s*(d\dreg\d+\w)\}(.*?)(?=\\item|\\end\{enumerate\})', src, re.S):
    name, body = m.group(1), m.group(2)
    it = {'name': name, 'line': src[:m.start()].count('\n') + 1, 'text': body}
    es = edge_sets(body)
    it['edges'] = es[0][1] if es else None
    cp = re.search(r'\\\[\s*(x\^\{?\d+\}?[^\]]*?)\\\]', body, re.S)
    it['charpoly'] = cp.group(1) if cp else None
    for key, pat in [('diameter', r'[Dd]iameter \$(\d+)\$'), ('girth', r'girth \$(\d+)\$'),
                     ('circumference', r'circumference \$(\d+)\$'),
                     ('aut', r'automorphism group (?:is )?(?:of )?(?:order|size) \$(\d+)\$'),
                     ('crit', r'critical group[^$]*?\$(\d+)')]:
        mm = re.search(pat, body)
        it[key] = int(mm.group(1)) if mm else None
    sg = re.search(r'LCFGraph\(([^@+]*)\)', body)
    it['sage'] = sg.group(1) if sg else None
    data['items'].append(it)

# summary tables (graph label & LCF & aut & genus & crit)
data['summary'] = []
for m in re.finditer(r'(d\dreg\d+\w)\s*&\s*([^&]*)&\s*(\d+)\s*&\s*(\d+)\s*(?:&\s*\$([^$]*)\$)?', src):
    data['summary'].append({'name': m.group(1), 'lcf': m.group(2).strip(), 'aut': int(m.group(3)),
                            'genus': int(m.group(4)), 'crit': m.group(5)})

json.dump(data, open('data.json', 'w'), indent=1)
print(len(data['examples']), 'examples;', sum(len(e['tables']) for e in data['examples']), 'tables;',
      sum(len(e['groups']) for e in data['examples']), 'groups;', len(data['items']), 'items;',
      len(data['summary']), 'summary rows')
for e in data['examples']:
    print(e['name'], 'E:', [(l, len(x)) for l, x in e['edges']], 'G:', len(e['groups']), 'T:',
          [len(t['rows']) for t in e['tables']])
