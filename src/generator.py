import datetime
import json
import os
import platform
import shutil
import subprocess
import sys

import markdown
import yaml
from babel.dates import format_date
from jinja2 import Environment, FileSystemLoader

CURRENT_YEAR = datetime.datetime.now().year
DEFAULT_LANG = "en"


class Post:
    def __init__(self, title, slug, date, language, content, summary):
        self.title = title
        self.slug = slug
        self.date = date
        self.language = language
        self.content = content
        self.summary = summary
        self.html = None
        self.formatted_date = None

    def render(self, config):
        env = Environment(loader=FileSystemLoader("src/templates"))
        post_template = env.get_template("post.html")

        md = markdown.Markdown(extensions=["meta", "extra"])
        processed_content = md.convert(self.content)

        if self.language == DEFAULT_LANG:
            output_path = os.path.join("output", "articles", self.slug, "index.html")
        else:
            output_path = os.path.join(
                "output", self.language, "articles", self.slug, "index.html"
            )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            self.html = processed_content
            file.write(
                post_template.render(
                    post=self,
                    config=config,
                    current_year=CURRENT_YEAR,
                    default_lang=DEFAULT_LANG,
                )
            )


def clean_output_directory():
    if os.path.exists("output"):
        shutil.rmtree("output")


def copy_static_files():
    shutil.copytree("src/static", "output/static")


def copy_public_assets(src_dir="src/public", dest_dir="output"):
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)


def load_config(lang):
    with open(f"src/content/{lang}/config.yaml", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_posts(lang):
    posts = []
    md = markdown.Markdown(extensions=["meta", "extra"])

    for filename in os.listdir(f"src/content/{lang}/posts"):
        if filename.endswith(".md"):
            with open(f"src/content/{lang}/posts/{filename}", encoding="utf-8") as file:
                content = file.read()
                md.convert(content)
                meta = md.Meta
                date = datetime.datetime.strptime(meta["date"][0], "%Y-%m-%d")
                post = Post(
                    title=meta["title"][0],
                    slug=meta["slug"][0],
                    date=date,
                    language=meta["language"][0],
                    content=content,
                    summary=meta["summary"][0],
                )
                post.formatted_date = format_date(
                    date.date(), format="long", locale=lang
                )
                posts.append(post)

    return posts


def generate_articles(posts, config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("articles.html")

    posts_per_page = config["posts_per_page"]
    num_pages = (len(posts) + posts_per_page - 1) // posts_per_page

    for page in range(1, num_pages + 1):
        start_index = (page - 1) * posts_per_page
        end_index = start_index + posts_per_page
        current_posts = posts[start_index:end_index]

        if config["language"] == DEFAULT_LANG:
            if page == 1:
                folder_path = os.path.join("output", "articles")
            else:
                folder_path = os.path.join("output", "articles", "page", page)
        else:
            if page == 1:
                folder_path = os.path.join("output", config["language"], "articles")
            else:
                folder_path = os.path.join(
                    "output", config["language"], "articles", "page", page
                )

        output_path = os.path.join(folder_path, "index.html")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(
                template.render(
                    posts=current_posts,
                    config=config,
                    page=page,
                    num_pages=num_pages,
                    current_page=page,
                    current_year=CURRENT_YEAR,
                    default_lang=DEFAULT_LANG,
                )
            )

    if num_pages == 0:
        # create articles empty
        if config["language"] == DEFAULT_LANG:
            output_path = os.path.join("output", "articles", "index.html")
        else:
            output_path = os.path.join(
                "output", config["language"], "articles", "index.html"
            )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(
                template.render(
                    posts=posts,
                    config=config,
                    page=1,
                    num_pages=0,
                    current_page=1,
                    current_year=CURRENT_YEAR,
                    default_lang=DEFAULT_LANG,
                )
            )


def generate_home(posts, config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("home.html")

    if config["language"] == DEFAULT_LANG:
        output_path = os.path.join("output", "index.html")
    else:
        output_path = os.path.join("output", config["language"], "index.html")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(
            template.render(
                posts=posts[:3],
                config=config,
                current_year=CURRENT_YEAR,
                default_lang=DEFAULT_LANG,
            )
        )


def generate_projects(config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("projects.html")

    if config["language"] == DEFAULT_LANG:
        output_path = os.path.join("output", "projects", "index.html")
    else:
        output_path = os.path.join(
            "output", config["language"], "projects", "index.html"
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(
            template.render(
                config=config, current_year=CURRENT_YEAR, default_lang=DEFAULT_LANG
            )
        )


def generate_404(config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("404.html")

    output_path = os.path.join("output", config["language"], "404.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(
            template.render(
                config=config, current_year=CURRENT_YEAR, default_lang=DEFAULT_LANG
            )
        )


def build_site():
    clean_output_directory()
    copy_static_files()
    copy_public_assets()

    languages = ["en", "es"]

    for lang in languages:
        config = load_config(lang)
        posts = load_posts(lang)
        posts.sort(key=lambda x: x.date, reverse=True)

        generate_articles(posts, config)
        generate_home(posts, config)
        generate_projects(config)
        generate_404(config)

        for post in posts:
            post.render(config)


def build_project():
    python_path = sys.executable
    if platform.system() == "Windows":
        cmd_separator = "&"
    else:
        cmd_separator = "&&"

    tailwind_build_command = "npx tailwindcss build -i src/input.css -o output/static/css/styles.css --minify"
    build_command = (
        f"{python_path} src/generator.py {cmd_separator} {tailwind_build_command}"
    )
    result = subprocess.run(build_command, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        print("Error executing build command:")
        print(result.stderr)


def serve():
    from livereload import Server

    server = Server()
    build_project()

    server.watch(
        "src/**/*.html",
        build_project,
    )
    server.watch("src/**/*.md", build_project)
    server.serve(root="output", port=8000)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
    elif len(sys.argv) > 1 and sys.argv[1] == "build":
        build_project()
    else:
        build_site()


if __name__ == "__main__":
    main()
