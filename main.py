from pathlib import Path


class SlugProvider(object):
    @property
    def slug(self):
        return self.make_link(self.name)

    @staticmethod
    def slugify(source_name):
        raise NotImplementedError()


class SimpleSlugProvider(SlugProvider):
    @staticmethod
    def slugify(source_text):
        connector = '-'
        slug_chars = []
        for char in source_text:
            if char.isalnum():
                slug_chars.append(char)
            elif char.isspace():
                slug_chars.append(connector)
        return ''.join(slug_chars).strip(connector).lower()


class Page ():
    @property
    def link(self):
        raise NotImplementedError()

    @property
    def markdown_view(self):
        raise NotImplementedError()

    @property
    def html_view(self):
        raise NotImplementedError()


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


class Collection(SimpleSlugProvider):
    def __init__(self, *, name=None, articles_per_page=2):
        self._name = name
        self._flat_list = []
        self._page_list = []
        self._articles_per_page = articles_per_page

    @property
    def name(self):
        return self._name

    @property
    def articles_per_page(self):
        return self._articles_per_page

    def add_article(self, article):
        self._flat_list.append(article)

    @property
    def flat_list(self):
        return self._flat_list

    @property
    def page_list(self):
        step = self.articles_per_page
        starts = range(0, len(self.flat_list), step)
        return [self.flat_list[i:i + step] for i in starts]


class Article(SimpleSlugProvider, Page):
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

    def __repr__(self):
        return f'Article(name="{self.name}")'


main_collection = Collection(name='all', articles_per_page=2)
site = Site(name='test site', path='.')
site.collections['all'] = main_collection
site.scan()
print(site.collections['all'].page_list)
