import pytest
from hogwarts.magic_tests.factory import change_field_to_faker, generate_factory_class, flatten_multiline, \
    generate_imports, split_model_classes, generate_factories_code
from hogwarts.utils import code_strip


def test_it_changes_field_to_faker():
    field = "title = models.CharField(max_length=100)"
    expected = 'title = factory.Faker("name")'

    new_field = change_field_to_faker(field)

    assert new_field == expected


def test_it_ignores_blank_and_null():
    field = "title = models.CharField(max_length=50, null=True, blank=True)"

    assert change_field_to_faker(field) is None


def test_it_flattens_multiline_fields():
    code = """
    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField(
            max_length=500,
            blank=True,
            null=True
        )
    """

    expected = """
    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField(max_length=500,blank=True,null=True)
    """

    assert flatten_multiline(code) == expected



def test_it_replaces_fields_with_factory_faker():
    model = """
    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        views_number = models.IntegerField()        
    """

    expected = """
    class PostFactory(factory.django.DjangoModelFactory):
        title = factory.Faker("name")
        content = factory.Faker("paragraph")
        views_number = factory.fuzzy.FuzzyInteger(0, 100)
        
        class Meta:
            model = Post
    """

    result = generate_factory_class(model)

    assert result == code_strip(expected)


def test_it_skips_fields_with_default_values():
    line = "title = models.CharField(max_length=100, default='something')"
    result = change_field_to_faker(line)

    assert result is None


def test_it_generates_imports_from_factory_code():
    model = """
    class PostFactory(factory.django.DjangoModelFactory):
        title = factory.Faker("name")
        content = factory.Faker("paragraph")
        views_number = factory.fuzzy.FuzzyInteger(0, 100)
        
        class Meta:
            model = Post      
    """

    expected = """
        import factory
        from factory import fuzzy
        
        from .models import Post
    """

    result = generate_imports(model)

    assert result == code_strip(expected)


def test_it_splits_model_classes():
    code = """
    from django.db import models
    
    
    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        views_number = models.IntegerField()
        
        
    class User(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
    """

    expected = [
        """
        class Post(models.Model):
            title = models.CharField(max_length=100)
            content = models.TextField()
            views_number = models.IntegerField()
        """,
        """
        class User(models.Model):
            name = models.CharField(max_length=100)
            email = models.EmailField()
        """
    ]

    result = split_model_classes(code)

    assert result == [code_strip(x) for x in expected]


def test_it_generates_factories_code():
    code = """
        from django.db import models


        class Post(models.Model):
            title = models.CharField(max_length=100)
            content = models.TextField()
            views_number = models.IntegerField()


        class User(models.Model):
            name = models.CharField(max_length=100)
            email = models.EmailField()
    """

    expected = """
        import factory
        from factory import fuzzy
    
        from .models import Post, User
        
        
        class PostFactory(factory.django.DjangoModelFactory):
            title = factory.Faker("name")
            content = factory.Faker("paragraph")
            views_number = factory.fuzzy.FuzzyInteger(0, 100)
            
            class Meta:
                model = Post
                
                
        class UserFactory(factory.django.DjangoModelFactory):
            name = factory.Faker("name")
            email = factory.Faker("email")
            
            class Meta:
                model = User
    """

    result = generate_factories_code(code)

    assert result == code_strip(expected)
