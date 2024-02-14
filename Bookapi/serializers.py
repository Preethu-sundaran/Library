from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from decimal import Decimal

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)
    

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "email",  
            "first_name",
            "last_name",
            
        ]


   

    def create(self, validated_data):
        

        user = CustomUser.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password']),
           
           
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={"input_type":"password"})

class LoginResponseSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    def get_refresh_token(self,instance):
        return str(RefreshToken.for_user(instance))
    def get_access_token(self,instance):
        return str(RefreshToken.for_user(instance).access_token)

    class Meta:
        model = CustomUser
        fields =[
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "access_token",
            "refresh_token",
            
        ]
        

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
        fields = ['id','book_name','genre_name','price','author','price_details','language']
    
    def get_price_details(self,instance):
        limit = 100
        if instance.price<=100:
            data = 'Low price'
            return data
        if instance.price>100:
            data = 'High Price'
            return data
            

