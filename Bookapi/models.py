from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length=100)

    def __str__(self):
        return self.author_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_name

class Librarian(models.Model):
    librarian_name = models.CharField(max_length=200)

    def __str__(self):
        return self.librarian_name

class Library(models.Model):
    library_title = models.CharField(max_length=200)
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE,related_name='librarian')
    address = models.TextField()

    def __str__(self):
        return self.library_title

class Book(models.Model):
    book_name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='books')   
    genre = models.ManyToManyField(Genre)  
    language = models.CharField(max_length=200) 
    price = models.PositiveIntegerField()
    released_year = models.DateField()
    copies_available = models.PositiveIntegerField()
    pages = models.PositiveIntegerField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE,related_name='library')


    def __str__(self):
        return self.book_name


    
