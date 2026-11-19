# AGENTS.md

Shared instructions for AI coding agents (Claude Code, Codex, and any others) working on this repository. `CLAUDE.md` imports this file, so this is the single source of truth. Edit this file, not `CLAUDE.md`.

## Project overview

- This is Om Prabhu's personal website, served at https://omprabhu31.github.io/.
- It's a **Jekyll** site built and hosted by **GitHub Pages** (`github-pages` gem), using a lightly modified [Type Theme](https://github.com/rohanchandra/type-theme/).
- **Pushing to `master` deploys the live site.** GitHub Pages rebuilds automatically on every push to `master`.
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
| `resume.pdf` | Current resume (linked from the nav in `_layouts/default.html` and from `index.md`) |
| `changelog.md` | Credits for edits suggested by others (`/changelog/`, linked from `index.md`) |
| `_scripts/` | Repo tooling, not published (Jekyll skips `_`-prefixed folders). `check_links.py` is the link checker |

## Conventions

### Pages
- Each page needs YAML front matter. Match the existing pages:
  ```yaml
  ---
  layout: page
  title: Page Title
  permalink: /section/page-name/
  feature-img: "assets/img/sample_feature_img_2.png"
  hide: true
  ---
  ```
- The header nav lists every page that has a `title` and **doesn't** set `hide: true`. Set `hide: true` unless the page should show up in the top nav, and leave existing pages' `hide` values alone unless asked to change them.
- Always set an explicit `permalink` with a trailing slash.
- Use `{{ site.baseurl }}` / `relative_url` in templates for internal links. In Markdown content, root-relative links (`/academics/courses/`) are fine and match existing style.
- Existing content mixes Markdown and inline HTML (`<h3>`, `<ul><li>`, `<center>`). Follow the style of the file you're editing rather than converting it.

### Blog posts
- File name: `_posts/YYYY-MM-DD-slug.md`, with `layout: post`, `title`, and optionally `tags` and `feature-img`.

### Courses page (`academics/courses.md`)
- Add new semesters below the latest one, in the same format: `<h4>Semester N (Season YYYY)</h4>` followed by a `<ul>` of `<li><a href="...">CODE - Course Name</a></li>`.

### Notes (`academics/notes/`)
- One folder per course. Commit the `.tex` source, the compiled `.pdf`, and any images it uses.
- **Don't** commit LaTeX build artefacts (`.aux`, `.log`, `.out`, `.toc`, `.synctex.gz`, `.bak`). Some old ones are already tracked; leave those alone unless asked to clean them up.
- Link new notes from `academics/notes/notes.md`.

### Styling
- Change theme colours, fonts and spacing in `_sass/base/_variables.scss`, not with one-off inline styles.
- Math rendering uses KaTeX (`katex: true` in `_config.yml`).

### Assets and file naming
- Put site images in `assets/img/`. Put files that belong to a course's notes in that course's `academics/notes/<course>/` folder.
- **Give every new file a clear, descriptive name:**
  - lowercase, no spaces, words separated by hyphens (`-`), or by underscores (`_`) if the neighbouring files in that folder already use them;
  - describe the content, e.g. `me226-heat-exchanger-diagram.png`, `ma214-notes.pdf`, `2026-11-blog-cover.jpg`. Include the course code or date where relevant;
  - lowercase extensions (`.jpg`, `.png`, `.pdf`), not `.JPG` / `.PNG`;
  - never generic or auto-generated names like `image1.png`, `Screenshot 2026-11-19 at 10.02.png`, `untitled.pdf`, `final_final2.jpg`.
- Don't rename existing files to fit this convention unless asked. Renaming breaks links, including links from outside the site.
- Keep files reasonably small (compress large photos before committing).
- `.gitattributes` routes `*.bc` files through Git LFS.

## Constraints
- **GitHub Pages only allows its whitelisted plugins.** Don't add gems or plugins that aren't supported by the `github-pages` gem (currently used: `jekyll-paginate`, `jekyll-seo-tag`). There is no custom CI build.
- GitHub Pages uses Jekyll 3.x, where the `exclude:` list in `_config.yml` **replaces** the defaults. If you add a repo-only file (docs, scripts, agent files), add it to `exclude:` so it isn't published to the live site.
- Don't commit `_site/`, `.sass-cache/`, `.bundle/`, `Gemfile.lock`, or `.DS_Store` (already in `.gitignore`).
- Don't change personal details (email, social links, resume, about/contact text) unless the user explicitly asks.
- Don't delete or rename existing pages or permalinks without asking. External sites may link to them.

## Verifying changes
Do all of these before every commit:

1. **Build.** If Ruby/Bundler are available, run `bundle install` once, then `bundle exec jekyll build` (or `bundle exec jekyll serve` to preview at http://localhost:4000). The build must succeed with no errors. If Jekyll isn't installed locally, check by hand that front matter is valid YAML and Liquid tags are balanced, and say in your summary that the site wasn't built.
2. **Check links.** Run `python3 _scripts/check_links.py` from the repo root.
   - `--internal` checks only links within the site (fast, works offline). The full run also fetches every external link. Do the full run whenever you add or change external links.
   - Your change must not add any new broken links. Fix any you introduced. If you notice existing broken links, fix them when the fix is obvious (typo, moved page). Otherwise report them to the user.
   - A non-200 from an external site isn't always a dead link (bot-blocking, rate limits, outages). Open it before deleting it. The script already ignores LinkedIn/Facebook bot-blocking and skips HTTP 429.
   - **This applies to sub-agents too.** When you hand website work to a sub-agent or another agent, tell it to run the link checker and report the results.
3. After pushing to `master`, the live site updates within a few minutes. Say so when reporting back.

### Google Forms used on the site
Both are owned by the user's Google account. Responses go there.
- **Anonymous message** (`…/1FAIpQLSe1cNYSMjQDIuQBHMxn0FZAlslGAcqdmh1BdeW-A7CotFF6yQ/viewform`): footer (`_config.yml`), embedded on `contact.md` (with `?embedded=true`), and the notes pages under `academics/notes/*/`.
- **Blog suggestions & feedback** (`…/1FAIpQLSc07E4VZhgkYpqSRcE-ur6TddJLVlG1HOHVgyIF0_xQf_1ukw/viewform`): `blog.md`.
- If you add a new "anonymous message" or "feedback" link, reuse these forms rather than creating new ones.

## Git workflow (applies to every agent)

**Commit and push automatically.** As soon as a website feature or addition has been created, updated or processed, and verified as above, commit it and push it without waiting to be asked. Where it goes depends on the size of the change:

### Size of change → where it goes

| Size | Examples | What to do |
| --- | --- | --- |
| **Small** | Adding courses, notes, a blog post or an image; fixing typos or broken links; updating `resume.pdf`; copy edits on one page | Commit and push straight to the **current branch** (normally `master`, so it goes live). |
| **Bigger** | A new page or section that follows existing patterns; changes across many files; reorganising notes; new helper scripts | Create a branch `feature/<short-name>` from up-to-date `master`. Commit and push there as you go, verify everything, then merge into `master` and push. |
| **Major** | Layout/template/theme/Sass changes; home page or nav changes; `_config.yml` changes; new site sections; removing, renaming or moving pages or permalinks; new JS, plugins or external services | Same as "bigger", but **don't merge**. Push the branch, open a PR into `master` (`gh pr create`), and ask the user to review it. Merge only after the user approves (see step 7), then clean up (step 8). |

If you're unsure, treat the change as the larger category. If the user has a non-`master` branch checked out, small changes go on that branch. Don't switch away from it.

The user can preview an unmerged branch locally with `git checkout feature/<name> && bundle exec jekyll serve`. GitHub Pages only builds `master`.

### Steps
1. **Commit identity:** every commit must be authored as `Om Prabhu <prabhu.om@icloud.com>`. Check `git config user.email` before your first commit. If it's different, set it for this repo only (`git config user.email prabhu.om@icloud.com`) and mention that you did.
2. Before starting, run `git status` and `git pull --rebase` (if the branch has an upstream) so you're working on the latest version.
3. Make one commit per finished feature or change. Don't bundle unrelated changes, and don't commit half-finished work to `master`. Work-in-progress commits are fine on a `feature/` branch.
4. Stage only the files you changed for that feature (`git add <paths>`). Don't use `git add -A` or `git add .` blindly, and don't commit unrelated pre-existing changes you didn't make. Leave those alone and mention them.
5. Commit messages: short, lowercase, imperative or past-tense summary, matching the repo's existing style (e.g. `added sem 9 courses`, `fixed typo in about page`). Add a body if the change needs explanation. Add any co-author/attribution trailers your tool requires.
6. Push: `git push` (use `git push -u origin <branch>` the first time you push a new branch).
7. **Merging:**
   - A verified "bigger" branch: `git checkout master && git pull --rebase && git merge --no-ff feature/<name> && git push`.
   - A "major" PR the user has approved: `gh pr merge <number> --merge --admin --delete-branch`. `master` has a branch protection rule requiring one approving review, and the user can't approve their own PR on GitHub. Their explicit approval in chat ("merge it") is the review, and `--admin` uses their admin rights to satisfy the rule. Never use `--admin` without that explicit approval.
8. **After every merge into `master`, clean up, however the merge happened (local merge, `gh pr merge`, or the user merging on GitHub):**
   - Delete the feature branch locally (`git branch -d feature/<name>`) and on GitHub (`git push origin --delete feature/<name>`, unless `--delete-branch` already did it).
   - Switch back to `master` and `git pull --rebase` so the local copy matches the live site.
   - Run `git fetch --prune` so the deleted branch doesn't linger as a stale `origin/feature/<name>` reference.
   - Only delete branches you created for that feature. Leave other branches (e.g. `test-deployment`) alone unless the user asks.
9. If a push is rejected because the remote moved ahead, run `git pull --rebase`, resolve conflicts, re-verify, and push again. **Never force-push to `master`**, and never rewrite history that has already been pushed to it.
10. If the build or link check fails, fix it before committing to `master`. If you can't fix it, don't push to `master`. Report the problem instead.
11. Never commit secrets, tokens or credentials.

## Collaborating between agents (Claude ↔ Codex)
- Both agents may work on this repo, sometimes one after the other. Always assume the other agent may have pushed since you last looked, so `git pull --rebase` before starting and before pushing.
- Read recent history (`git log --oneline -10`) at the start of a task to see what was changed last.
- Don't undo or rewrite another agent's work unless the user asks. If something they did looks wrong, point it out to the user.
- Keep this file current. If you set up a new convention (a new section, a new page pattern, a build step), add it here in the same commit.
- Agent-specific files (`CLAUDE.md`, `.claude/`, `.codex/`) should only hold tool-specific settings. Put shared instructions in this file.

## Reporting back
When you finish, tell the user briefly:
- what changed (files and pages affected),
- whether the site was built locally, and the link-checker result,
- the commit hash and branch you pushed to (and the PR link, if review is needed),
- anything you noticed but didn't fix (e.g. broken links).
