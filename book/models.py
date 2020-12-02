from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'


class Keyword(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'keywords'


class Book(models.Model):
    title             = models.CharField(max_length=45)
    subtitle          = models.CharField(max_length=45, null=True)
    image_url         = models.URLField(max_length=200)
    company           = models.CharField(max_length=45)
    author            = models.CharField(max_length=45)
    about_author      = models.TextField(null=True)
    contents          = models.TextField(default='')
    company_review    = models.TextField(null=True)
    page              = models.IntegerField(default='')
    publication_date  = models.DateField()
    description       = models.TextField(null=True)
    category          = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    keyword           = models.ForeignKey(Keyword, on_delete=models.SET_NULL, null=True)
    reviews           = models.ManyToManyField('user.User', through='Review')

    class Meta:
        db_table = 'books'


class Today(models.Model):
    book         = models.ForeignKey(Book, on_delete=models.CASCADE)
    description  = models.TextField(default='')
    pick_date    = models.DateField()

    class Meta:
        db_table = 'today'


class Review(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    contents    = models.CharField(max_length=200)
    created_at  = models.DateTimeField(auto_now_add=True)
    likes       = models.ManyToManyField('user.User', through='Like', related_name='review_likes')

    class Meta:
        db_table = 'reviews'


class Like(models.Model):
    review  = models.ForeignKey(Review, on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
