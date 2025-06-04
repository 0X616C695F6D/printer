# Automated Morning Paper

Printer: Creates a single paged newspaper with NASA and ScienceDaily content
with NASA image of the day

**Version**: 2.0

**License**: MIT

---

Overview

Produces a printable 2-column PDF that looks like a simple newspaper article.
Handles image placement & transformation, summarization using a local Ollama
model. Everything is unfortunately hardcoded since its not meant to be a serious
project. I wanted to learn how to run local ollama model and use it to summarize
content plus scraping information off webpages and handling any errors
elegantly.

---

Features

- Automated content scraping from ScienceDaily and NASA
- AI summarization using local Llama3.1 model
- Black & white image processing for NASA's Image of the Day
- 2-column printable PDF simulating a newspaper
- Custom typography with D-DIN fonts
- comprehensive error handling

---

Sources

- NASA Image of the Day: Featured space photography
- NASA Blogs: Latest astronomy and space exploration articles
- ScienceDaily: Engineering and technology news

---

Paper Format

- Layout: 2-column newspaper style
- Sections: NASA & SPACE, EVERYDAY SCIENCE
- Image: black & white NASA image placement
- Typography: D-DIN font family
- Output: Printable PDF
