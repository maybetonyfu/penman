from pathlib import Path
from slugify import slugify
import mistune


class HasSlug():
    @property
    def slug(self):
        return slugify(self.name)


class Page ():
    def __init__(self, *, articles=None, index=None):
        self._articles = articles
        self._index = index

    @property
    def articles(self):
        return self._articles

    @property
    def index(self):
        return self._index

    def build(self):
        content = ''
        for article in self.articles:
            content += f'{article.title} {article.path}'
        return content


class Site (object):
    def __init__(self, *, name=None, path=None):
        self._name = name
        self._path = Path(path).resolve()
        self._articles = []
        self._collections = {}

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def articles(self):
        return self._articles

    @property
    def collections(self):
        return self._collections

    def scan(self):
        for path in self.path.glob('*/index.md'):
            article = Article(
                name=path.parent.name,
                path=path.parent
            )
            self.articles.append(article)
            self.collections.get('all').add_article(article)

    def ensure_public_dir(self):
        public_dir = self.path / 'public'
        public_dir.mkdir(parents=True, exist_ok=True)

    def build_articles(self):
        self.ensure_public_dir()
        for article in self.articles:
            article.build()

    def build_collections(self):
        for collection in self.collections.values():
            collection.build(path=self.path)


class Collection(HasSlug):
    def __init__(self, *, name=None, articles_per_page=2):
        self._name = name
        self._articles = []
        self._pages = []
        self._articles_per_page = articles_per_page

    @property
    def name(self):
        return self._name

    @property
    def articles_per_page(self):
        return self._articles_per_page

    def add_article(self, article):
        self._articles.append(article)

    @property
    def articles(self):
        return self._articles

    @property
    def pages(self):
        if not len(self._pages) is 0:
            return self.pages
        step = self.articles_per_page
        starts = range(0, len(self.articles), step)
        for index, start in enumerate(starts, start=1):
            articles_slice = self.articles[start:start + step]
            page = Page(articles=articles_slice, index=index)
            self._pages.append(page)
        return self._pages

    def build(self, *, path=None):
        html_path = path / 'public' / self.slug
        html_path.mkdir(parents=True, exist_ok=True)
        for page in self.pages:
            file_path = html_path / (f'{page.index}.html')
            file_path.write_text(page.build())


class Article(HasSlug):
    def __init__(self, *, name=None, path=None):
        self._name = name
        self._path = path

    @property
    def created_date(self):
        return self

    @property
    def author(self):
        return self

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._name

    @property
    def path(self):
        return self._path

    def build(self):
        md_path = self.path / 'index.md'
        html_path = self.path.parent / 'public' / (self.slug + '.html')
        html = mistune.markdown(md_path.read_text())
        html_path.write_text(html)

    def __repr__(self):
        return f'Article(name="{self.name}")'


main_collection = Collection(name='all', articles_per_page=2)
site = Site(name='test site', path='.')
site.collections['all'] = main_collection
site.scan()
site.build_articles()
site.build_collections()
