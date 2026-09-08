#!/usr/bin/env python3
"""Static anatomy of the Autoware source tree (stdlib only).

Usage:
    python3 autoware_anatomy.py <clone_root> [--launch-root autoware.launch.xml] [--depth 4]

<clone_root> must contain shallow clones of (a subset of):
    autoware, autoware_core, autoware_universe, autoware_launch,
    autoware_msgs, autoware_adapi_msgs, autoware_internal_msgs

The script prints a markdown report to stdout. It measures, per repo and per
top-level module directory:
  * ROS packages (package.xml)
  * node registrations  (RCLCPP_COMPONENTS_REGISTER_NODE / "public rclcpp::Node")
  * launch files (*.launch.xml / *.launch.py)
  * .msg/.srv/.action interface files
  * LOC by language (cpp / hpp / py / cu)
  * package.xml dependency edges (<depend>, <build_depend>, <exec_depend>, ...)
  * top-N most-depended packages
  * mentions of agnocast / cuda_blackboard / tensorrt / onnx per package
  * a static include tree of autoware_launch starting at autoware.launch.xml

Everything is a *static* text measurement: no ROS/colcon needed, nothing runs.
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
REPOS_DEFAULT = [
    "autoware",
    "autoware_core",
    "autoware_universe",
    "autoware_launch",
    "autoware_msgs",
    "autoware_adapi_msgs",
    "autoware_internal_msgs",
]
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", "build", "install", "log"}
LANG_EXT = {
    "cpp": {".cpp", ".cc", ".cxx", ".c"},
    "hpp": {".hpp", ".h", ".hh", ".hxx"},
    "py": {".py"},
    "cu": {".cu", ".cuh"},
}
SRC_EXT = set().union(*LANG_EXT.values())
DEP_TAGS = (
    "depend",
    "build_depend",
    "build_export_depend",
    "exec_depend",
    "test_depend",
    "buildtool_depend",
    "doc_depend",
)
TECH_PATTERNS = {
    "agnocast": re.compile(r"agnocast", re.I),
    "cuda_blackboard": re.compile(r"cuda_blackboard", re.I),
    "tensorrt": re.compile(r"tensorrt|nvinfer", re.I),
    "onnx": re.compile(r"\bonnx", re.I),
}
RE_REGISTER = re.compile(r"RCLCPP_COMPONENTS_REGISTER_NODE\s*\(")
RE_PUBLIC_NODE = re.compile(r"public\s+rclcpp::(?:Node|LifecycleNode)\b|public\s+rclcpp_lifecycle::LifecycleNode\b")
RE_INCLUDE_XML = re.compile(r"<include\s[^>]*?file\s*=\s*\"([^\"]+)\"", re.S)
RE_FIND_PKG = re.compile(r"\$\(find-pkg-share\s+([^)]+)\)")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def git_info(path: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", path, "log", "-1", "--format=%h %cI"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return out
    except Exception:  # noqa: BLE001
        return "n/a"


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def count_loc(path: str) -> int:
    n = 0
    try:
        with open(path, "rb") as fh:
            for line in fh:
                if line.strip():
                    n += 1
    except OSError:
        pass
    return n


def walk(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        yield dirpath, dirnames, filenames


class Pkg:
    __slots__ = (
        "name",
        "repo",
        "module",
        "dir",
        "deps",
        "dep_tags",
        "register_nodes",
        "public_nodes",
        "launch_xml",
        "launch_py",
        "msg",
        "srv",
        "action",
        "loc",
        "tech",
        "files",
    )

    def __init__(self, name, repo, module, d):
        self.name = name
        self.repo = repo
        self.module = module
        self.dir = d
        self.deps = []
        self.dep_tags = collections.Counter()
        self.register_nodes = 0
        self.public_nodes = 0
        self.launch_xml = 0
        self.launch_py = 0
        self.msg = 0
        self.srv = 0
        self.action = 0
        self.loc = collections.Counter()
        self.tech = set()
        self.files = 0


def parse_package_xml(path: str):
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return None, [], collections.Counter()
    root = tree.getroot()
    name_el = root.find("name")
    name = name_el.text.strip() if name_el is not None and name_el.text else None
    deps = []
    tags = collections.Counter()
    for tag in DEP_TAGS:
        for el in root.findall(tag):
            if el.text:
                deps.append((tag, el.text.strip()))
                tags[tag] += 1
    return name, deps, tags


# --------------------------------------------------------------------------- #
# Scan
# --------------------------------------------------------------------------- #
def discover_packages(clone_root: str, repos: list[str]) -> list[Pkg]:
    pkgs: list[Pkg] = []
    for repo in repos:
        rroot = os.path.join(clone_root, repo)
        if not os.path.isdir(rroot):
            continue
        for dirpath, dirnames, filenames in walk(rroot):
            if "COLCON_IGNORE" in filenames:
                dirnames[:] = []
                continue
            if "package.xml" in filenames:
                name, deps, tags = parse_package_xml(os.path.join(dirpath, "package.xml"))
                if not name:
                    continue
                rel = os.path.relpath(dirpath, rroot)
                module = rel.split(os.sep)[0] if rel != "." else "."
                p = Pkg(name, repo, module, dirpath)
                p.deps = deps
                p.dep_tags = tags
                pkgs.append(p)
                # do not descend into nested packages? ROS allows nested; keep walking
    return pkgs


def scan_package(p: Pkg):
    for dirpath, _dirnames, filenames in walk(p.dir):
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            p.files += 1
            ext = os.path.splitext(fn)[1].lower()
            if fn.endswith(".launch.xml"):
                p.launch_xml += 1
            elif fn.endswith(".launch.py"):
                p.launch_py += 1
            if ext == ".msg":
                p.msg += 1
            elif ext == ".srv":
                p.srv += 1
            elif ext == ".action":
                p.action += 1
            if ext in SRC_EXT:
                for lang, exts in LANG_EXT.items():
                    if ext in exts:
                        p.loc[lang] += count_loc(fp)
                        break
                if ext in LANG_EXT["cpp"] or ext in LANG_EXT["hpp"] or ext in LANG_EXT["cu"]:
                    txt = read_text(fp)
                    p.register_nodes += len(RE_REGISTER.findall(txt))
                    p.public_nodes += len(RE_PUBLIC_NODE.findall(txt))
                    for k, rx in TECH_PATTERNS.items():
                        if k not in p.tech and rx.search(txt):
                            p.tech.add(k)
            if fn in ("package.xml", "CMakeLists.txt"):
                txt = read_text(fp)
                for k, rx in TECH_PATTERNS.items():
                    if k not in p.tech and rx.search(txt):
                        p.tech.add(k)


# --------------------------------------------------------------------------- #
# Launch include tree
# --------------------------------------------------------------------------- #
def build_pkg_index(pkgs: list[Pkg]) -> dict[str, str]:
    idx = {}
    for p in pkgs:
        idx.setdefault(p.name, p.dir)
    return idx


def resolve_launch_path(expr: str, pkg_index: dict[str, str]) -> tuple[str | None, str]:
    """Return (abs_path_or_None, display)."""
    m = RE_FIND_PKG.search(expr)
    if not m:
        return None, expr
    pkg = m.group(1).strip()
    rest = expr[m.end():].lstrip("/")
    if "$(" in pkg or "$(" in rest:
        # dynamic (e.g. $(var sensor_model)_launch) -> cannot resolve statically
        return None, expr
    base = pkg_index.get(pkg)
    if base is None:
        return None, expr
    return os.path.join(base, rest), f"{pkg}/{rest}"


def launch_tree(start: str, pkg_index: dict[str, str], max_depth: int, clone_root: str):
    """Yield (depth, display, status, n_children) lines by DFS."""
    lines = []
    seen_stack = []

    def rel(p):
        return os.path.relpath(p, clone_root)

    def visit(path: str, display: str, depth: int):
        if not os.path.isfile(path):
            lines.append((depth, display, "MISSING"))
            return
        if path.endswith(".launch.py"):
            lines.append((depth, display, "py-leaf"))
            return
        txt = read_text(path)
        incs = RE_INCLUDE_XML.findall(txt)
        lines.append((depth, display, f"{len(incs)} includes"))
        if depth >= max_depth:
            return
        if path in seen_stack:
            lines.append((depth + 1, "(cycle)", ""))
            return
        seen_stack.append(path)
        for inc in incs:
            child, disp = resolve_launch_path(inc, pkg_index)
            if child is None:
                lines.append((depth + 1, disp, "UNRESOLVED(dynamic/pkg-not-cloned)"))
            else:
                visit(child, disp, depth + 1)
        seen_stack.pop()

    visit(start, rel(start), 0)
    return lines


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clone_root")
    ap.add_argument("--repos", nargs="*", default=REPOS_DEFAULT)
    ap.add_argument("--launch-root", default="autoware_launch/autoware_launch/launch/autoware.launch.xml")
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    clone_root = os.path.abspath(args.clone_root)
    repos = [r for r in args.repos if os.path.isdir(os.path.join(clone_root, r))]

    print("# Autoware static anatomy report")
    print()
    print(f"- generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"- python: {sys.version.split()[0]}")
    print(f"- clone_root: `{clone_root}`")
    print()
    print("## Repositories scanned")
    print()
    print(md_table(["repo", "HEAD (short hash, commit date)", "LICENSE (1st line)"],
                   [(r, git_info(os.path.join(clone_root, r)),
                     (read_text(os.path.join(clone_root, r, "LICENSE")).strip().splitlines() or ["n/a"])[0].strip())
                    for r in repos]))
    print()

    # autoware.repos listing
    repos_file = os.path.join(clone_root, "autoware", "repositories", "autoware.repos")
    if os.path.isfile(repos_file):
        print("## autoware.repos manifest (meta repo)")
        print()
        rows = []
        cur = None
        for line in read_text(repos_file).splitlines():
            m = re.match(r"^  ([A-Za-z0-9_./-]+):\s*(#.*)?$", line)
            if m:
                cur = [m.group(1), "", ""]
                rows.append(cur)
                continue
            if cur is not None:
                mu = re.match(r"^\s+url:\s*(\S+)", line)
                mv = re.match(r"^\s+version:\s*(\S+)", line)
                if mu:
                    cur[1] = mu.group(1)
                if mv:
                    cur[2] = mv.group(1)
        groups = collections.Counter(r[0].split("/")[0] for r in rows)
        print(f"- entries: {len(rows)}  by group: " + ", ".join(f"{k}={v}" for k, v in sorted(groups.items())))
        print()
        print(md_table(["path (group/name)", "url", "version"], rows))
        print()

    pkgs = discover_packages(clone_root, repos)
    for p in pkgs:
        scan_package(p)

    # ---------------- per repo summary
    print("## Per-repo summary")
    print()
    rows = []
    tot = collections.Counter()
    for r in repos:
        ps = [p for p in pkgs if p.repo == r]
        c = collections.Counter()
        for p in ps:
            c["pkgs"] += 1
            c["reg"] += p.register_nodes
            c["pub"] += p.public_nodes
            c["lx"] += p.launch_xml
            c["lp"] += p.launch_py
            c["msg"] += p.msg
            c["srv"] += p.srv
            c["act"] += p.action
            for lang in LANG_EXT:
                c[lang] += p.loc[lang]
            c["deps"] += len(p.deps)
        tot.update(c)
        rows.append((r, c["pkgs"], c["reg"], c["pub"], c["lx"], c["lp"], c["msg"], c["srv"], c["act"],
                     c["cpp"], c["hpp"], c["py"], c["cu"], c["deps"]))
    rows.append(("**TOTAL**", tot["pkgs"], tot["reg"], tot["pub"], tot["lx"], tot["lp"], tot["msg"], tot["srv"],
                 tot["act"], tot["cpp"], tot["hpp"], tot["py"], tot["cu"], tot["deps"]))
    print(md_table(["repo", "pkgs", "REGISTER_NODE", "public rclcpp::Node", "launch.xml", "launch.py",
                    "msg", "srv", "action", "LOC cpp", "LOC hpp", "LOC py", "LOC cu", "dep edges"], rows))
    print()

    # ---------------- per module (repo/module)
    print("## Per top-level module directory")
    print()
    rows = []
    bymod = collections.defaultdict(list)
    for p in pkgs:
        bymod[(p.repo, p.module)].append(p)
    for (r, m), ps in sorted(bymod.items()):
        c = collections.Counter()
        for p in ps:
            c["pkgs"] += 1
            c["reg"] += p.register_nodes
            c["pub"] += p.public_nodes
            c["lx"] += p.launch_xml
            c["lp"] += p.launch_py
            c["msg"] += p.msg + p.srv + p.action
            for lang in LANG_EXT:
                c[lang] += p.loc[lang]
            c["deps"] += len(p.deps)
        rows.append((r, m, c["pkgs"], c["reg"], c["pub"], c["lx"], c["lp"], c["msg"],
                     c["cpp"], c["hpp"], c["py"], c["cu"], c["deps"]))
    print(md_table(["repo", "module", "pkgs", "REGISTER_NODE", "public rclcpp::Node", "launch.xml", "launch.py",
                    "msg+srv+action", "LOC cpp", "LOC hpp", "LOC py", "LOC cu", "dep edges"], rows))
    print()

    # ---------------- msgs detail
    print("## Interface packages (msg/srv/action per package)")
    print()
    rows = [(p.repo, p.name, p.msg, p.srv, p.action) for p in pkgs if (p.msg + p.srv + p.action) > 0]
    rows.sort(key=lambda x: (x[0], -(x[2] + x[3] + x[4])))
    print(md_table(["repo", "package", "msg", "srv", "action"], rows))
    print()

    # ---------------- dependency graph
    print("## Dependency edges (package.xml)")
    print()
    tagcount = collections.Counter()
    for p in pkgs:
        tagcount.update(p.dep_tags)
    print("- edges by tag: " + ", ".join(f"`<{k}>`={v}" for k, v in tagcount.most_common()))
    internal = {p.name for p in pkgs}
    indeg = collections.Counter()
    indeg_int_src = collections.Counter()
    for p in pkgs:
        for _tag, d in set(p.deps):
            indeg[d] += 1
    n_int = sum(1 for p in pkgs for _t, d in set(p.deps) if d in internal)
    n_ext = sum(1 for p in pkgs for _t, d in set(p.deps) if d not in internal)
    print(f"- unique (src,dst) edges: internal(dst cloned)={n_int}, external(dst not cloned: rclcpp, pcl, ...)={n_ext}")
    print()
    print(f"### Top-{args.top} most-depended packages (all)")
    print()
    print(md_table(["rank", "package", "in-degree", "cloned?"],
                   [(i + 1, n, c, "yes" if n in internal else "no")
                    for i, (n, c) in enumerate(indeg.most_common(args.top))]))
    print()
    print(f"### Top-{args.top} most-depended packages (cloned Autoware packages only)")
    print()
    print(md_table(["rank", "package", "in-degree", "repo/module"],
                   [(i + 1, n, c, next((f"{p.repo}/{p.module}" for p in pkgs if p.name == n), "?"))
                    for i, (n, c) in enumerate([(n, c) for n, c in indeg.most_common() if n in internal][:args.top])]))
    print()
    # out-degree top
    print("### Top-10 packages by out-degree (most dependencies declared)")
    print()
    print(md_table(["package", "repo/module", "#deps"],
                   [(p.name, f"{p.repo}/{p.module}", len(set(d for _t, d in p.deps)))
                    for p in sorted(pkgs, key=lambda q: -len(set(d for _t, d in q.deps)))[:10]]))
    print()

    # ---------------- tech mentions
    print("## Technology mentions (agnocast / cuda_blackboard / tensorrt / onnx)")
    print()
    for k in TECH_PATTERNS:
        users = sorted((p for p in pkgs if k in p.tech), key=lambda q: (q.repo, q.module, q.name))
        print(f"### {k}: {len(users)} packages")
        print()
        bym = collections.Counter(f"{p.repo}/{p.module}" for p in users)
        print("- by module: " + (", ".join(f"{m}={c}" for m, c in bym.most_common()) or "(none)"))
        print("- packages: " + (", ".join(f"`{p.name}`" for p in users) or "(none)"))
        print()

    # ---------------- node registration detail (top)
    print("## Packages with most node registrations (RCLCPP_COMPONENTS_REGISTER_NODE)")
    print()
    print(md_table(["package", "repo/module", "REGISTER_NODE", "public rclcpp::Node", "LOC cpp+hpp+cu"],
                   [(p.name, f"{p.repo}/{p.module}", p.register_nodes, p.public_nodes,
                     p.loc["cpp"] + p.loc["hpp"] + p.loc["cu"])
                    for p in sorted(pkgs, key=lambda q: -q.register_nodes)[:15]]))
    print()
    print("## Largest packages by LOC (cpp+hpp+cu+py)")
    print()
    print(md_table(["package", "repo/module", "LOC total", "cpp", "hpp", "cu", "py"],
                   [(p.name, f"{p.repo}/{p.module}", sum(p.loc.values()), p.loc["cpp"], p.loc["hpp"], p.loc["cu"], p.loc["py"])
                    for p in sorted(pkgs, key=lambda q: -sum(q.loc.values()))[:15]]))
    print()

    # ---------------- launch tree
    start = os.path.join(clone_root, args.launch_root)
    print(f"## Static launch include tree (depth <= {args.depth}) from `{args.launch_root}`")
    print()
    print("Legend: `N includes` = number of `<include file=...>` in the file; `py-leaf` = .launch.py (not parsed); "
          "`UNRESOLVED` = path uses `$(var ...)` or package not in the clone set; `MISSING` = resolved path not found.")
    print()
    if os.path.isfile(start):
        pkg_index = build_pkg_index(pkgs)
        lines = launch_tree(start, pkg_index, args.depth, clone_root)
        print("```")
        for depth, disp, status in lines:
            print("  " * depth + f"- {disp}  [{status}]")
        print("```")
        st = collections.Counter(s.split("(")[0] for _d, _x, s in lines)
        print()
        print(f"- lines: {len(lines)}; resolved xml nodes: {sum(1 for _d,_x,s in lines if s.endswith('includes'))}, "
              f"py-leaf: {st['py-leaf']}, unresolved: {st['UNRESOLVED']}, missing: {st['MISSING']}")
    else:
        print(f"launch root not found: {start}")
    print()


if __name__ == "__main__":
    main()
