# Static Site Generator ✨📚💻

This project is a static site generator implemented in Python, designed to transform content written in Markdown into a fully functional static website. 🌟📄💡

## Features 🚀🛠️📋

- **Markdown to HTML Conversion**: Transforms Markdown files into HTML pages using two template tags:

  - `{{ Title }}`: Replaced with the content of the `<h1>` in the Markdown file.
  - `{{ Content }}`: Replaced with the HTML generated from the Markdown file.

- **Static Asset Management**: Handles static assets like CSS and JavaScript files.

- **Content Organization**: Supports organizing content into directories for structured site architecture.

## Installation 🔧📦💾

1. **Clone the Repository**: 🚢💻🗂️

   ```bash
   git clone https://github.com/calvertjadon/static-site-generator.git
   ```

2. **Navigate to the Project Directory**: 📂➡️🏗️

   ```bash
   cd static-site-generator
   ```

3. **Install Dependencies**: 📥📜📦

   ```bash
   pip install .
   ```

## Usage ⚙️📑🚀

1. **Add Content**: Place your Markdown files in the `content` directory. 📝📁✅

2. **Run the Generator**: 🎯🖥️⚡

   ```bash
   python main.py
   ```

3. **View the Output**: The generated HTML files will be located in the `public` directory. 👀🗂️🌐

## Project Structure 🗂️🏗️🔍

```
static-site-generator/
├── content/        # Markdown content files
├── template.html   # HTML template with {{ Title }} and {{ Content }} tags
├── static/         # Static assets (CSS, JS, images)
├── public/         # Generated HTML files
├── main.py         # Main script to run the generator
├── pyproject.toml  # Python dependencies
└── README.md       # Project documentation
```

## Contributing 🤝🖋️🌟

Contributions are welcome! Please fork the repository and submit a pull request with your changes. 🔄📤✅

## License 📜⚖️🔒

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 🏷️📄✅

## Acknowledgements 🙏🎉🎓

This project was inspired by various static site generators and aims to provide a simple yet effective tool for static website generation. 💡✨🌐
