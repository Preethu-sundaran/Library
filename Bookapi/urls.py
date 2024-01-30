from django.urls import path
from .views import *

urlpatterns = [
    path('add_author/',AuthorCreateView.as_view(),name='add-author'),
    path('list_author/',AuthorListView.as_view(),name='list-author'),
    path('get_author/<int:pk>/',AuthorDetailView.as_view(),name='detail-author'),

    path('add_genre/',GenreCreateView.as_view(),name='add-genre'),
    path('list_genre/',GenreListView.as_view(),name='list-genre'),
    path('get_genre/<int:pk>/',GenreDetailCreateView.as_view(),name='detail-genre'),
    path('books_by_genre/<slug:genre_name>/', BooksByGenreView.as_view(), name='books_by_genre'),
    
    path('add_librarian/',LibrarianCreateView.as_view(),name='add-librarian'),
    path('list_librarian/',LibrarianListView.as_view(),name='list-librarian'),
    path('get_librarian/<int:pk>/',LibrarianRetrieveView.as_view(),name='get-librarian'),
    path('update_libarian/<int:pk>/',LibrarianUpdateView.as_view(),name='update-librarian'),
    path('delete_librarian/<int:pk>/',LibrarianDeleteView.as_view(),name='delete-librarian'),

    path('add_library/',LibraryCreateView.as_view(),name='add-library'),
    path('list_library/',LibraryListView.as_view(),name='list-library'),
    path('get_library/<int:pk>/',LibraryRetrieveView.as_view(),name='get-library'),
    path('update_libary/<int:pk>/',LibraryUpdateView.as_view(),name='update-library'),
    path('delete_library/<int:pk>/',LibraryDeleteView.as_view(),name='delete-library'),

    path('add_book/',BookCreateView.as_view(),name='add-book'),
    path('list_book/',BookListView.as_view(),name='list-book'),
    path('get_book/<int:pk>/',BookRetrieveView.as_view(),name='get-book'),
    path('update_book/<int:pk>/',BookUpdateView.as_view(),name='update-book'),
    path('delete_book/<int:pk>/',BookDeleteView.as_view(),name='delete-book'),

    
    
    
    
]