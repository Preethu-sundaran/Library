
from django.core.management.base import BaseCommand
from Bookapi.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        try:
            
            author1 = Author.objects.get(id=8)
            author2= Author.objects.create(author_name='Sreethu')
            

            genre1 = Genre.objects.get(id=10)
            genre2 = Genre.objects.get(id=4)

            librarian1 = Librarian.objects.get(id=6)

            library1 = Library.objects.get(id=10)
            library2 = Library.objects.get(id=7)
             
            
            books_to_create = [
                Book(
                    book_name='Hope of Hopeless',
                    author=author1,
                    language='English',
                    price=100,
                    released_year='2012-12-23',
                    copies_available=19,
                    pages=167,
                    library=library1,
                ),
                Book(
                    book_name='Danger',
                    author=author2,
                    language='malayalam',
                    price=300,
                    released_year='2002-08-04',
                    copies_available=1,
                    pages=300,
                    library=library2,
                )
            ]

            Book.objects.bulk_create(books_to_create)

            
            books_created = Book.objects.filter(book_name__in=['Hope of Hopeless', 'Danger'])

        
            for book in books_created:
                if book.book_name == 'Hope of Hopeless':
                    book.genre.set([genre1])
                elif book.book_name == 'Danger':
                    book.genre.set([genre2])

            books_to_update = Book.objects.filter(book_name__in=['Hope of Hopeless', 'Danger'])
            for book in books_to_update:
                if book.book_name == 'Hope of Hopeless':
                    book.price = 50 
                elif book.book_name == 'Danger':
                    book.price = 30  

            Book.objects.bulk_update(books_to_update, ['price'])

            return 'Success'

        except Exception as e:
            return 'Failed'

