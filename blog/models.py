import os.path
from turtle import mode
from django.db import models
from django.contrib.auth.models import User

from markdown import markdown
from markdownx.models import MarkdownxField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'categories'
    # 오류 여기서 c를 C라고 적음


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    hook = models.TextField(blank=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    # ForeingKey를 통해 라이브러리 모델의 레퍼런스값 키를 받아오는 함수에서 매개변수로는 User
    # 그리고 삭제되었을때, 작성자만 지우는게아니라, 글도 같이 삭제되게끔.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   # Create your models here.

    # method 메소드 오버라이딩
    def __str__(self):
        return f'[{self.pk}] [{self.title}] :: {self.author}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
# 에러시 return os.path.basename(self.attached_file.name) 로변경
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_markdown_content(self):
        return markdown(self.content)