from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=45)
    subtitle = models.CharField(max_length=45)
    image_url = models.CharField(max_length=200)
    company = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    about_author = models.TextField()
    contents = models.TextField()
    company_review = models.TextField()
    page = models.IntegerField()
    publication_date = models.DateField()
    description = models.TextField()
    category =
    keyword =

    class Meta:
        db_table = 'books'

class Review(models.Model):
    



class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Keyword(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'keywords'

class Today(models.Model):
    description = models.TextField()
    pick_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = 'today'

class Like(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'


