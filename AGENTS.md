# AGENTS.md

Project rules for every agent working on this repo. `CLAUDE.md` imports this file; edit this one. The user's global defaults (`~/projects/agent-collab-setup/global/AGENTS.md`: shared checkouts, staging, secrets, honesty) also apply; this file wins where they differ.

## Project overview

- Om Prabhu's personal website, served at https://omprabhu31.github.io/.
- A **Jekyll** site built and hosted by **GitHub Pages** (`github-pages` gem), using a lightly modified [Type Theme](https://github.com/rohanchandra/type-theme/).
- **Pushing to `master` deploys the live site** within a few minutes.
- Remote: `origin` → `https://github.com/omprabhu31/omprabhu31.github.io`.
- `/gamedev/…` pages are **not** in this repo. They're served from the separate `omprabhu31/gamedev` repo (a GitHub Pages project site on the same domain).

## Repository layout

| Path | Purpose |
| --- | --- |
| `_config.yml` | Site config: title, nav/social settings, KaTeX toggle, pagination, plugins, `exclude` list |
| `_layouts/` | Page templates (`default`, `home`, `page`, `post`, `blog`, `tags`) |
| `_includes/` | Partials (`head`, `header`, `footer`, `icons`, `post_nav`, `disqus`, `tags_list`) |
| `_sass/` | Theme styles; colours/fonts/spacing live in `_sass/base/_variables.scss` |
| `assets/` | `css/main.scss` (Sass entry point), `img/` (feature images, avatar), `js/` (KaTeX init, search) |
| `_posts/` | Blog posts, named `YYYY-MM-DD-slug.md` |
| `index.md` | Home page (`layout: home`) with the main link list |
| `about.md`, `blog.md`, `contact.md` | Top-level pages |
| `academics/courses.md` | Course list, grouped by semester |
| `academics/notes/` | Course notes: one folder per course (LaTeX source + compiled PDF + figures), indexed by `notes.md` |
| `resume.pdf` | Current resume (linked from the nav in `_layouts/default.html` and from `index.md`). Built from `_resume/`, don't edit by hand |
| `_resume/` | CV LaTeX source (`main.tex`, `developercv.cls`, images) plus `build.sh`, which builds it into `resume.pdf`. **Gitignored, local only** |
| `changelog.md` | Credits for edits suggested by others (`/changelog/`, linked from `index.md`) |
| `_scripts/` | Repo tooling, not published (Jekyll skips `_`-prefixed folders). `check_links.py` is the link checker |

## Conventions

### Pages
- Each page needs YAML front matter matching the existing pages:
  ```yaml
  ---
  layout: page
  title: Page Title
  permalink: /section/page-name/
  feature-img: "assets/img/sample_feature_img_2.png"
  hide: true
  ---
  ```
- The header nav lists every page that has a `title` and **doesn't** set `hide: true`. Set `hide: true` unless the page should be in the top nav, and leave existing pages' `hide` values alone unless asked.
- Always set an explicit `permalink` with a trailing slash.
- Use `{{ site.baseurl }}` / `relative_url` in templates for internal links. In Markdown content, root-relative links (`/academics/courses/`) match existing style.
- Content mixes Markdown and inline HTML (`<h3>`, `<ul><li>`, `<center>`). Follow the style of the file you're editing.

### Blog posts
- `_posts/YYYY-MM-DD-slug.md`, with `layout: post`, `title`, and optionally `tags` and `feature-img`.

### Courses page (`academics/courses.md`)
- Add new semesters below the latest one: `<h4>Semester N (Season YYYY)</h4>` followed by a `<ul>` of `<li><a href="...">CODE - Course Name</a></li>`.

### Notes (`academics/notes/`)
- One folder per course. Commit the `.tex` source, the compiled `.pdf`, and any images it uses. Link new notes from `academics/notes/notes.md`.
- **Don't** commit LaTeX build artefacts (`.aux`, `.log`, `.out`, `.toc`, `.synctex.gz`, `.bak`). Some old ones are tracked; leave those alone unless asked.

### Resume (`_resume/`)
- `_resume/main.tex` is the master copy of the CV. The user no longer uses Overleaf: edit `main.tex` directly, and don't overwrite it from an Overleaf export unless asked.
- `_resume/` exists only on the user's machine. **Never commit the CV source**; only the built `resume.pdf` goes on GitHub. If `_resume/` is missing, stop and ask the user where the source is. Don't recreate it.
- `_resume/build.sh` (needs `latexmk`) compiles `main.tex` and copies the PDF to `/resume.pdf`.
- The CV must stay **one page**; `build.sh` warns if it isn't. Fix it by tightening spacing or wording in `main.tex` (never by cutting content without asking), and say what you changed. Spacing is already tight: `top=12mm`, `bottom=11mm`, `\vspace{-17 pt}` before the lower section headings. The Visual Acuity project is hidden in `\begin{comment}`.
- Commit only `resume.pdf` (a small change, straight to `master`).

### Styling
- Change theme colours, fonts and spacing in `_sass/base/_variables.scss`, not with one-off inline styles. Maths uses KaTeX (`katex: true` in `_config.yml`).

### Assets and file naming
- Site images go in `assets/img/`; files belonging to a course's notes go in `academics/notes/<course>/`.
- New files get clear, descriptive names: lowercase, no spaces, hyphens (or underscores if neighbouring files use them), lowercase extensions, and the course code or date where relevant (e.g. `me226-heat-exchanger-diagram.png`, `2026-11-blog-cover.jpg`). Never generic names like `image1.png`, `Screenshot ….png` or `final_final2.jpg`.
- Don't rename existing files to fit this unless asked; renaming breaks links, including external ones.
- Keep files reasonably small (compress large photos before committing). `.gitattributes` routes `*.bc` files through Git LFS.

## Constraints
- **GitHub Pages only allows its whitelisted plugins.** Don't add gems or plugins unsupported by the `github-pages` gem (currently `jekyll-paginate`, `jekyll-seo-tag`). There is no custom CI build.
- Jekyll 3.x: the `exclude:` list in `_config.yml` **replaces** the defaults. Add any repo-only file (docs, scripts, agent files) to `exclude:` so it isn't published.
- Don't commit `_site/`, `.sass-cache/`, `.bundle/`, `Gemfile.lock` or `.DS_Store`.
- Don't change personal details (email, social links, resume, about/contact text) unless the user explicitly asks.
- Don't delete or rename existing pages or permalinks without asking.

## Verifying changes
Before every commit:

1. **Build:** `bundle exec jekyll build` (run `bundle install` once; `jekyll serve` previews at http://localhost:4000). It must succeed with no errors. If Jekyll isn't installed, check front matter is valid YAML and Liquid tags are balanced, and say the site wasn't built.
2. **Links:** `python3 _scripts/check_links.py` from the repo root. `--internal` is fast and offline; do the full run whenever you add or change external links. Add no new broken links. Fix existing ones when the fix is obvious, otherwise report them. A non-200 from an external site isn't always dead (bot-blocking, rate limits): open it before deleting. The script already ignores LinkedIn/Facebook blocking and skips HTTP 429. **When handing website work to another agent, tell it to run the link checker and report the results.**

### Google Forms used on the site
Both are owned by the user's Google account; responses go there. Reuse them rather than creating new ones.
- **Anonymous message** (`…/1FAIpQLSe1cNYSMjQDIuQBHMxn0FZAlslGAcqdmh1BdeW-A7CotFF6yQ/viewform`): footer (`_config.yml`), embedded on `contact.md` (with `?embedded=true`), and the notes pages under `academics/notes/*/`.
- **Blog suggestions & feedback** (`…/1FAIpQLSc07E4VZhgkYpqSRcE-ur6TddJLVlG1HOHVgyIF0_xQf_1ukw/viewform`): `blog.md`.

## Git workflow (overrides the global default)

**Commit and push automatically.** As soon as a website feature or addition is done and verified, commit and push it without waiting to be asked:

| Size | Examples | What to do |
| --- | --- | --- |
| **Small** | Adding courses, notes, a blog post or an image; fixing typos or broken links; updating `resume.pdf`; copy edits on one page | Commit and push straight to the **current branch** (normally `master`, so it goes live). |
| **Bigger** | A new page or section following existing patterns; changes across many files; reorganising notes; new helper scripts | Branch `feature/<short-name>` from up-to-date `master`, commit and push as you go, verify, then merge into `master` and push. |
| **Major** | Layout/template/theme/Sass changes; home page or nav changes; `_config.yml` changes; new site sections; removing, renaming or moving pages or permalinks; new JS, plugins or external services | As "bigger", but **don't merge**: push the branch, open a PR into `master` (`gh pr create`) and ask the user to review. Merge only after they approve. |

If unsure, treat it as the larger category. If the user has a non-`master` branch checked out, small changes go on that branch; don't switch away. Unmerged branches can be previewed with `git checkout feature/<name> && bundle exec jekyll serve` (Pages only builds `master`).

1. **Identity:** commits are authored as `Om Prabhu <prabhu.om@icloud.com>`. If `git config user.email` differs, set it for this repo only and mention it.
2. Before starting, `git status` and `git pull --rebase` (if the branch has an upstream).
3. One commit per finished change; no half-finished work on `master` (WIP commits are fine on `feature/`).
4. Messages: short, lowercase summary in the repo's style (e.g. `added sem 9 courses`), plus any attribution trailers your tool requires.
5. Push with `git push` (`git push -u origin <branch>` the first time for a new branch). If the push is rejected because the remote moved ahead, `git pull --rebase`, resolve conflicts, re-verify, and push again. **Never force-push to `master`** or rewrite history already pushed to it.
6. Merging:
   - Verified "bigger" branch: `git checkout master && git pull --rebase && git merge --no-ff feature/<name> && git push`.
   - User-approved "major" PR: `gh pr merge <number> --merge --admin --delete-branch`. `master` requires one approving review and the user can't approve their own PR; their explicit "merge it" in chat is the review. Never use `--admin` without it.
7. **After every merge into `master`** (however it happened): delete the feature branch locally and on GitHub, switch to `master`, `git pull --rebase`, then `git fetch --prune`. Only delete branches you created; leave others (e.g. `test-deployment`) alone.
8. If the build or link check fails, fix it before committing to `master`. If you can't fix it, don't commit or push to `master`; report the problem instead.

Keep this file current: if you set up a new convention, add it here in the same commit.

## Reporting back
Tell the user: what changed (files and pages), whether the site was built and the link-checker result, the commit hash and branch pushed (and PR link if review is needed), that the live site updates within a few minutes, and anything you noticed but didn't fix.
