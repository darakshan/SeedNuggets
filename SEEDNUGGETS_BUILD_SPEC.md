# SeedNuggets Build and Site Specification

This document captures the full specification for the SeedNuggets site and build system. Implement (or re-implement) everything in the **correct** repository (e.g. Software/Python/SeedNuggets). Do not assume any prior edits; treat this as the single source of requirements and clarifications.

---

## 1. File structure and web root

- **Web root** = repository root (so the site has access to the `nuggets` directory).
- **Generated HTML:**
  - **`index.html`** is written to the **repository root** (not under `d/`).
  - **All other** generated HTML goes under **`d/`** (e.g. `d/about.html`, `d/internal.html`, `d/001-sample.html`).
- **Links** in generated pages use `/d/...` for docs (e.g. `/d/about.html`, `/d/resources.html`). No URL rewrites; links are fine as `/d/...`.

---

## 2. About and Internal pages

- **About** and **Internal** are each a **single HTML page** built from a directory of content.
- In each such directory, look for a file **`page.md`**.
  - **If `page.md` exists:** It contains content and **references to other files**. Use a simple convention: each line of the form `@include filename.md` means “include the contents of that file here.” Resolve paths relative to the directory containing `page.md`. If there is a standard for .md includes, use it; otherwise use this `@include` convention.
  - **If there is no `page.md`:** Include all `.md` files in that directory **alphabetically**, with a **section heading** before each (heading = file name).
- **About** page is built from the **`/about`** directory.
- **Internal** page is built from the **`/internal`** directory. Include a link to **`/nuggets`** so all source nuggets are readable.
- **build.py** should stay simple; the structure is driven by the skeleton `page.md` (and included files), not by hard-coded logic.

---

## 3. Required files; build must complain, not invent

- **Required files:** The build must **require** these and **exit with an error** (complain) if any are missing. It must **not** construct default or fallback pages.
  - `about/page.md`
  - `internal/page.md`
  - `content/resources.md`
  - `content/status` (see Status section below)
- Create **preliminary** versions of these with just the basics so the build works out of the box. The preliminary `page.md` files should **list the files currently in their directory** (via `@include` or equivalent) so the build runs without extra setup.

---

## 4. Resources page and nav

- A single **Resources** page is built from **`content/resources.md`** (similar to how `page.md` works: content plus references as needed).
- That page should **point to:** repository (source nuggets), index (home), and bibliography.
- This single Resources page simplifies the nav bar; it may remove the need for a separate “collapse to menu on phones” behavior, but narrow-screen behavior is still desired (see Nav bar below).
- Put the initial **resources.md** in **`/content`** (i.e. `content/resources.md`).

---

## 5. Status

- A file in **`/content`** contains **all valid statuses in their sort order** (one status per line). Example: `draft1`, `prelim`, `empty`.
- **build.py** must **complain** (exit with error) if it finds a nugget with a status **not** listed in that file.
- Statuses are used for ordering “most ready” first (see Home and Repository below).

---

## 6. Repository page

- The **repository** view (e.g. `d/repository.html`) shows nuggets in a table.
- Add a **sort-order pulldown** at the top of the table. Orders:
  - **Alphabetical**
  - **By most recent**
  - **By status** (using the order defined in `content/status`).

---

## 7. Home page

- The **articles** (nuggets) shown on the home page should be **selected and ordered by status**: the “most ready” nuggets first, using the sort order from the status file (e.g. draft1 before prelim before empty).

---

## 8. Nav bar

- The **nav bar** at the top should become a **menu on narrow screens** (e.g. smartphones)—e.g. hamburger or collapsible menu—so the site is usable on small viewports.

---

## 9. Bibliography

- **Directive in nuggets:** Add a directive to the nugget grammar/parser to identify **individual references** so a bibliography can be generated.
  - **Syntax:** A separate line: `#ref title [ "|" author ]`. Use `|` as separator because it is unlikely to appear in a title. Author is optional.
- **Build behavior:** Analyze all **draft1** nuggets to find and mark these references. Generate a **bibliography** that:
  - Is sorted **alphabetically** (e.g. by title).
  - Lists **book and article titles** (and author, etc.); **page numbers** stay in the nuggets only.
  - Shows **which nuggets** contain each reference.
- The bibliography can be very incomplete at this stage; the main goal is to get the **metadata into the nuggets** and the pipeline in place.
- **Docs:** Update **internal/structure.md** and **internal/grammar.md** (or equivalent) to describe the nugget format and the `#ref` directive. Do **not** overwrite existing structure or grammar docs: read what’s there first and **merge** or add new sections; if the original structure/grammar lived in one file and was split out, respect that and add only the new material appropriately.

---

## 10. Implementation notes (for redoing edits)

- **Do not overwrite existing files** without checking first and without the user’s approval. If a file already exists (e.g. `internal/structure.md`, CONTEXT files), read it and either merge new content or write to a new file.
- **Do not delete** the repository’s `.git` directory or any existing content. Work only in the intended repo (e.g. Software/Python/SeedNuggets).
- All behavior above (paths, required files, status validation, page.md, @include, Resources, repository sort, home order, bibliography, nav) must be implemented in the **build script** and related assets (e.g. CSS/JS for nav and repository sort) in that repository. Treat this spec as the source of truth; do not assume the state of any other directory (e.g. Software/Web/SeedNuggets) is correct or complete.

---

## 11. Quick reference: URLs and key paths

| Item            | Location / URL example                    |
|-----------------|-------------------------------------------|
| Web root        | Repo root                                 |
| Home            | `index.html` at repo root                 |
| About           | `d/about.html`                            |
| Internal        | `d/internal.html`                         |
| Resources       | `d/resources.html`                        |
| Repository      | `d/repository.html`                       |
| Bibliography    | `d/bibliography.html`                     |
| Nugget page     | `d/<id>.html`                             |
| Source nuggets  | `/nuggets/` (link from Internal/Resources) |
| Status list     | `content/status` (one status per line)    |
| Resources source| `content/resources.md`                    |
| About source    | `about/page.md` + @include                |
| Internal source | `internal/page.md` + @include             |

---

*End of specification.*
