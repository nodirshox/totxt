# 🖥️ totxt: Source Code Repository to Single Text File

## 🌟 Overview

**totxt** is a Python CLI tool designed to extract source code files from a repository and consolidate them into a single, comprehensive text file. It respects `.gitignore` patterns, filters out unnecessary files, and ensures accurate encoding detection for seamless processing.

## ✨ Features

- 🔍 **Recursive Scanning**: Automatically scans directories to find all source code files.
- 🚫 **Respects .gitignore**: Excludes files and directories specified in `.gitignore`.
- 📄 **Multi-Language Support**: Handles files from various programming languages.
- 🔤 **Robust Encoding Detection**: Ensures accurate reading of source files with different encodings.
- 🚀 **Fast and Lightweight**: Efficiently processes large repositories without heavy resource usage.

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/totxt.git
cd totxt

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage

```bash
python totxt.py /path/to/repository
```

### Advanced Options

```bash
# Specify max file size in KB (default: 100 KB)
python totxt.py /path/to/repository --max-size 200

# Custom output filename
python totxt.py /path/to/repository --output custom_output.txt

# Enable verbose logging
python totxt.py /path/to/repository --verbose
```

## 🔧 Supported Languages

**totxt** supports source files in a wide range of languages, including:

- Python
- JavaScript/TypeScript
- HTML/CSS
- Java
- C/C++
- Ruby
- Go
- Rust
- Swift
- Shell Scripts
- Configuration Files (YAML, JSON, INI, etc.)

## 🚧 Limitations

- Excludes binary files and files exceeding the specified size limit.
- Focuses exclusively on text-based source code files.

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to your branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📬 Contact

For questions, feedback, or suggestions, feel free to contact [deepamhere@proton.me].

**Made by Deepam Makwana & Dev Shinde.**
