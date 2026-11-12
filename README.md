# Docchat

This project is a command-line assistant that answers questions about files in the
current folder. You can list files, read documents, search for matching lines,
and also do some calculations with arithmetic expressions!

## Markdown compiler

```text
$ cd test_projects/markdown-compiler
$ chat
chat> /ls .
example.txt
chat> How does this project convert Markdown headings into HTML?
In most Markdown‑to‑HTML projects the heading conversion works in the same way:

1. **Read the source line** – the parser scans the file line‑by‑line (or token‑by‑token).  
2. **Detect heading syntax** – it looks for the “#” characters at the start of the line.  
   * `#` → level 1, `##` → level 2, … up to `######` → level 6.  
3. **Determine the heading level** – count the consecutive “#” characters before any space.  
4. **Strip the Markdown syntax** – remove the “#”s and the following space to get the heading text.  
5. **Wrap the text in the corresponding `<hN>` tag** – e.g. `## Welcome` becomes `<h2>Welcome</h2>`.  
6. **Preserve any inline Markdown** – inside the heading text, other Markdown (bold, links, etc.) is processed recursively.  
7. **Emit the HTML** – the generated `<hN>` element is written to the output stream.

### Typical implementation snippets

**Using a regex (very simple):**

```js
const headingRE = /^(#{1,6})\s+(.*)$/gm;
const html = mdText.replace(headingRE, (_, hashes, content) => {
  const level = hashes.length;
  return `<h${level}>${content.trim()}</h${level}>`;
});
```

**Using a library (e.g., `marked` or `markdown-it`):**

```js
const marked = require('marked');
marked.setOptions({ renderer: new marked.Renderer() });

const renderer = new marked.Renderer();
renderer.heading = function(text, level) {
  return `<h${level}>${text}</h${level}>\n`;
};
const html = marked(mdText, { renderer });
```

This helped me learn that using a regex makes converting Markdown headings a lot easier compared to using a library.

## Homepage

```text
$ cd test_projects/lab-homepage
$ chat
chat> /ls .
README.md  active_vs_index.jpeg  etf_image.jpeg  index.html  page2.html  page3.html  style.css  submission.toml  thanks1.jpeg
chat> What is the title of the homepage in index.html?
The homepage’s `<title>` tag reads:
**“A Primer on Index Funds”**
```

I learned that `ndex.html sets the homepage title to “A Primer on Index Funds.


## eBay scraper

```text
$ cd test_projects/ebay-scraper
$ chat
chat> /ls .
README.MD  Skyrim.json  ebay-dl.py  halo.json  practice-pages  practice-pages.zip  star wars.json
chat> Which function in ebay-dl.py converts prices to cents?
The function that converts prices to cents is **`price_in_cents`**.
```

I learned that the scraper uses price_in_cents to convert a listing’s price text into cents.