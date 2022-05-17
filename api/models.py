from django.db import models
from ckeditor.fields import RichTextField


TAGS = (('SPRING', 'SPRING'), ('FLASK', 'FLASK'), ('DJANGO', "DJANGO"))

CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]
class EmailSubscriber(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField()


class Profile(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    mobile_number = models.IntegerField()
    content = RichTextField(blank=True, null=True)
    tag = models.CharField(choices=TAGS, default='TECH', max_length=25)
    choices = models.CharField(choices=CHOICES, max_length=1)
    status = models.BooleanField(default=1)
    detail = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = "Profiles"


class Hobby(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='hobby')
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hobby'
        verbose_name_plural = "Hobbies"


class Job(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='job')
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = "Jobs"


class Favourite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Favourite'
        verbose_name_plural = 'Favourites'

# class Post(models.Model):
#     title = models.CharField(max_length=100, blank=True, default='')
#     body = models.TextField(blank=True, default='')
#
#
#     class Meta:
#         ordering = ['created']
