import datetime
import os
import platform
import shutil
import subprocess
import sys

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

CURRENT_YEAR = datetime.datetime.now().year


class Post:
    def __init__(self, title, slug, date, language, content, summary):
        self.title = title
        self.slug = slug
        self.date = date
        self.language = language
        self.content = content
        self.summary = summary
        self.html = None

    def render(self, config):
        env = Environment(loader=FileSystemLoader("src/templates"))
        post_template = env.get_template("post.html")

        md = markdown.Markdown(extensions=["fenced_code", "meta"])
        processed_content = md.convert(self.content)

        output_path = os.path.join(
            "output", self.language, "posts", f"{self.slug}.html"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            self.html = processed_content
            file.write(post_template.render(post=self, config=config, current_year=CURRENT_YEAR))


def clean_output_directory():
    if os.path.exists("output"):
        shutil.rmtree("output")


def copy_static_files():
    shutil.copytree("src/static", "output/static")
    
    
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
    md = markdown.Markdown(extensions=["fenced_code", "meta"])

    for filename in os.listdir(f"src/content/{lang}/posts"):
        if filename.endswith(".md"):
            with open(f"src/content/{lang}/posts/{filename}", encoding="utf-8") as file:
                content = file.read()
                md.convert(content)
                meta = md.Meta
                post = Post(
                    title=meta["title"][0],
                    slug=meta["slug"][0],
                    date=datetime.datetime.strptime(meta["date"][0], "%Y-%m-%d"),
                    language=meta["language"][0],
                    content=content,
                    summary=meta["summary"][0]
                )

                posts.append(post)

    return posts


def generate_index(posts, config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    index_template = env.get_template("index.html")

    posts_per_page = config["posts_per_page"]
    num_pages = (len(posts) + posts_per_page - 1) // posts_per_page

    for page in range(1, num_pages + 1):
        start_index = (page - 1) * posts_per_page
        end_index = start_index + posts_per_page
        current_posts = posts[start_index:end_index]

        if page == 1:
            file_name = "index.html"
        else:
            file_name = f"index{page}.html"

        output_path = os.path.join("output", config["language"], file_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(
                index_template.render(
                    posts=current_posts,
                    config=config,
                    page=page,
                    num_pages=num_pages,
                    current_page=page,
                    current_year=CURRENT_YEAR
                )
            )


def generate_articles(posts, config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    archive_template = env.get_template("articles.html")

    output_path = os.path.join("output", config["language"], "articles.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(archive_template.render(posts=posts, config=config, current_year=CURRENT_YEAR))
        

def generate_home(posts, config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    archive_template = env.get_template("home.html")

    output_path = os.path.join("output", config["language"], "index.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(archive_template.render(posts=posts[:3], config=config, current_year=CURRENT_YEAR))


def generate_projects(config):
    env = Environment(loader=FileSystemLoader("src/templates"))
    archive_template = env.get_template("projects.html")

    output_path = os.path.join("output", config["language"], "projects.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(archive_template.render(config=config, current_year=CURRENT_YEAR))


def build_site():
    clean_output_directory()
    copy_static_files()
    copy_public_assets()

    languages = ["en", "es"]

    for lang in languages:
        config = load_config(lang)
        posts = load_posts(lang)
        posts.sort(key=lambda x: x.date, reverse=True)

        #generate_index(posts, config)
        generate_articles(posts, config)
        generate_home(posts, config)
        generate_projects(config)

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
