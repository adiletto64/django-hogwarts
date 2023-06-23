import textwrap
import ast

from hogwarts.codegen import ViewGenerator, insert_code

from ..models import Article
from ..utils import code_strip

generator = ViewGenerator(Article)


def test_it_generates_detail_view():
    code = generator.gen_detail_view()
    expected_code = """
    class ArticleDetailView(DetailView):
        model = Article
        context_object_name = "article"
        template_name = "articles/article_detail.html"
    """

    assert code_strip(code) == code_strip(expected_code)


def test_it_generates_list_view():
    code = generator.gen_list_view()
    expected_code = """
    class ArticleListView(ListView):
        model = Article
        context_object_name = "articles"
        template_name = "articles/article_list.html"
    """

    assert code_strip(code) == code_strip(expected_code)


def test_it_generated_create_view():
    code = generator.gen_create_view()
    expected_code = """
    class ArticleCreateView(CreateView):
        model = Article
        fields = ['id', 'title', 'description', 'created_at', 'beta']
        template_name = "articles/article_create.html"
    """

    assert code_strip(code) == code_strip(expected_code)


def test_it_generated_update_view():
    code = generator.gen_update_view()
    expected_code = """
    class ArticleUpdateView(UpdateView):
        model = Article
        fields = ['id', 'title', 'description', 'created_at', 'beta']
        template_name = "articles/article_update.html"
    """

    assert code_strip(code) == code_strip(expected_code)


def test_code_gen_imports():
    gen = ViewGenerator(Article)
    gen.gen_update_view()
    gen.gen_detail_view()

    imports = ["UpdateView", "DetailView", "Article"]
    imports_code = """
    from django.views.generic import UpdateView, DetailView
    from .models import Article
    """

    assert set(gen.imports) == set(imports)
    assert code_strip(gen.get_imports_code()) == code_strip(imports_code)


def test_it_inserts_code():
    gen = ViewGenerator(Article)
    create_code = gen.gen_create_view()
    detail_code = gen.gen_detail_view()

    new_code = insert_code([create_code, detail_code], gen.get_imports_code())

    expected_code = """
    from django.views.generic import CreateView, DetailView
    from .models import Article
    
    class ArticleCreateView(CreateView):
        model = Article
        fields = ['id', 'title', 'description', 'created_at', 'beta']
        template_name = "articles/article_create.html"
    
    class ArticleDetailView(DetailView):
        model = Article
        context_object_name = "article"
        template_name = "articles/article_detail.html"
    """

    print(new_code)
    print("======")
    print(code_strip(expected_code))

    assert code_strip(new_code) == code_strip(expected_code)
