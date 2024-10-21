import datetime
import os
import platform
import re
import shutil
import subprocess
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import timezone
from io import BytesIO

import markdown
import requests
import yaml
from babel.dates import format_date
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageDraw, ImageFont


CURRENT_DATE = datetime.datetime.now()
CURRENT_YEAR = CURRENT_DATE.year
DEFAULT_LANG = "en"
LANGUAGES = ["en", "es"]


class Post:
    def __init__(self, title, slug, date, language, content, summary, tags=[]):
        self.title = title
        self.slug = slug
        self.date = date
        self.language = language
        self.content = content
        self.summary = summary
        self.tags = tags
        self.html = None
        self.formatted_date = None

    @property
    def topic(self):
        if self.tags:
            return self.tags[0]
        return None

    def process_content(self):
        if self.html is None:
            md = markdown.Markdown(extensions=["full_yaml_metadata", "extra"])
            self.html = md.convert(self.content)

    def render(self, config):
        env = Environment(loader=FileSystemLoader("src/templates"))
        post_template = env.get_template("post.html")

        self.process_content()

        if self.language == DEFAULT_LANG:
            output_path = os.path.join("output", "articles", self.slug, "index.html")
        else:
            output_path = os.path.join(
                "output", self.language, "articles", self.slug, "index.html"
            )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(
                post_template.render(
                    post=self,
                    config=config,
                    current_year=CURRENT_YEAR,
                    default_lang=DEFAULT_LANG,
                    og=OpenGraph(config, self),
                )
            )

    def generate_og_image(self, config):
        og_image = OpenGraphImageGenerator(self.language, self.slug, self.title, config.get("site_name"), self.topic)
        og_image.generate()


class OpenGraph:
    def __init__(self, config, post=None):
        self.config = config
        self.post = post
        self.type = "website"
        self.twitter_card = "summary_large_image"

    @property
    def title(self):
        if self.post is None:
            return self.config.get("site_title")
        return self.post.title

    @property
    def description(self):
        if self.post is None:
            return self.config.get("site_description")
        return self.post.summary

    @property
    def site_name(self):
        return self.config.get("site_name")

    @property
    def image(self):
        if self.post is None:
            return "/static/img/favicons/apple-touch-icon.png"
        return f"https://{self.domain}/static/img/og/{self.post.language}/{self.post.slug}.png"

    @property
    def url(self):
        if self.post is None:
            return f"https://{self.domain}/"
        if self.locale == DEFAULT_LANG:
            return f"https://{self.domain}/articles/{self.post.slug}/"
        return f"https://{self.domain}/{self.locale}/articles/{self.post.slug}/"

    @property
    def locale(self):
        return self.config.get("language")

    @property
    def domain(self):
        return self.config.get("domain")

    @property
    def twitter_creator(self):
        username = self.config.get("twitter_username")
        return f"@{username}"


class OpenGraphImageGenerator:
    FONT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".font_cache/")
    WIDTH = 1200
    HEIGHT = 630
    TOP_COLOR = (206, 236, 255)
    BOTTOM_COLOR = (236, 248, 255)
    FONT_NAME = "Roboto"

    def __init__(self, language, slug, title, site_name, topic):
        self.language = language
        self.title = title
        self.slug = slug
        self.site_name = site_name
        self.topic = topic

    def wrap_text(self, text, width, font):
        lines = []
        if font.getsize(text)[0] <= width:
            lines.append(text)
        else:
            words = text.split(" ")
            i = 0
            while i < len(words):
                line = ""
                while i < len(words) and font.getsize(line + words[i])[0] <= width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines

    def get_image(self, name, thumbnail: tuple = None, opacity=1):
        with open(f"src/static/img/{name}.png", "rb") as f:
            image_bytes = f.read()
        image_stream = BytesIO(image_bytes)
        image = Image.open(image_stream)
        if thumbnail:
            image.thumbnail(thumbnail)
        rgba = image.convert("RGBA")

        if opacity != 1 and opacity <= 1 and opacity >= 0:
            for x in range(rgba.width):
                for y in range(rgba.height):
                    r, g, b, a = rgba.getpixel((x, y))
                    rgba.putpixel((x, y), (r, g, b, int(a * opacity)))
        return rgba

    def download_font(self):
        font_directory = self.FONT_CACHE_DIR

        if not os.path.isdir(font_directory):
            os.makedirs(font_directory)

            url = f"https://fonts.google.com/download/list?family={self.FONT_NAME}"
            response = requests.get(url)

            for match in re.findall(
                r"\"(https:(?:.*?)\.[ot]tf)\"", str(response.content)
            ):
                with requests.get(match) as res:
                    res.raise_for_status()

                    with BytesIO(res.content) as fontdata:
                        font = ImageFont.truetype(fontdata)
                        name, style = font.getname()
                        name = " ".join(
                            [name.replace(self.FONT_NAME, ""), style]
                        ).strip()
                        target = os.path.join(font_directory, f"{name}.ttf")

                        with open(target, "wb") as f:
                            f.write(res.content)

    def create_gradient(self):
        base = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.TOP_COLOR)
        top = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.BOTTOM_COLOR)
        mask = Image.new("L", (self.WIDTH, self.HEIGHT))
        mask_data = []
        for y in range(self.HEIGHT):
            mask_data.extend([int(255 * (y / self.HEIGHT))] * self.WIDTH)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def generate(self):
        self.download_font()
        img = self.create_gradient().convert("RGBA")
        d = ImageDraw.Draw(img)

        title_font = ImageFont.truetype(self.FONT_CACHE_DIR + "Medium.ttf", 70)
        site_font = ImageFont.truetype(self.FONT_CACHE_DIR + "Regular.ttf", 30)

        code_logo = self.get_image("code", (120, 120))
        img.paste(code_logo, (45, 50), code_logo)

        title_lines = self.wrap_text(self.title, 0.8 * self.WIDTH - 2 * 50, title_font)
        title_y = 200

        line_spacing = 10

        for line in title_lines:
            d.text((50, title_y), line, fill="#252525", font=title_font)
            title_y += title_font.getsize("A")[1] + line_spacing
        site_x = 50
        site_y = self.HEIGHT - site_font.getsize("A")[1] - 50

        d.text((site_x, site_y), self.site_name, fill="#585858", font=site_font)

        if self.topic:
            try:
                topic_image = self.get_image(self.topic, opacity=0.5)
                img.paste(topic_image, (894, 324), topic_image)
            except FileNotFoundError:
                pass
        target = os.path.join(
            f"output/static/img/og/{self.language}", f"{self.slug}.png"
        )
        os.makedirs(os.path.dirname(target), exist_ok=True)
        img.save(target, "PNG")


def generate_rss(posts, config):
    site_url = f"http://{config.get('domain')}"
    if config.get("language") != DEFAULT_LANG:
        site_url = f"http://{config.get('domain')}/{config.get('language')}"

    fg = FeedGenerator()
    fg.id(site_url)
    fg.title(config.get("site_title"))
    fg.author({"name": config.get("author_name"), "email": config.get("author_email")})
    fg.link(href=site_url, rel="alternate")
    fg.subtitle(config.get("site_description"))
    fg.language(config.get("language"))

    for post in sorted(posts, key=lambda post: post.date, reverse=True):
        post_url = f"/{site_url}/articles/{post.slug}"
        fe = fg.add_entry(order="append")
        fe.id(post_url)
        fe.title(post.title)
        fe.link(href=post_url)
        post.process_content()
        fe.content(content=post.html)
        if post.topic is not None:
            fe.category(term=post.topic)
        fe.description(post.summary)
        fe.pubDate(post.date)

    xml = fg.rss_str(pretty=True)

    if config["language"] == DEFAULT_LANG:
        filename = os.path.join("output", "rss.xml")
    else:
        filename = os.path.join("output", config.get("language"), "rss.xml")

    with open(filename, "wb") as f:
        f.write(xml)


def generate_robots(domain):
    filename = os.path.join("output", "robots.txt")

    with open(filename, "w") as f:
        f.write(
            f"""User-agent: *
Allow: /

Sitemap: https://{domain}/sitemap.xml"""
        )


def generate_sitemap():
    urlset = ET.Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
        attrib={"xmlns:xhtml": "http://www.w3.org/1999/xhtml"},
    )

    pages = []
    for lang in LANGUAGES:
        config = load_config(lang)
        posts = load_posts(lang)
        base_url = f"https://{config.get('domain')}"

        if lang != DEFAULT_LANG:
            base_url = f"{base_url}/{lang}"

        for post in posts:
            pages.append(
                {
                    "url": f"{base_url}/articles/{post.slug}",
                    "last_mod": post.date.strftime("%Y-%m-%d"),
                }
            )

        pages.append(
            {"url": f"{base_url}/articles", "last_mod": CURRENT_DATE.strftime("%Y-%m-%d")}
        )
        pages.append(
            {"url": f"{base_url}/projects", "last_mod": CURRENT_DATE.strftime("%Y-%m-%d")}
        )

    for page in pages:
        url = ET.SubElement(urlset, "url")

        ET.SubElement(url, "loc").text = page["url"]
        ET.SubElement(url, "lastmod").text = page["last_mod"]

    xml_str = ET.tostring(urlset, encoding="utf-8", method="xml")
    reparsed = xml.dom.minidom.parseString(xml_str)
    filename = os.path.join("output", "sitemap.xml")

    with open(filename, "w") as f:
        f.write(reparsed.toprettyxml(indent=" "))


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
    md = markdown.Markdown(extensions=["full_yaml_metadata", "extra"])

    for filename in os.listdir(f"src/content/{lang}/posts"):
        if filename.endswith(".md"):
            with open(f"src/content/{lang}/posts/{filename}", encoding="utf-8") as file:
                content = file.read()
                md.convert(content)
                meta = md.Meta
                date = meta["date"]
                if isinstance(date, datetime.date):
                    date = datetime.datetime.combine(date, datetime.datetime.min.time())
                date = date.replace(tzinfo=timezone.utc)
                post = Post(
                    title=meta["title"],
                    slug=meta["slug"],
                    date=date,
                    language=meta["language"],
                    content=content,
                    summary=meta["summary"],
                    tags=meta.get("tags", []),
                )
                post.formatted_date = format_date(
                    date, format="long", locale=lang
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
                folder_path = os.path.join("output", "articles", "page", str(page))
        else:
            if page == 1:
                folder_path = os.path.join("output", config["language"], "articles")
            else:
                folder_path = os.path.join(
                    "output", config["language"], "articles", "page", str(page)
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
                    languages=LANGUAGES,
                    og=OpenGraph(config),
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
                    languages=LANGUAGES,
                    og=OpenGraph(config),
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
                languages=LANGUAGES,
                og=OpenGraph(config),
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
                config=config,
                current_year=CURRENT_YEAR,
                default_lang=DEFAULT_LANG,
                languages=LANGUAGES,
                og=OpenGraph(config),
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
                config=config,
                current_year=CURRENT_YEAR,
                default_lang=DEFAULT_LANG,
                og=OpenGraph(config),
            )
        )


def build_site():
    domain = ""
    clean_output_directory()
    copy_static_files()
    copy_public_assets()

    for lang in LANGUAGES:
        config = load_config(lang)
        posts = load_posts(lang)
        posts.sort(key=lambda x: x.date, reverse=True)

        generate_articles(posts, config)
        generate_home(posts, config)
        generate_projects(config)
        generate_404(config)
        generate_rss(posts, config)

        for post in posts:
            post.render(config)
            post.generate_og_image(config)

        domain = config.get("domain")

    generate_sitemap()
    generate_robots(domain)


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
