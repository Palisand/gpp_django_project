from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateField()
    common_id = models.IntegerField(default=None, null=True)
    section_id = models.IntegerField(default=None, null=True)
    pub_or_foil = models.CharField(max_length=120)
    agency = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    url = models.URLField()

    def __unicode__(self):
        return self.title