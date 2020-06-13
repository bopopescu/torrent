from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import random
import hashlib
import datetime
from django.db.models import Q
from django.contrib.auth import get_user_model

from torrent_main.utils.languages import LANGUAGES


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(is_pub=True)

    def get_by_user(self, user, **kwargs):
        if user.is_authenticated:
            res = super(PublishManager, self).get_queryset().filter(Q(**kwargs) &
                                                                    (Q(uploaded_by=user) | Q(is_pub=True)))
        else:
            res = self.get_queryset().filter(**kwargs)

        if len(res) == 1:
            return res[0]
        if not res:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name
            )
        return res


class Type(models.Model):

    type_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.type_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.type_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Torrent(models.Model):

    objects = models.Manager()
    published = PublishManager()

    slug = models.SlugField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ttype = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    # todo: at admin and template i have different view
    language = models.CharField(max_length=30, choices=LANGUAGES)
    total_size = models.CharField(max_length=10, null=True)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    downloads = models.IntegerField(default=0)
    last_checked = models.DateField(null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    seeders = models.IntegerField(null=True)
    leeches = models.IntegerField(null=True)
    # url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='torrent_images')
    file = models.FileField(upload_to='torrent_files')
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_pub = models.BooleanField(default=False)
    info_hash = models.CharField(max_length=50, null=True)
    # tracker_list is actually list. But i think that i dont need to create new model for it.
    # i understand that is bad in SQL. But i think make it in str and split will be better

    # tracker_list = models.TextField()


    class Meta:
        ordering = ('downloads', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + hashlib.md5(str(random.randrange(100000)).encode() +
                                                          str(datetime.datetime.now()).encode()).hexdigest()
        return super().save(*args, **kwargs)

    def get_files(self):
        return TorrentFileInfo.objects.filter(torrent=self)

    def get_comments(self):
        return Comment.objects.filter(torrent=self)

    def get_comment_count(self):
        comments = self.get_comments()
        return len(comments)


class TorrentFileInfo(models.Model):
    size = models.FloatField()
    name = models.CharField(max_length=100)
    torrent = models.ForeignKey(Torrent, on_delete=models.CASCADE)


class Comment(models.Model):
    torrent = models.ForeignKey(Torrent, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)
    text = models.TextField()
