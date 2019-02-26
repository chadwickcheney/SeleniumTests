from django.db import models
from jsonfield import JSONField
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Site(models.Model):
    url = models.URLField(max_length=200)
    #url = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.url

    def was_piloted_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Pilot(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    current_rating = models.IntegerField()
    pub_date = models.DateTimeField('date published')

    viewport_json = JSONField(default=[])
    site_json = JSONField(default=[])

    def __str__(self):
        return ("tests object")

class Comment(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(-1)]
        )
