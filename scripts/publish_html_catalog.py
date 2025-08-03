#!/usr/bin/env python3
"""
publish_html_catalog.py

Generates subscotia_vault.html from your vault JSON, with:
 - Live search, dropdown filters (type/dev), sortable columns
 - Badge-style tags that you can click to filter by tag
 - Dark/light mode, responsive layout
 - Title: Subscotia Sound Vault
"""

import json
from datetime import datetime
from pathlib import Path

INPUT_JSON  = "ivault_master.json"
OUTPUT_HTML = "subscotia_vault.html"

def build_html(input_path: Path, output_path: Path):
    data = json.loads(input_path.read_text(encoding="utf-8"))
    types = sorted({item.get("type","") for item in data if item.get("type")})
    devs  = sorted({item.get("developer","") for item in data if item.get("developer")})
    now   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def wrap_tags(tags):
        if isinstance(tags, list):
            return " ".join(
                f'<span class="tag" data-tag="{tag.lower()}">{tag}</span>'
                for tag in tags
            )
        if isinstance(tags, str):
            t = tags.strip()
            return f'<span class="tag" data-tag="{t.lower()}">{t}</span>'
        return ""

    # start HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Subscotia Sound Vault</title>
  <style>
    :root {{ --bg:#f6f6f6; --fg:#222; --accent:#4f80ff; }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --bg:#1e1e1e; --fg:#ddd; --accent:#4f80ff; }}
    }}
    body {{
      background:var(--bg); color:var(--fg);
      font-family:sans-serif; margin:0; padding:1.5rem;
    }}
    h1 {{ margin:0; font-size:1.8rem; }}
    .updated {{ font-size:0.9rem; color:var(--accent); margin:0.2rem 0 1rem; }}

    #controls {{
      display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem;
    }}
    #controls input, #controls select {{
      padding:0.4rem; font-size:1rem;
      border:1px solid var(--accent); border-radius:4px;
      background:var(--bg); color:var(--fg);
    }}

    table {{
      width:100%; border-collapse:collapse; table-layout:fixed;
    }}
    th, td {{
      padding:0.5rem; border:1px solid var(--fg);
      overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
    }}
    th {{
      background:var(--accent); color:#fff; cursor:pointer;
    }}
    tr:nth-child(even) {{ background:rgba(0,0,0,0.04); }}
    tr.hidden {{ display:none; }}

    /* column widths */
    td:nth-child(5), th:nth-child(5) {{ width:40%; white-space:normal; }}
    td:nth-child(2), th:nth-child(2),
    td:nth-child(4), th:nth-child(4) {{ width:20%; }}

    /* tag badges */
    .tag {{
      display:inline-block;
      background:var(--accent); color:#fff;
      padding:0.2rem 0.5rem; margin:0.1rem 0.2rem 0.1rem 0;
      border-radius:4px; font-size:0.8rem;
      cursor:pointer;
      user-select:none;
    }}
    .tag.active {{
      background:#fff; color:var(--accent);
      border:1px solid var(--accent);
    }}
  </style>
</head>
<body>

  <h1>Subscotia Sound Vault</h1>
  <p class="updated">Last updated: {now}</p>
  <p>Total entries: {len(data)}</p>

  <div id="controls">
    <input id="searchBox" placeholder="Search…">
    <select id="typeFilter">
      <option value="">All Types</option>
      {''.join(f'<option value="{t}">{t}</option>' for t in types)}
    </select>
    <select id="devFilter">
      <option value="">All Developers</option>
      {''.join(f'<option value="{d}">{d}</option>' for d in devs)}
    </select>
  </div>

  <table id="vaultTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">ID</th>
        <th onclick="sortTable(1)">Name</th>
        <th onclick="sortTable(2)">Type</th>
        <th onclick="sortTable(3)">Developer</th>
        <th>Tags</th>
      </tr>
    </thead>
    <tbody>
"""
    # rows
    for item in data:
        rid   = item.get("id","")
        name  = item.get("name","")
        typ   = item.get("type","")
        dev   = item.get("developer","")
        tags  = item.get("tags", [])
        tag_html = wrap_tags(tags)
        # searchable text
        terms = " ".join(tags if isinstance(tags,list) else [str(tags)])
        search_text = f"{rid} {name} {typ} {dev} {terms}".lower()
        html += f"""
      <tr data-search="{search_text}" data-type="{typ}" data-dev="{dev}">
        <td>{rid}</td>
        <td>{name}</td>
        <td>{typ}</td>
        <td>{dev}</td>
        <td class="tags">{tag_html}</td>
      </tr>"""
    # close & JS
    html += """
    </tbody>
  </table>

  <script>
    const searchBox = document.getElementById("searchBox");
    const typeFilter = document.getElementById("typeFilter");
    const devFilter = document.getElementById("devFilter");
    const rows = Array.from(document.querySelectorAll("#vaultTable tbody tr"));
    let activeTag = "";

    function filterTable() {
      const terms = searchBox.value.toLowerCase().trim().split(/\\s+/);
      const tVal = typeFilter.value;
      const dVal = devFilter.value;

      rows.forEach(row => {
        const txt = row.dataset.search;
        const bySearch = terms.every(t => !t || txt.includes(t));
        const byType   = !tVal || row.dataset.type === tVal;
        const byDev    = !dVal || row.dataset.dev === dVal;
        const byTag    = !activeTag || txt.includes(activeTag);
        row.classList.toggle("hidden", !(bySearch && byType && byDev && byTag));
      });
    }

    // search + dropdowns
    searchBox.addEventListener("input", filterTable);
    typeFilter.addEventListener("change", filterTable);
    devFilter.addEventListener("change", filterTable);

    // clickable tags
    document.body.addEventListener("click", e => {
      if (!e.target.classList.contains("tag")) return;
      const tag = e.target.dataset.tag;
      // toggle
      if (activeTag === tag) activeTag = "";
      else activeTag = tag;
      // update badge styles
      document.querySelectorAll(".tag").forEach(el => {
        el.classList.toggle("active", el.dataset.tag === activeTag);
      });
      // re-filter
      filterTable();
    });

    // column sorting
    function sortTable(colIdx) {
      const table = document.getElementById("vaultTable");
      const tbody = table.tBodies[0];
      const sorted = Array.from(tbody.rows)
        .sort((a,b) => a.cells[colIdx].innerText.localeCompare(b.cells[colIdx].innerText));
      // toggle order if already sorted
      if (table.dataset.sorted === colIdx) sorted.reverse();
      sorted.forEach(r => tbody.appendChild(r));
      table.dataset.sorted = table.dataset.sorted === colIdx ? "" : colIdx;
    }
  </script>

</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    print(f"✔ HTML report written to {output_path}")

if __name__ == "__main__":
    build_html(Path(INPUT_JSON), Path(OUTPUT_HTML))