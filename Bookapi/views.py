import logging
import datetime
import openpyxl
import xlwt
import csv
from openpyxl import Workbook
from django.http import HttpResponse
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters,status
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.generics import *
from rest_framework import filters
from rest_framework import status
from rest_framework.pagination import CursorPagination
from django.contrib import messages
from django.http.response import Http404
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import *
from .serializers import *
from django.db.models import F

logger = logging.getLogger(__name__)

class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializers
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
      
        user = serializer.instance
        content_type = ContentType.objects.get_for_model(Book)
        permissions = Permission.objects.filter(
            codename__in=['create_book','modify_book','destroy_book'],
            content_type=content_type
        )
        user.user_permissions.add(*permissions)

        return Response({"message": "User registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

       
    def perform_create(self, serializer):
        serializer.save()


class Login(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            try:
                user_obj = CustomUser.objects.get(
                    Q(username__iexact=data["username"]) | Q(email__iexact=data["username"])
                )
                
                
                if user_obj.status == 0:
                    if check_password(data["password"], user_obj.password):
                        user_obj.last_login = datetime.datetime.now()
                        user_obj.save()
                        refresh_token = RefreshToken.for_user(user_obj)
                        resp = LoginResponseSerializer(instance=user_obj)
                        return Response(resp.data, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Invalid password", "status": "1"})
                else:
                    return Response({"message": "you are blocked by admin"})

            except CustomUser.DoesNotExist:
                logger.error('Invalid user')
                return Response({"message": "Invalid user", "status": "1"})
                
                
            except Exception as e:
                logger.error('An error occurred: %s', str(e))
                return Response({"message": "An error occurred", "status": "1"})
        else:
            logger.error('Serializer errors: %s', serializer.errors)
            return Response(serializer.errors)

class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        author_name = request.data.get('author_name')
        existing_author = Author.objects.filter(author_name=author_name).exists()

    
        if existing_author:
            message = "Author with the name '{}' already exists.".format(author_name)
            logger.warning(message)
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
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GenreCreateView(generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        genre_name = request.data.get('genre_name')
        existing_genre = Genre.objects.filter(genre_name=genre_name).exists()

    
        if existing_genre:
            message = "Genre with the name '{}' already exists.".format(genre_name)
            logger.warning(message)
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
    permission_classes = [IsAuthenticated, IsAdminUser]

class GenreDetailCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class LibrarianCreateView(generics.CreateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated, IsAdminUser]

class LibrarianRetrieveView(generics.RetrieveAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
            message = "Librarian with ID '{}' does not exist.".format(pk)
            logger.error(message)
            return Response({
                "status": "not found",
                "message": message,
            }, status=status.HTTP_404_NOT_FOUND)

class LibrarianUpdateView(generics.UpdateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated, IsAdminUser]

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
            message = "Failed to delete librarian with ID '{}'. Error: {}".format(pk, str(e))
            logger.error(message)
            return Response({
                "Status": "Failed",
                "Message": "Librarian Deletion Failed"
            }, status=500)


class LibraryCreateView(generics.CreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated]

class LibraryRetrieveView(generics.RetrieveAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated]

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
            message = "Library with ID '{}' does not exist.".format(pk)
            logger.error(message)
            return Response({
                "status": "not found",
                "message": "Library does not exist",
            }, status=status.HTTP_404_NOT_FOUND)


class LibraryUpdateView(generics.UpdateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated, IsAdminUser]

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
            message = "Failed to delete library with ID '{}'. Error: {}".format(pk, str(e))
            logger.error(message)
            return Response({
                "Status": "Failed",
                "Message": "Library Deletion Failed"
            }, status=500)

 
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [IsAuthenticated]
    
 
    def get_serializer_class(self):
        return BookCreateSerializer
 
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('Bookapi.create_book'):
            message = "User '{}' does not have permission to create a book.".format(request.user.username)
            logger.warning(message)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        self.perform_create(serializer)

        
        return Response({"message": "New Book Added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
 
    def perform_create(self, serializer):
        serializer.save()


class BookListPagination(CursorPagination):
    page_size = 5
    ordering = 'id'


class BookListView(generics.ListAPIView):
    queryset = Book.objects.only('book_name', 'author', 'language', 'price').select_related('author').prefetch_related('genre').order_by(F('price').asc())
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['book_name', 'author__author_name', 'genre__genre_name']
    pagination_class = BookListPagination


    
    def get_queryset(self):
        queryset = super().get_queryset()

        ordering = self.request.query_params.get('ordering', 'book_name')
        queryset = queryset.order_by(ordering)

        return queryset

class ExportBookToExcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Book.objects.only('book_name','author','language','price').select_related('author').prefetch_related('genre')
        serializer = BookSerializer(queryset, many=True)

       
        wb = Workbook()
        ws = wb.active

        headers = ['ID', 'Book Name', 'Author', 'Language', 'Price']

        ws.append(headers)

        for book in serializer.data:
            ws.append([
                book['id'],
                book['book_name'],
                book['author']['author_name'],
                book['language'],
                book['price']
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=book_list.xlsx'

        wb.save(response)

        return response   


class ExportBookIntoXlwtView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        queryset = Book.objects.only('book_name','author','language','price').select_related('author').prefetch_related('genre')
        serializer = BookSerializer(queryset,many=True)

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Book List')

        headers = ['ID','BOOK NAME','AUTHOR','LANGUAGE','PRICE']

        for col,header in enumerate(headers):
            ws.write(0,col,header)

        for row,book in enumerate(serializer.data,start=1):
            ws.write(row,0,book['id'])
            ws.write(row,1,book['book_name'])
            ws.write(row,2,book['author']['author_name'])
            ws.write(row,3,book['language'])
            ws.write(row,4,book['price'])

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=xlwt_book_list.xls'
        wb.save(response)
        return response

        
class ExportBookIntoCSVView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Book.objects.only('book_name', 'author', 'language', 'price').select_related('author').prefetch_related('genre')
        serializer = BookSerializer(queryset, many=True)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="csv_listbook.csv"'

        writer = csv.writer(response ,delimiter=',')
        
       
        writer.writerow(['ID', 'Book Name', 'Author', 'Language', 'Price'])

        for book in serializer.data:
            writer.writerow([
                book['id'],
                book['book_name'],
                book['author']['author_name'],
                book['language'],
                book['price']
            ])

        return response

class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

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
            message = "Book with ID '{}' does not exist.".format(pk)
            logger.error(message)
            return Response({
                "status": "not found",
                "message": message,
            }, status=status.HTTP_404_NOT_FOUND)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        instance = self.get_object()

        if not request.user.has_perm('Bookapi.modify_book'):
            message = "User '{}' does not have permission to modify this book.".format(request.user.username)
            logger.warning(message)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)
        
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

        if not request.user.has_perm('Bookapi.modify_book'):
            message = "User '{}' does not have permission to modify this book.".format(request.user.username)
            logger.warning(message)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

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
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        book = self.get_object()

        if not request.user.has_perm('Bookapi.destroy_book'):
            message = "User '{}' does not have permission to delete this book.".format(request.user.username)
            logger.warning(message)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        try:
            book.delete()
            messages.success(request, 'Book successfully deleted.')
            return Response({
                "Status": "Success",
                "Message": "Book deleted"
            }, status=204)
        except Exception as e:
            message = "Failed to delete book with ID '{}'. Error: {}".format(pk, str(e))
            logger.error(message)
            # messages.error(request, f'Failed to delete book. Error: {str(e)}')
            return Response({
                "Status": "Failed",
                "Message": message,
            }, status=500)


class BookListByPriceView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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