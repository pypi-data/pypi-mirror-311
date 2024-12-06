<div align="center">
  <img src="./logo.png" alt="Logo" width="200">
  <h1>Klean</h1>
  <p>A Text Manipulation Library.</p>
  <a href="https://github.com/walidsa3d/actions/workflows/test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/walidsa3d/klean/test.yml?branch=main&style=flat-square" alt="Test Status">
  </a>
  <a href="https://github.com/walidsa3d/klean/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/walidsa3d/klean?style=flat-square" alt="License">
  </a>
</div>

Klean is a text manipulation library.

## 🚀 Features
- **HTML Stripping**: Clean your text by removing all HTML tags.
- **Capitalization**: Convert strings to various capitalization formats (title case, uppercase, etc.).
- **Slugify**: Convert strings to URL-friendly slugs.
- **Whitespace**: Remove or normalize whitespace in your text.
- **Text Sanitization**: Replace or remove unwanted characters and symbols.
- **Normalization**: Convert text to a consistent format, including diacritic removal, converting quotes, etc.

## Installation

```sh
pip install klean
```

## Usage

```python
from klean import klean
txt = "Hello World"
klean(txt).capital().to_text()
```

## 🧑‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.


