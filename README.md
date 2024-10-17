# blasferna.com

This project is a simple and customizable static site generator built using Python, initially developed for my personal website. It can also be used as a base for creating and managing other static blogs or websites easily, without the need for a database or server-side scripting.

<p align="center">
    <img src="https://github.com/blasferna/blasferna.com/assets/8385910/081144fb-5214-4042-abda-35310439bf04" />
</p>


## Features

* Markdown support for writing posts and pages
* Jinja2 templates for easy customization of the site's appearance
* Pagination for articles page
* Multilingual support with separate configurations for each language
* Automatic generation of index, articles, and post pages
* Simple development server for testing the site locally
* Support for static files (CSS, JavaScript, images, etc.)
* Tailwind CSS for styling
* Generation of metadata for Open Graph
* Sitemap.xml generation
* RSS feed generation
* Built-in Open Graph image generator
* Github action for automated deployment on GitHub Pages
* Giscus comments integration

## Getting Started

### Requirements

* Python 3.7 or higher
* Jinja2
* PyYAML
* Markdown
* Tailwind CSS
* LiveReload (Python)

### Installation

1. Clone this repository or download the source code:

```bash
git clone https://github.com/blasferna/blasferna.com.git
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Install the required Node.js packages:

```bash
npm install
```


### Usage

1. Create your posts and pages in the `content` directory using Markdown format. You can organize your content in subdirectories for different languages (e.g., `content/en` and `content/es`).

2. Customize the Jinja2 templates in the `templates` directory to change the appearance of your site.

3. Edit the configuration files located in the language-specific directories (e.g., `en/config.yaml`, `es/config.yaml`) to set up the site's configuration for each language.

4. Generate the static site by running the following command:

```bash
python src/generator.py build
```

5. Test your site locally by running the built-in development server:

```bash
python src/generator.py serve
```

Visit `http://localhost:8000` in your web browser to view your site.

6. Deploy your site by uploading the contents of the `output` directory to your web server.


## License

This project is released under the MIT License. For more information, please see the `LICENSE` file in the root of the project.

