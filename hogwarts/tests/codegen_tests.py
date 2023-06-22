import textwrap

from hogwarts.codegen import ViewGenerator

from ..models import Article

generator = ViewGenerator(Article)


def test_it_generates_detail_view():
    code = generator.gen_detail_view()
    expected_code = """
    class ArticleDetailView(DetailView):
        model = Article
        context_object_name = "article"
        template_name = "articles/article_detail.html"
    """

    assert code == expected_code


def test_it_generates_list_view():
    code = generator.gen_list_view()
    expected_code = """
    class ArticleListView(ListView):
        model = Article
        context_object_name = "articles"
        template_name = "articles/article_list.html"
    """

    assert code == expected_code


def test_it_generated_create_view():
    code = generator.gen_create_view()
    expected_code = """
    class ArticleCreateView(CreateView):
        model = Article
        fields = ['id', 'title', 'description', 'created_at', 'beta']
        template_name = "articles/article_create.html"
    """

    assert code == expected_code


def test_it_generated_update_view():
    code = generator.gen_update_view()
    expected_code = """
    class ArticleUpdateView(UpdateView):
        model = Article
        fields = ['id', 'title', 'description', 'created_at', 'beta']
        template_name = "articles/article_update.html"
    """

    assert code == expected_code


def code_equals(code1: str, code2: str):
    return textwrap.dedent(code1).strip() == textwrap.dedent(code2).strip()
