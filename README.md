# Docchat

This project is a command-line assistant that answers questions about files in the
current folder. You can list files, read documents, search for matching lines,
and also do some calculations with arithmetic expressions!

## Markdown compiler
```text
$ cd test_projects/markdown-compiler
$ chat
chat> /ls .
README.md  example  markdown_compiler  pyproject.toml  requirements.txt  submission.toml
chat> Which function converts Markdown headings? Give just the function name.
compile_headers
```
This showed me that the compile_headers function converts the Markdown headings in that project. 


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
