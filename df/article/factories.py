import datetime

import factory
from . import models

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Article

    title = str(factory.Faker('name')) + str(factory.Sequence(lambda n: " #%s" % n))
    dt = datetime.datetime.utcnow()
    dt_dvd = datetime.datetime.utcnow()
