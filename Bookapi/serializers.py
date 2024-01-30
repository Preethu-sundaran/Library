from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ShowGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Librarian
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class BookCreateSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(write_only=True)
 
   
    genre_details = GenreSerializer(source='genre', read_only=True, many=True)
 
    class Meta:
        model = Book
        fields = '__all__'


    def create(self, validated_data):
        
        genre_data = validated_data.pop('genre', '')
        genre_ids = [int(gen_id.strip()) for gen_id in genre_data.split(',') if gen_id.strip()]
        book = Book.objects.create(**validated_data)
        book.genre.set(genre_ids)
 
        return book
 


        
class BookSerializer(serializers.ModelSerializer):
    price_details = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    genre_name = ShowGenreSerializer(many=True,source='genre',read_only=True)
    
    class Meta:
        model = Book
        fields = ['id','book_name','genre_name','price','author','price_details']
    
    def get_price_details(self,instance):
        limit = 100
        if instance.price<=100:
            data = 'Low price'
            return data
        if instance.price>100:
            data = 'High Price'
            return data
            

