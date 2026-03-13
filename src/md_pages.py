"""
Markdown page processor: single pipeline for all .md pages.
Load file → @include → @directives → markdown → HTML.
Used by build.py for home, about, resources, internal pages.
"""

import re
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None


def _display_number(num):
    """Strip leading zeros for display; used in sample seed rows."""
    if num and num.isdigit():
        return str(int(num))
    return num or "?"


def expand_includes(text, base_dir, warn=None):
    """Replace lines @include filename with file contents from base_dir. Paths resolved under base_dir."""
    if warn is None:
        warn = lambda msg: None
    base_dir = Path(base_dir).resolve()
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("@include "):
            name = stripped[8:].strip()
            inc_path = (base_dir / name).resolve()
            if not str(inc_path).startswith(str(base_dir)):
                warn(f"Warning: @include {name!r} resolves outside {base_dir}")
                continue
            if not inc_path.exists():
                warn(f"Warning: @include {name!r} not found")
                continue
            out.append(inc_path.read_text(encoding="utf-8"))
        else:
            out.append(line)
    return "\n".join(out)


def _render_samples_html(nuggets, status_order, copy, count=5, full_section=False):
    """Render sample seed rows (or full seed-list-section when full_section=True). copy = index.txt dict."""
    status_rank = {s: i for i, s in enumerate(status_order)}
    key_status = lambda n: status_rank.get(n.get("status", "empty"), len(status_order))
    key_num = lambda n: int(n.get("number", "0")) if (n.get("number") or "").isdigit() else 0
    by_ready = sorted(nuggets, key=lambda n: (key_status(n), key_num(n)))
    recent = by_ready[:count]
    d = "d/"
    rows_html = ""
    for n in recent:
        fname = n.get("filename", "") + ".html"
        num = n.get("number", "")
        title = n.get("title", "")
        subtitle = n.get("subtitle", "")
        status = n.get("status", "empty")
        stub = " stub" if status == "empty" else ""
        rows_html += f"""
    <a href="{d}{fname}" class="seed-row{stub}">
      <div class="seed-num">{_display_number(num)}</div>
      <div>
        <div class="seed-title">{title}</div>
        <div class="seed-sub">{subtitle}</div>
      </div>
      <div class="seed-status-col">{status}</div>
    </a>"""
    if not full_section:
        return rows_html.strip()
    total = len(nuggets)
    view_all_text = (copy.get("view_all") or "View all {n} seeds →").replace("{n}", str(total))
    return f"""
  <div class="seed-list-section">
    <div class="section-head">
      <span class="mono small">{copy.get("section_head", "All seeds")}</span>
      <a href="{d}list.html" class="link-mono-small">{copy.get("repo_link", "Full repository →")}</a>
    </div>
    {rows_html}
    <div class="seed-list-more-wrap">
      <a href="{d}list.html" class="link-mono-accent">{view_all_text}</a>
    </div>
  </div>"""


def expand_page_directives(text, context):
    """Replace @directives in page content. Returns (text_with_placeholders, {placeholder: html}).
    context: nuggets, status_order, copy (from index.txt), build_time, page.
    @timestamp is replaced everywhere it appears (whole line or inline)."""
    if not text:
        return text, {}
    nuggets = context.get("nuggets") or []
    status_order = context.get("status_order") or []
    copy = context.get("copy") or {}
    build_time = context.get("build_time")
    page = context.get("page")
    timestamp_str = build_time.strftime("%Y-%m-%d %H:%M Pacific") if build_time else None
    out = []
    replacements = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("@samples"):
            rest = stripped[7:].strip()
            count = 5
            if rest.isdigit():
                count = min(int(rest), 50)
            if nuggets and status_order:
                full = page == "home"
                block = _render_samples_html(nuggets, status_order, copy, count=count, full_section=full)
                placeholder = "{{SAMPLES}}"
                replacements[placeholder] = block
                out.append(placeholder)
            continue
        if stripped == "@timestamp" and timestamp_str:
            out.append(timestamp_str)
            continue
        if timestamp_str and "@timestamp" in line:
            line = line.replace("@timestamp", timestamp_str)
        out.append(line)
    return "\n".join(out), replacements


def process_md_to_html(md_path, context=None):
    """Single pipeline for .md → HTML: load file, @include, @directives, markdown. Returns body HTML.
    context: copy (index.txt), nuggets, status_order, page, build_time, warn (callable)."""
    if context is None:
        context = {}
    if not md_path.exists():
        raise SystemExit(f"Missing markdown file: {md_path}")
    if markdown is None:
        raise SystemExit(
            "Markdown pages require the markdown package.\n"
            "  pip install markdown\n"
            "Or in a venv: pip install -r requirements.txt"
        )
    raw = md_path.read_text(encoding="utf-8")
    base_dir = md_path.parent.resolve()
    warn = context.get("warn", lambda msg: None)
    raw = expand_includes(raw, base_dir, warn=warn)
    expanded, replacements = expand_page_directives(raw, context)
    for placeholder, block in replacements.items():
        expanded = expanded.replace(placeholder, block)
    if not expanded.strip():
        return ""
    html = markdown.markdown(
        expanded,
        extensions=["fenced_code", "tables"],
        extension_configs={"fenced_code": {}},
    )
    html = re.sub(
        r'<p>(TBD|No reviews completed yet\.)</p>',
        r'<p class="dim placeholder">\1</p>',
        html,
    )
    return html
