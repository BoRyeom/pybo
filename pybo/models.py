from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.name])

class Question(models.Model):
    class Meta:
        ordering = ['id']

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')  # , null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # voter 추가
    view_count = models.IntegerField(null=True, blank=True, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('pybo:detail', args=[self.id])

    def get_recent_comments(self):
        return self.comment_set.all().order_by('-create_date')[:5]

class QuestionCount(models.Model):
    ip = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.ip


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # , null=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')  # voter 추가

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # , null=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
