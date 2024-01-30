from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters,status
from django.contrib import messages
from django.http.response import Http404
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import *

class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        author_name = request.data.get('author_name')
        existing_author = Author.objects.filter(author_name=author_name).exists()

    
        if existing_author:
            message = "Author with the name '{}' already exists.".format(author_name)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response({"message": "New Author Added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreCreateView(generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def create(self, request, *args, **kwargs):
        genre_name = request.data.get('genre_name')
        existing_genre = Genre.objects.filter(genre_name=genre_name).first()

    
        if existing_genre:
            message = "Genre with the name '{}' already exists.".format(genre_name)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response({"message": "New Genre Added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreDetailCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class LibrarianCreateView(generics.CreateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

    def create(self, request, *args, **kwargs):
        librarian_name = request.data.get('librarian_name')


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response({"message": "Librarian Added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class LibrarianListView(generics.ListAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

class LibrarianRetrieveView(generics.RetrieveAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

    def get(self, request, pk, format=None):
        try:
            instance = self.get_object()
            serializer = LibrarianSerializer(instance)
            return Response({
                "status": "success",
                "message": "Librarian details retrieved successfully",
                "body": serializer.data,
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "status": "not found",
                "message": "Librarian does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

class LibrarianUpdateView(generics.UpdateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

    def put(self, request, pk, format=None):
        instance = self.get_object()
        serializer = LibrarianSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Librarian successfully updated.')
            return Response({
                "status": "success",
                "message": "Successfully Updated!",
                "body": serializer.data,
            }, status=200)
        else:
            messages.error(request, 'Failed to update librarian. Please check the data.')
            return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        instance = self.get_object()
        serializer = LibrarianSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Librarian successfully patched!')
            return Response({
                "status": "success",
                "message": "Successfully Patched!",
                "body": serializer.data,
            }, status=200)
        else:
            messages.error(request, 'Failed to update librarian. Please check the data.')
            return Response(serializer.errors, status=400)

class LibrarianDeleteView(generics.DestroyAPIView):
    queryset = Librarian.objects.all()

    def delete(self, request, pk, format=None):
        librarian = self.get_object()
        try:
            librarian.delete()
            messages.success(request, 'Librarian successfully deleted.')
            return Response({
                "Status": "Success",
                "Message": "Librarian deleted"
            }, status=204)
        except Exception as e:
            messages.error(request, f'Failed to delete Librarian. Error: {str(e)}')
            return Response({
                "Status": "Failed",
                "Message": "Librarian Deletion Failed"
            }, status=500)


class LibraryCreateView(generics.CreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def create(self, request, *args, **kwargs):
        library_title  = request.data.get('library_name')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response({"message": "Library Added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class LibraryListView(generics.ListAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class LibraryRetrieveView(generics.RetrieveAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def get(self, request, pk, format=None):
        try:
            instance = self.get_object()
            serializer = LibrarySerializer(instance)
            return Response({
                "status": "success",
                "message": "Library details retrieved successfully",
                "body": serializer.data,
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "status": "not found",
                "message": "Library does not exist",
            }, status=status.HTTP_404_NOT_FOUND)


class LibraryUpdateView(generics.UpdateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def put(self, request, pk, format=None):
        instance = self.get_object()
        serializer = LibrarySerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Library successfully updated.')
            return Response({
                "status": "success",
                "message": "Successfully Updated!",
                "body": serializer.data,
            }, status=200)
        else:
            messages.error(request, 'Failed to update library. Please check the data.')
            return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        instance = self.get_object()
        serializer = LibrarySerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Library successfully patched!')
            return Response({
                "status": "success",
                "message": "Successfully Patched!",
                "body": serializer.data,
            }, status=200)
        else:
            messages.error(request, 'Failed to update library. Please check the data.')
            return Response(serializer.errors, status=400)

class LibraryDeleteView(generics.DestroyAPIView):
    queryset = Library.objects.all()

    def delete(self, request, pk, format=None):
        library = self.get_object()
        try:
            library.delete()
            messages.success(request, 'Library successfully deleted.')
            return Response({
                "Status": "Success",
                "Message": "Library deleted"
            }, status=204)
        except Exception as e:
            messages.error(request, f'Failed to delete Library. Error: {str(e)}')
            return Response({
                "Status": "Failed",
                "Message": "Library Deletion Failed"
            }, status=500)

 
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    
 
    def get_serializer_class(self):
        return BookCreateSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        self.perform_create(serializer)

        
        return Response({"message": "New Book Added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
 
    def perform_create(self, serializer):
        serializer.save()

class BookListView(generics.ListAPIView):
    queryset = Book.objects.only('book_name','author','language','price').select_related('author').prefetch_related('genre')
    serializer_class = BookSerializer
 
class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk, format=None):
        try:
            instance = self.get_object()
            serializer = BookSerializer(instance)
            return Response({
                "status": "success",
                "message": "Book details retrieved successfully",
                "body": serializer.data,
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "status": "not found",
                "message": "Book does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer

    def put(self, request, pk, format=None):
        instance = self.get_object()
        serializer = BookCreateSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Book successfully updated.')
            return Response({
                "status": "success",
                "message": "Successfully Updated!",
                "body": serializer.data,
            }, status=200)
        else:
            messages.error(request, 'Failed to update book. Please check the data.')
            return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        instance = self.get_object()
        serializer = BookCreateSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Book successfully patched!')
            return Response({
                "status": "success",
                "message": "Successfully Patched!",
                "body": serializer.data,
            }, status=200)
        else:
            messages.error(request, 'Failed to update book. Please check the data.')
            return Response(serializer.errors, status=400)

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()

    def delete(self, request, pk, format=None):
        book = self.get_object()
        try:
            book.delete()
            messages.success(request, 'Book successfully deleted.')
            return Response({
                "Status": "Success",
                "Message": "Book deleted"
            }, status=204)
        except Exception as e:
            messages.error(request, f'Failed to delete book. Error: {str(e)}')
            return Response({
                "Status": "Failed",
                "Message": "Book Deletion Failed"
            }, status=500)


class BookListByPriceView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        price = self.request.query_params.get('price')
        queryset = Book.objects.all()
        limit = 100
        if price<=100:
            return Response('Low Price')
        else:
            return Response('High Price')


class BooksByGenreView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
  
        genre = get_object_or_404(Genre, genre_name=self.kwargs['genre_name'])

        return genre.book_set.all().select_related('author').prefetch_related('genre')

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        total_count = queryset.count()
        response_data = {
            
            'total_count': total_count,
            'books': serializer.data,
        }

        return Response(response_data)