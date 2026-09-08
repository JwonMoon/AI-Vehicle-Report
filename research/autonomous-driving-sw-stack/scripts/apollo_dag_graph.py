#!/usr/bin/env python3
"""apollo_dag_graph.py -- static anatomy of a Baidu Apollo checkout (python3 stdlib only).

Usage:
    python3 apollo_dag_graph.py <apollo_repo_root> [--out report.md]

What it measures (all from the source tree, no build required):
  * *.dag files -> Cyber RT components (class_name, config file, reader channels, timer interval)
  * per component: output channels inferred from CreateWriter<...>(...) in the component .cc,
    resolved through (a) string literals, (b) FLAGS_* (DEFINE_string in any gflags .cc),
    (c) proto config accessors (xxx_channel_name()) looked up in the component's config pb.txt
  * per top-level module dir: LOC by language, dag/component counts, GPU/TensorRT/Paddle/ONNX/Torch usage
  * counts of .proto files and Bazel BUILD targets (by rule kind)
  * cyber/ summary: sub-dir LOC, scheduler confs (classic groups / choreography), transport modes
  * edge list + DOT graph for the main driving pipeline (drivers/perception/prediction/planning/control/...)

Everything is heuristic text parsing; unresolved channel expressions are reported as `<expr>`.
"""
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict, OrderedDict
from datetime import datetime, timezone

# --------------------------------------------------------------------------------------
# generic helpers
# --------------------------------------------------------------------------------------
TEXT_EXT_LANG = OrderedDict([
    ('.cc', 'C++'), ('.cpp', 'C++'), ('.cxx', 'C++'), ('.c', 'C'),
    ('.h', 'C/C++ header'), ('.hpp', 'C/C++ header'), ('.hh', 'C/C++ header'), ('.inl', 'C/C++ header'),
    ('.cu', 'CUDA'), ('.cuh', 'CUDA'),
    ('.py', 'Python'), ('.proto', 'Proto'),
    ('.js', 'JS/TS'), ('.jsx', 'JS/TS'), ('.ts', 'JS/TS'), ('.tsx', 'JS/TS'),
    ('.sh', 'Shell'), ('.bash', 'Shell'),
    ('.bzl', 'Bazel'), ('.bazel', 'Bazel'),
    ('.pb.txt', 'Config(pb.txt/conf/dag/launch/flag)'), ('.conf', 'Config(pb.txt/conf/dag/launch/flag)'),
    ('.dag', 'Config(pb.txt/conf/dag/launch/flag)'), ('.launch', 'Config(pb.txt/conf/dag/launch/flag)'),
    ('.flag', 'Config(pb.txt/conf/dag/launch/flag)'), ('.yaml', 'YAML/JSON/XML'), ('.yml', 'YAML/JSON/XML'),
    ('.json', 'YAML/JSON/XML'), ('.xml', 'YAML/JSON/XML'),
    ('.md', 'Markdown'), ('.S', 'Assembly'), ('.s', 'Assembly'),
])
SKIP_DIRS = {'.git', 'node_modules', 'third_party', 'bazel-bin', 'bazel-out'}


def lang_of(path):
    base = os.path.basename(path)
    if base in ('BUILD', 'BUILD.bazel', 'WORKSPACE') or base.endswith('.BUILD'):
        return 'Bazel'
    low = base.lower()
    if low.endswith('.pb.txt'):
        return TEXT_EXT_LANG['.pb.txt']
    for ext, lang in TEXT_EXT_LANG.items():
        if base.endswith(ext):
            return lang
    return None


def read_text(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ''


def walk(root, skip_third_party=True):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS or (d == 'third_party' and not skip_third_party)]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def rel(root, path):
    return os.path.relpath(path, root)


def top_module(relpath):
    """modules/<x>/... -> x ; cyber/... -> cyber ; else first path element"""
    parts = relpath.split(os.sep)
    if parts[0] == 'modules' and len(parts) > 1:
        return 'modules/' + parts[1]
    return parts[0]


# --------------------------------------------------------------------------------------
# minimal text-proto parser (enough for .dag and *.pb.txt / sched .conf files)
# --------------------------------------------------------------------------------------
_TOKEN = re.compile(r'''
    \s+ | \#[^\n]* |                       # whitespace / comment
    (?P<str>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*') |
    (?P<punct>[{}\[\],:;]) |
    (?P<word>[^\s{}\[\],:;"']+)
''', re.X)


def tokenize(text):
    pos = 0
    out = []
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m:
            pos += 1
            continue
        pos = m.end()
        if m.group('str') is not None:
            out.append(('str', m.group('str')[1:-1]))
        elif m.group('punct') is not None:
            out.append(('p', m.group('punct')))
        elif m.group('word') is not None:
            out.append(('w', m.group('word')))
    return out


def parse_textproto(text):
    """Returns dict: key -> list of values (str or dict). Repeated keys accumulate."""
    toks = tokenize(text)
    i = [0]

    def parse_value():
        t = toks[i[0]]
        if t == ('p', '{'):
            i[0] += 1
            return parse_msg()
        if t == ('p', '['):
            i[0] += 1
            vals = []
            while i[0] < len(toks) and toks[i[0]] != ('p', ']'):
                if toks[i[0]] == ('p', ','):
                    i[0] += 1
                    continue
                vals.append(parse_value())
            i[0] += 1  # ]
            return vals
        i[0] += 1
        # adjacent string literals concatenate
        val = t[1]
        while t[0] == 'str' and i[0] < len(toks) and toks[i[0]][0] == 'str':
            val += toks[i[0]][1]
            i[0] += 1
        return val

    def parse_msg():
        msg = defaultdict(list)
        while i[0] < len(toks):
            t = toks[i[0]]
            if t == ('p', '}'):
                i[0] += 1
                return msg
            if t[0] != 'w':
                i[0] += 1
                continue
            key = t[1]
            i[0] += 1
            if i[0] < len(toks) and toks[i[0]] == ('p', ':'):
                i[0] += 1
            if i[0] >= len(toks):
                break
            v = parse_value()
            if isinstance(v, list):
                msg[key].extend(v)
            else:
                msg[key].append(v)
            if i[0] < len(toks) and toks[i[0]] in (('p', ','), ('p', ';')):
                i[0] += 1
        return msg

    return parse_msg()


def first(msg, key, default=''):
    v = msg.get(key, [])
    return v[0] if v else default


# --------------------------------------------------------------------------------------
# DAG parsing
# --------------------------------------------------------------------------------------
def parse_dag(root, path):
    text = read_text(path)
    msg = parse_textproto(text)
    comps = []
    for mc in msg.get('module_config', []):
        if not isinstance(mc, dict):
            continue
        lib = first(mc, 'module_library')
        for kind in ('components', 'timer_components'):
            for c in mc.get(kind, []):
                if not isinstance(c, dict):
                    continue
                cfg = first(c, 'config', {})
                if not isinstance(cfg, dict):
                    cfg = {}
                readers = []
                for r in cfg.get('readers', []):
                    if isinstance(r, dict):
                        ch = first(r, 'channel')
                        if ch:
                            readers.append(ch)
                comps.append({
                    'dag': rel(root, path),
                    'module': top_module(rel(root, path)),
                    'library': lib,
                    'kind': 'timer' if kind == 'timer_components' else 'component',
                    'class_name': first(c, 'class_name'),
                    'name': first(cfg, 'name'),
                    'config_file': first(cfg, 'config_file_path'),
                    'flag_file': first(cfg, 'flag_file_path'),
                    'interval_ms': first(cfg, 'interval'),
                    'dag_readers': readers,
                })
    return comps


# --------------------------------------------------------------------------------------
# source scanning: component classes, writers/readers, gflags topics
# --------------------------------------------------------------------------------------
RE_REGISTER = re.compile(r'CYBER_REGISTER_COMPONENT\(\s*([A-Za-z_][\w:]*)\s*\)')
RE_DEFINE_STRING = re.compile(r'DEFINE_string\(\s*(\w+)\s*,\s*("(?:\\.|[^"\\])*")')
# CreateWriter<Type>(  -- the first argument is extracted with balanced-paren scanning (see iter_create_calls)
RE_CREATE_HEAD = re.compile(r'Create(Writer|Reader)\s*<\s*([\w:<>\s]+?)\s*>\s*\(', re.S)
TESTDATA_DIRS = {'testdata', 'test_data', 'testdata_backup'}


def iter_create_calls(text):
    """Yield (kind, msg_type, first_arg_expr) for every CreateWriter/CreateReader call in text."""
    for m in RE_CREATE_HEAD.finditer(text):
        i, depth, start = m.end(), 0, m.end()
        while i < len(text):
            ch = text[i]
            if ch in '([{<' and ch != '<':
                depth += 1
            elif ch in ')]}':
                if depth == 0:
                    break
                depth -= 1
            elif ch == ',' and depth == 0:
                break
            elif ch == '"':  # skip string literal
                j = text.find('"', i + 1)
                while j != -1 and text[j - 1] == '\\':
                    j = text.find('"', j + 1)
                i = j if j != -1 else i
            i += 1
        yield m.group(1), ' '.join(m.group(2).split()), text[start:i].strip()
RE_CHANNELISH_FIELD = re.compile(r'^\s*([a-z_]*(?:channel|topic)[a-z_]*)\s*:\s*"([^"]*)"', re.M)
GPU_PATTERNS = OrderedDict([
    ('CUDA', re.compile(r'\bcuda[A-Z_]\w*\(|#include\s*[<"]cuda|__global__|\bcudaMalloc|cublas|cudnn', re.I)),
    ('TensorRT', re.compile(r'NvInfer|nvinfer1|tensorrt|TensorRT|\.trt\b|\.engine\b')),
    ('Paddle', re.compile(r'paddle_inference|paddle::|PaddleInference|libpaddle|\bpaddle\b', re.I)),
    ('ONNX', re.compile(r'onnxruntime|\bonnx\b|\.onnx\b', re.I)),
    ('LibTorch', re.compile(r'torch::|#include\s*[<"]torch/|libtorch|\.pt\b')),
    ('ROCm/HIP', re.compile(r'\bhip[A-Z]\w+\(|#include\s*[<"]hip/|__HIP_PLATFORM|rocm', re.I)),
])


def scan_sources(root):
    """One pass over the tree; returns dicts keyed as needed."""
    loc = defaultdict(lambda: Counter())         # module -> lang -> lines
    files_by_lang = defaultdict(lambda: Counter())
    registered = {}                              # class_name -> source file
    flags = {}                                   # FLAGS name -> value
    gpu_hits = defaultdict(lambda: Counter())    # module -> pattern -> file count
    cu_files = Counter()                         # module -> .cu count
    proto_files = []
    build_rule_kinds = Counter()
    build_files = 0
    build_targets_by_module = Counter()
    sources = {}                                 # relpath -> text (only .cc/.h to save memory)
    testdata_loc = Counter()                     # module -> lines living under testdata/ dirs
    for path in walk(root):
        rp = rel(root, path)
        lang = lang_of(path)
        if lang is None:
            continue
        text = read_text(path)
        if not text:
            continue
        mod = top_module(rp)
        nlines = text.count('\n') + (0 if text.endswith('\n') else 1)
        if any(part in TESTDATA_DIRS for part in rp.split(os.sep)):
            testdata_loc[mod] += nlines   # kept out of the language columns
        else:
            loc[mod][lang] += nlines
        files_by_lang[mod][lang] += 1
        if lang == 'Proto':
            proto_files.append(rp)
        if lang == 'Bazel' and os.path.basename(path) in ('BUILD', 'BUILD.bazel'):
            build_files += 1
            for m in re.finditer(r'^([a-z_][a-z0-9_]*)\s*\(', text, re.M):
                build_rule_kinds[m.group(1)] += 1
                build_targets_by_module[mod] += 1
        if lang in ('C++', 'C/C++ header', 'CUDA', 'C'):
            if lang == 'CUDA':
                cu_files[mod] += 1
            for m in RE_REGISTER.finditer(text):
                registered.setdefault(m.group(1).split('::')[-1], rp)
            for m in RE_DEFINE_STRING.finditer(text):
                flags.setdefault(m.group(1), m.group(2)[1:-1])
            if 'CreateWriter' in text or 'CreateReader' in text or 'CYBER_REGISTER_COMPONENT' in text:
                sources[rp] = text
            for name, pat in GPU_PATTERNS.items():
                if pat.search(text):
                    gpu_hits[mod][name] += 1
        elif lang in ('Python', 'Config(pb.txt/conf/dag/launch/flag)', 'Bazel'):
            for name, pat in GPU_PATTERNS.items():
                if name in ('TensorRT', 'Paddle', 'ONNX', 'LibTorch') and pat.search(text):
                    gpu_hits[mod][name] += 1
    return dict(loc=loc, files_by_lang=files_by_lang, registered=registered, flags=flags,
                gpu_hits=gpu_hits, cu_files=cu_files, proto_files=proto_files,
                build_rule_kinds=build_rule_kinds, build_files=build_files,
                build_targets_by_module=build_targets_by_module, sources=sources, testdata_loc=testdata_loc)


def config_channel_fields(root, config_file):
    """Return {field_name: [values]} for channel/topic-like fields in a component config file."""
    if not config_file:
        return {}
    p = config_file
    for prefix in ('/apollo/', '/opt/apollo/neo/'):
        if p.startswith(prefix):
            p = p[len(prefix):]
    cand = os.path.join(root, p)
    if not os.path.exists(cand):
        return {}
    text = read_text(cand)
    out = defaultdict(list)
    for m in RE_CHANNELISH_FIELD.finditer(text):
        out[m.group(1)].append(m.group(2))
    return out


def _split_list(v):
    return [x.strip() for x in v.split(',') if x.strip()] if ',' in v else [v]


def resolve_expr(expr, flags, cfg_fields, text='', depth=0):
    """Resolve a CreateWriter/Reader channel expression to a channel string when possible."""
    expr = ' '.join(expr.split())
    m = re.search(r'"([^"]+)"', expr)
    if m:
        return m.group(1), 'literal'
    m = re.search(r'FLAGS_(\w+)', expr)
    if m and m.group(1) in flags:
        return flags[m.group(1)], 'FLAGS_' + m.group(1)
    # config accessor chains: config_.topic_config().prediction_topic()  /  comp_config.output_channel_name()
    accs = re.findall(r'(\w+)\(\)', expr)
    for acc in reversed(accs):
        if acc in cfg_fields and cfg_fields[acc]:
            vals = [x for v in cfg_fields[acc] for x in _split_list(v)]
            return (vals[0] if len(vals) == 1 else vals), 'conf.' + acc
    # ReaderConfig object:  foo_reader_config.channel_name = <expr2>;  (control component style)
    if text and depth < 2 and re.fullmatch(r'[\w.]+', expr):
        m = re.search(re.escape(expr) + r'\.channel_name\s*=\s*([^;]+);', text)
        if m:
            val, ev = resolve_expr(m.group(1), flags, cfg_fields, text, depth + 1)
            if val is not None:
                return val, 'ReaderConfig.channel_name<-' + ev
        # member assigned from a config accessor:  output_channel_name_ = comp_config.output_channel_name();
        m = re.search(r'\b' + re.escape(expr) + r'\s*=\s*([^;]+);', text)
        if m and m.group(1).strip() != expr:
            val, ev = resolve_expr(m.group(1), flags, cfg_fields, text, depth + 1)
            if val is not None:
                return val, ev
    # bare member variable (e.g. output_channel_name_): try a matching config field
    m = re.search(r'\b(\w+?)_?\b$', expr)
    if m:
        stem = m.group(1).rstrip('_')
        for k, vals in cfg_fields.items():
            if k == stem or k.endswith(stem):
                vals = [x for v in vals for x in _split_list(v)]
                return (vals[0] if len(vals) == 1 else vals), 'conf.' + k
    return None, expr


def component_sources(root, cls, scan):
    """Registration file + sibling files in the same directory that implement `cls` and call Create*."""
    reg = scan['registered'].get(cls)
    if not reg:
        return []
    d = os.path.dirname(reg)
    out = [reg]
    for rp in scan['sources']:
        if rp != reg and os.path.dirname(rp) == d and (cls + '::') in scan['sources'][rp]:
            out.append(rp)
    return out


def infer_channels(root, comp, scan):
    """Fill comp['inputs'], comp['outputs'] (lists of (channel, evidence)) and comp['source']."""
    cls = comp['class_name']
    srcs = component_sources(root, cls, scan)
    comp['source'] = ', '.join(srcs)
    cfg_fields = config_channel_fields(root, comp['config_file'])
    inputs = [(ch, 'dag reader') for ch in comp['dag_readers']]
    outputs = []
    unresolved = []
    for src in srcs:
        text = scan['sources'].get(src) or read_text(os.path.join(root, src))
        for kind, mtype, expr in iter_create_calls(text):
            val, ev = resolve_expr(expr, scan['flags'], cfg_fields, text)
            entry_list = outputs if kind == 'Writer' else inputs
            if val is None:
                unresolved.append((kind, mtype, ev))
                entry_list.append(('<%s>' % ev, 'code:%s' % src))
            else:
                vals = val if isinstance(val, list) else [val]
                for v in vals:
                    entry_list.append((v, '%s via %s' % (mtype, ev)))
    # config-only hints (fields containing output/input in their name)
    for k, vals in cfg_fields.items():
        for v in [x for v0 in vals for x in _split_list(v0)]:
            if 'output' in k and all(v != o[0] for o in outputs):
                outputs.append((v, 'conf field ' + k))
            elif 'input' in k and all(v != o[0] for o in inputs):
                inputs.append((v, 'conf field ' + k))
    # de-dup preserving order
    def dedup(lst):
        seen, out = set(), []
        for ch, ev in lst:
            if ch not in seen:
                seen.add(ch)
                out.append((ch, ev))
        return out
    comp['inputs'] = dedup(inputs)
    comp['outputs'] = dedup(outputs)
    comp['unresolved'] = unresolved


# --------------------------------------------------------------------------------------
# cyber/ summary
# --------------------------------------------------------------------------------------
def cyber_summary(root):
    out = {'sched': [], 'transport': {}, 'subdirs': Counter()}
    conf_dir = os.path.join(root, 'cyber', 'conf')
    if os.path.isdir(conf_dir):
        for fn in sorted(os.listdir(conf_dir)):
            p = os.path.join(conf_dir, fn)
            msg = parse_textproto(read_text(p))
            sc = first(msg, 'scheduler_conf', {})
            if isinstance(sc, dict) and sc:
                policy = first(sc, 'policy')
                entry = {'file': 'cyber/conf/' + fn, 'policy': policy or '(default)',
                         'routine_num': first(sc, 'routine_num'), 'default_proc_num': first(sc, 'default_proc_num'),
                         'process_level_cpuset': first(sc, 'process_level_cpuset'),
                         'threads': [], 'groups': [], 'choreo': None}
                for th in sc.get('threads', []):
                    if isinstance(th, dict):
                        entry['threads'].append('%s(cpuset=%s,%s,prio=%s)' % (
                            first(th, 'name'), first(th, 'cpuset'), first(th, 'policy'), first(th, 'prio')))
                cc = first(sc, 'classic_conf', {})
                if isinstance(cc, dict):
                    for g in cc.get('groups', []):
                        if isinstance(g, dict):
                            tasks = [t for t in g.get('tasks', []) if isinstance(t, dict)]
                            prios = [int(first(t, 'prio', '0')) for t in tasks]
                            entry['groups'].append({
                                'name': first(g, 'name'), 'processor_num': first(g, 'processor_num'),
                                'affinity': first(g, 'affinity'), 'cpuset': first(g, 'cpuset'),
                                'policy': first(g, 'processor_policy'), 'prio': first(g, 'processor_prio'),
                                'n_tasks': len(tasks),
                                'prio_range': '%d-%d' % (min(prios), max(prios)) if prios else '-',
                                'tasks': [first(t, 'name') for t in tasks]})
                ch = first(sc, 'choreography_conf', {})
                if isinstance(ch, dict) and ch:
                    tasks = [t for t in ch.get('tasks', []) if isinstance(t, dict)]
                    pinned = [t for t in tasks if first(t, 'processor')]
                    entry['choreo'] = {
                        'choreography_processor_num': first(ch, 'choreography_processor_num'),
                        'choreography_cpuset': first(ch, 'choreography_cpuset'),
                        'choreography_affinity': first(ch, 'choreography_affinity'),
                        'choreography_policy': first(ch, 'choreography_processor_policy'),
                        'pool_processor_num': first(ch, 'pool_processor_num'),
                        'pool_cpuset': first(ch, 'pool_cpuset'),
                        'pool_policy': first(ch, 'pool_processor_policy'),
                        'n_tasks': len(tasks), 'n_pinned': len(pinned),
                        'tasks': ['%s@p%s(prio %s)' % (first(t, 'name'), first(t, 'processor', '-'), first(t, 'prio', '-')) for t in tasks]}
                out['sched'].append(entry)
            tc = first(msg, 'transport_conf', {})
            if isinstance(tc, dict) and tc:
                cm = first(tc, 'communication_mode', {})
                shm = first(tc, 'shm_conf', {})
                arena = []
                if isinstance(shm, dict):
                    a = first(shm, 'arena_shm_conf', {})
                    if isinstance(a, dict):
                        for acc in a.get('arena_channel_conf', []):
                            if isinstance(acc, dict):
                                arena.append('%s(max_msg_size=%s,max_pool_size=%s)' % (
                                    first(acc, 'channel_name'), first(acc, 'max_msg_size'), first(acc, 'max_pool_size')))
                out['transport'][fn] = {
                    'same_proc': first(cm, 'same_proc') if isinstance(cm, dict) else '',
                    'diff_proc': first(cm, 'diff_proc') if isinstance(cm, dict) else '',
                    'diff_host': first(cm, 'diff_host') if isinstance(cm, dict) else '',
                    'shm_notifier': first(shm, 'notifier_type') if isinstance(shm, dict) else '',
                    'shm_type': first(shm, 'shm_type') if isinstance(shm, dict) else '',
                    'arena': arena,
                    'run_mode': first(first(msg, 'run_mode_conf', {}), 'run_mode') if isinstance(first(msg, 'run_mode_conf', {}), dict) else '',
                }
    cyber_root = os.path.join(root, 'cyber')
    if os.path.isdir(cyber_root):
        for path in walk(cyber_root):
            lang = lang_of(path)
            if lang in ('C++', 'C/C++ header', 'Python', 'Proto', 'Assembly', 'C'):
                sub = rel(cyber_root, path).split(os.sep)[0]
                if os.path.isdir(os.path.join(cyber_root, sub)):
                    out['subdirs'][sub] += read_text(path).count('\n')
    return out


# --------------------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------------------
MAIN_PIPELINE_MODULES = ['modules/drivers', 'modules/localization', 'modules/perception', 'modules/prediction',
                         'modules/planning', 'modules/control', 'modules/canbus', 'modules/routing',
                         'modules/external_command', 'modules/transform', 'modules/guardian']
CORE_PIPELINE = ['modules/perception', 'modules/prediction', 'modules/planning', 'modules/control',
                 'modules/canbus', 'modules/localization', 'modules/routing', 'modules/external_command']


def git_info(root):
    def run(*args):
        try:
            return subprocess.check_output(['git', '-C', root] + list(args), stderr=subprocess.DEVNULL).decode().strip()
        except Exception:
            return '(n/a)'
    return {'commit': run('rev-parse', 'HEAD'), 'date': run('log', '-1', '--format=%ci'),
            'subject': run('log', '-1', '--format=%s')}


def md_table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---'] * len(headers)) + '|']
    for r in rows:
        lines.append('| ' + ' | '.join(str(c).replace('|', '\\|') for c in r) + ' |')
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    root = os.path.abspath(sys.argv[1])
    out_path = None
    if '--out' in sys.argv:
        out_path = sys.argv[sys.argv.index('--out') + 1]

    gi = git_info(root)
    scan = scan_sources(root)
    dag_files = sorted(rel(root, p) for p in walk(root) if p.endswith('.dag'))
    comps = []
    for d in dag_files:
        comps.extend(parse_dag(root, os.path.join(root, d)))
    for c in comps:
        infer_channels(root, c, scan)

    all_channels = set()
    for c in comps:
        for ch, _ in c['inputs'] + c['outputs']:
            if not ch.startswith('<'):
                all_channels.add(ch)
    n_timer = sum(1 for c in comps if c['kind'] == 'timer')
    unique_classes = sorted({c['class_name'] for c in comps})

    L = []
    L.append('# Apollo static anatomy (auto-generated by apollo_dag_graph.py)')
    L.append('')
    L.append('- generated: %s' % datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
    L.append('- repo root: `%s`' % root)
    L.append('- commit: `%s` (%s) "%s"' % (gi['commit'], gi['date'], gi['subject']))
    L.append('- command: `python3 %s %s`' % (os.path.basename(sys.argv[0]), ' '.join(sys.argv[1:])))
    L.append('- note: third_party/ is excluded from LOC and GPU scans; .git excluded.')
    L.append('')
    L.append('## 1. Headline numbers')
    L.append('')
    L.append(md_table(['metric', 'value'], [
        ['.dag files', len(dag_files)],
        ['component instances declared in .dag (components + timer_components)', len(comps)],
        ['  of which timer_components', n_timer],
        ['distinct component class_names in .dag', len(unique_classes)],
        ['CYBER_REGISTER_COMPONENT() occurrences in C++ sources', len(scan['registered'])],
        ['distinct channels referenced (dag readers + inferred writers/readers)', len(all_channels)],
        ['.proto files', len(scan['proto_files'])],
        ['BUILD files (BUILD / BUILD.bazel)', scan['build_files']],
        ['Bazel targets (rule invocations in BUILD files)', sum(scan['build_rule_kinds'].values())],
        ['DEFINE_string gflags found (used to resolve FLAGS_*_topic)', len(scan['flags'])],
    ]))
    L.append('')
    L.append('Top Bazel rule kinds: ' + ', '.join('%s=%d' % kv for kv in scan['build_rule_kinds'].most_common(12)))
    L.append('')

    # ---- per-module LOC
    L.append('## 2. LOC by top-level directory and language (lines incl. blanks/comments)')
    L.append('')
    L.append('Files under directories named %s are excluded from the language columns and shown in the last column.' % '/'.join(sorted(TESTDATA_DIRS)))
    L.append('')
    langs = ['C++', 'C/C++ header', 'CUDA', 'Python', 'Proto', 'JS/TS', 'Shell', 'Bazel',
             'Config(pb.txt/conf/dag/launch/flag)', 'Markdown']
    dag_count = Counter(top_module(d) for d in dag_files)
    comp_count = Counter(c['module'] for c in comps)
    reg_count = Counter(top_module(p) for p in scan['registered'].values())
    rows = []
    for mod in sorted(scan['loc'], key=lambda m: -sum(scan['loc'][m].values())):
        lc = scan['loc'][mod]
        rows.append([mod, sum(lc.values())] + [lc.get(l, 0) for l in langs] +
                    [dag_count.get(mod, 0), comp_count.get(mod, 0), reg_count.get(mod, 0),
                     scan['build_targets_by_module'].get(mod, 0), scan['testdata_loc'].get(mod, 0)])
    L.append(md_table(['dir', 'total LOC'] + langs + ['.dag files', 'dag comp decls', 'CYBER_REGISTER', 'bazel targets', 'testdata LOC (excluded)'], rows))
    L.append('')

    # ---- GPU usage
    L.append('## 3. GPU / inference-runtime usage per directory (number of files matching pattern)')
    L.append('')
    gnames = list(GPU_PATTERNS.keys())
    rows = []
    for mod in sorted(scan['loc'], key=lambda m: -sum(scan['gpu_hits'][m].values()) - scan['cu_files'][m]):
        hits = scan['gpu_hits'][mod]
        if sum(hits.values()) == 0 and scan['cu_files'][mod] == 0:
            continue
        rows.append([mod, scan['cu_files'][mod]] + [hits.get(g, 0) for g in gnames])
    L.append(md_table(['dir', '.cu files'] + gnames, rows))
    L.append('')
    L.append('Patterns: ' + '; '.join('%s=`%s`' % (k, v.pattern.replace('|', ' \\| ')) for k, v in GPU_PATTERNS.items()))
    L.append('')

    # ---- cyber summary
    cy = cyber_summary(root)
    L.append('## 4. cyber/ (Cyber RT) summary')
    L.append('')
    L.append('LOC per cyber sub-directory (C++/headers/python/proto/asm):')
    L.append('')
    L.append(md_table(['cyber/<sub>', 'LOC'], [[k, v] for k, v in cy['subdirs'].most_common()]))
    L.append('')
    L.append('### 4.1 scheduler configs under cyber/conf')
    L.append('')
    for e in cy['sched']:
        L.append('- **%s**: policy=`%s` routine_num=%s default_proc_num=%s process_level_cpuset=%s threads=[%s]' % (
            e['file'], e['policy'], e['routine_num'] or '-', e['default_proc_num'] or '-',
            e['process_level_cpuset'] or '-', ', '.join(e['threads']) or '-'))
        for g in e['groups']:
            L.append('  - classic group `%s`: processor_num=%s affinity=%s cpuset=%s policy=%s prio=%s tasks=%d (task prio range %s)' % (
                g['name'], g['processor_num'], g['affinity'], g['cpuset'], g['policy'], g['prio'], g['n_tasks'], g['prio_range']))
            L.append('    - tasks: ' + ', '.join(g['tasks']))
        if e['choreo']:
            c = e['choreo']
            L.append('  - choreography: choreography_processor_num=%s cpuset=%s affinity=%s policy=%s | pool_processor_num=%s pool_cpuset=%s pool_policy=%s | tasks=%d (pinned to a processor: %d)' % (
                c['choreography_processor_num'], c['choreography_cpuset'], c['choreography_affinity'], c['choreography_policy'] or '-',
                c['pool_processor_num'], c['pool_cpuset'], c['pool_policy'] or '-', c['n_tasks'], c['n_pinned']))
            L.append('    - tasks: ' + ', '.join(c['tasks']))
    L.append('')
    L.append('### 4.2 transport config')
    L.append('')
    for fn, t in cy['transport'].items():
        L.append('- **cyber/conf/%s**: same_proc=%s diff_proc=%s diff_host=%s shm_notifier=%s shm_type=%s run_mode=%s arena=[%s]' % (
            fn, t['same_proc'], t['diff_proc'], t['diff_host'], t['shm_notifier'] or '(default)', t['shm_type'] or '(default)',
            t['run_mode'], ', '.join(t['arena'])))
    L.append('')

    # ---- component table
    L.append('## 5. Components declared in .dag files (all)')
    L.append('')
    rows = []
    for c in sorted(comps, key=lambda c: (c['module'], c['dag'])):
        rows.append([c['dag'], c['class_name'], c['name'], c['kind'] + ('(%sms)' % c['interval_ms'] if c['interval_ms'] else ''),
                     '<br>'.join(ch for ch, _ in c['inputs']) or '-', '<br>'.join(ch for ch, _ in c['outputs']) or '-'])
    L.append(md_table(['dag', 'class', 'name', 'kind', 'inputs (dag readers + code)', 'outputs (inferred)'], rows))
    L.append('')

    # ---- main pipeline edges
    L.append('## 6. Main driving pipeline: component -> channel edges')
    L.append('')
    L.append('Scope: components whose .dag lives under ' + ', '.join(CORE_PIPELINE) + ' (perception uses one dag per class; duplicates of the same class from variant dags are merged).')
    L.append('')
    seen = set()
    edges = []  # (src_node, channel, dst_node, evidence)
    nodes = OrderedDict()
    for c in comps:
        if c['module'] not in CORE_PIPELINE:
            continue
        key = c['class_name']
        if key in seen:
            continue
        seen.add(key)
        nodes[key] = c
    rows = []
    for key, c in nodes.items():
        for ch, ev in c['inputs']:
            rows.append([key, 'reads', ch, ev])
        for ch, ev in c['outputs']:
            rows.append([key, 'writes', ch, ev])
    L.append(md_table(['component class', 'dir', 'channel', 'evidence'], rows))
    L.append('')
    # derived component->component edges via shared channels
    writers_of = defaultdict(list)
    for key, c in nodes.items():
        for ch, _ in c['outputs']:
            if not ch.startswith('<'):
                writers_of[ch].append(key)
    c2c = []
    for key, c in nodes.items():
        for ch, _ in c['inputs']:
            for w in writers_of.get(ch, []):
                if w != key:
                    c2c.append((w, ch, key))
    L.append('### 6.1 Derived component -> component edges (writer of a channel -> reader of the same channel)')
    L.append('')
    L.append(md_table(['from', 'channel', 'to'], [[a, b, d] for a, b, d in c2c]))
    L.append('')
    L.append('### 6.2 DOT graph')
    L.append('')
    L.append('```dot')
    L.append('digraph apollo_pipeline {')
    L.append('  rankdir=LR; node [shape=box, fontsize=10];')
    color = {'modules/perception': 'lightblue', 'modules/prediction': 'lightyellow', 'modules/planning': 'lightgreen',
             'modules/control': 'salmon', 'modules/canbus': 'grey85', 'modules/localization': 'thistle',
             'modules/routing': 'wheat', 'modules/external_command': 'wheat'}
    for key, c in nodes.items():
        L.append('  "%s" [style=filled, fillcolor=%s, label="%s\\n(%s)"];' % (key, color.get(c['module'], 'white'), key, c['module'].split('/')[-1]))
    for a, ch, d in c2c:
        L.append('  "%s" -> "%s" [label="%s", fontsize=8];' % (a, d, ch))
    # external inputs (channels read but not written by any node in scope)
    ext = sorted({ch for key, c in nodes.items() for ch, _ in c['inputs'] if ch not in writers_of and not ch.startswith('<')})
    for ch in ext:
        L.append('  "%s" [shape=ellipse, fontsize=8];' % ch)
    for key, c in nodes.items():
        for ch, _ in c['inputs']:
            if ch in ext:
                L.append('  "%s" -> "%s";' % (ch, key))
    L.append('}')
    L.append('```')
    L.append('')

    # ---- unresolved
    unres = [(c['class_name'], c['dag'], k, t, e) for c in comps for (k, t, e) in c['unresolved']]
    L.append('## 7. Unresolved channel expressions (could not map to a string statically)')
    L.append('')
    L.append('Typically the dag instance points at a config file that lacks the topic field, or the channel is built at runtime.')
    L.append('')
    L.append(md_table(['component', 'dag instance', 'kind', 'msg type', 'expression'], sorted(set(unres))) if unres else '(none)')
    L.append('')
    L.append('## 8. Channel inventory (all distinct channel strings seen)')
    L.append('')
    L.append(', '.join('`%s`' % ch for ch in sorted(all_channels)))
    L.append('')

    report = '\n'.join(L)
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print('wrote', out_path, len(report), 'bytes')
    else:
        print(report)


if __name__ == '__main__':
    main()
