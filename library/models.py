from django.db import models


class Library(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    name       = models.CharField(max_length=45)
    image_url  = models.URLField(max_length=200)
    books      = models.ManyToManyField('book.Book', through='LibraryBook')

    class Meta:
        db_table = 'libraries'


class LibraryBook(models.Model):
    library     = models.ForeignKey(Library, on_delete=models.CASCADE)
    book        = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'library_books'
