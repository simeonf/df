import datetime
from haystack import indexes
from article.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    id = indexes.IntegerField(model_attr='id')
    title = indexes.CharField(use_template=True, boost=1.2)
    title_auto = indexes.EdgeNgramField(use_template=True, boost=1.2)
    text = indexes.CharField(document=True, use_template=True)
    text_auto = indexes.EdgeNgramField(use_template=True)
    cast = indexes.CharField(model_attr='cast')
    genre = indexes.MultiValueField(null=True)
    labels = indexes.MultiValueField(null=True)
    year = indexes.IntegerField(null=True, default=None)
    overall = indexes.MultiValueField()
    stars = indexes.MultiValueField()
    moral = indexes.MultiValueField()
    spiritual = indexes.MultiValueField()
    age = indexes.MultiValueField()
    mpaa = indexes.MultiValueField()
    usccb = indexes.MultiValueField()

    def prepare_overall(self, obj):
        return filter(None, [obj.overall])

    def prepare_stars(self, obj):
        return filter(None, [obj.stars])

    def prepare_moral(self, obj):
        return filter(None, [obj.moral])

    def prepare_spiritual(self, obj):
        return filter(None, [obj.spiritual])

    def prepare_age(self, obj):
        return filter(None, [obj.age])

    def prepare_mpaa(self, obj):
        return filter(None, [obj.mpaa])

    def prepare_usccb(self, obj):
        return filter(None, [obj.usccb])

    def prepare_year(self, obj):
        if obj.year and obj.year.isdigit():
            return obj.year
        return None

    def prepare_genre(self, obj):
        return [genre.id for genre in obj.genre.all()]

    def prepare_labels(self, obj):
        return [tag.id for tag in obj.labels.all()]

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(exclude_from_search=False, display=True)
