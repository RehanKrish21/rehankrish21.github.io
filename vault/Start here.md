# Start here

This vault is where essays for **rehankrish21.github.io** are written. Every note in `Essays/` that says `publish: true` becomes a page on the site, listed at `/essays/`. Everything else stays a draft and never appears.

## Writing a new essay

1. Make a new note in `Essays/` (new notes land there by default).
2. Insert the template: command palette (Cmd+P) → **Templates: Insert template** → **Essay**.
3. Fill in `title`, `subtitle` and `abstract` at the top. Leave `publish: false` while drafting.
4. Write. Use `## Headings` for sections; the site numbers them for you.
5. When it is ready, change `publish: false` to `publish: true` and push (see below).

## What works

| In Obsidian | On the site |
|---|---|
| `## Heading` | numbered section |
| `*italic*`, `**bold**`, `> quote` | the same |
| `[^1]` and `[^1]: reference` | superscript number and a References list at the end |
| `[[Another essay]]` | a link, if that essay is published; plain text if not |
| `![[figure.png]]` | the image, if the file is in `Attachments/` |
| `%% note to self %%` | nothing: never published |

## Getting it onto the site

The vault lives in the `paper-site` branch of the `rehankrish21.github.io` repository, in the `vault/` folder. Whenever a change to `vault/` is pushed, a GitHub Action rebuilds the essay pages; the site updates a minute or two later.

- **From your Mac:** clone the repository with GitHub Desktop, switch to the `paper-site` branch, and open the `vault` folder in Obsidian ("Open folder as vault"). Write, then commit and push in GitHub Desktop. (The Obsidian Git community plugin can do the commit and push from inside Obsidian.)
- **From the browser:** on github.com, open the `paper-site` branch, go to `vault/Essays/`, and use **Add file → Upload files** or the pencil icon.

## Checklist before publishing

- Every factual claim has a footnote to a source you have read.
- Every DOI opens the paper it names.
- Read it once out loud. It goes out under your name.
