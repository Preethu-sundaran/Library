from django.core.management.base import BaseCommand
from Bookapi.models import *
from django.core.exceptions import ValidationError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--author_id', type=int)
        parser.add_argument('--genre1_id', type=int)
        parser.add_argument('--genre2_id', type=int)
        parser.add_argument('--librarian_id', type=int)
        parser.add_argument('--library1_id', type=int)
        parser.add_argument('--library2_id', type=int)


    def handle(self, *args, **options):
        
        try:

            author_id = options['author_id'] 
            
            author1 = Author.objects.get(id=author_id)

            author_name = 'Aravindh Raj'
            author2, created2 = Author.objects.get_or_create(author_name=author_name)

            genre1_id = options['genre1_id']
            genre2_id = options['genre2_id']
            librarian_id = options['librarian_id']
            library1_id = options['library1_id']
            library2_id = options['library2_id']

            genre1 = Genre.objects.get(id=genre1_id)
            genre2 = Genre.objects.get(id=genre2_id)
            librarian1 = Librarian.objects.get(id=librarian_id)
            library1 = Library.objects.get(id=library1_id)
            library2 = Library.objects.get(id=library2_id)
            
                         
            books_to_create = [
                Book(
                    book_name='Iam dead',
                    author=author1,
                    language='malayalam',
                    price=100,
                    released_year='2012-12-23',
                    copies_available=19,
                    pages=167,
                    library=library1,
                ),
                Book(
                    book_name='Spiritual',
                    author=author2,
                    language='English',
                    price=300,
                    released_year='2002-08-04',
                    copies_available=1,
                    pages=300,
                    library=library2,
                )
            ]


            existing_book_names = set(Book.objects.values_list('book_name', flat=True))
            for new_book in books_to_create:
                if new_book.book_name in existing_book_names:
                    raise ValidationError('Book with the same name already exists')

            
            books_created = Book.objects.bulk_create(books_to_create)

            for book in books_created:
                if book.book_name == 'Iam dead':
                    book.genre.set([genre1])
                elif book.book_name == 'Spiritual':
                    book.genre.set([genre2])

            books_to_update = Book.objects.filter(book_name__in=['Hope of Hopeless', 'Danger'])
            for book in books_to_update:
                if book.book_name == 'Hope of Hopeless':
                    book.price = 50 
                elif book.book_name == 'Danger':
                    book.price = 30  

            Book.objects.bulk_update(books_to_update, ['price'])

            return 'Success'

        except ValidationError as ve:
            return f'Failed: {ve}'
        except Exception as e:
            return f'Failed: {e}'

