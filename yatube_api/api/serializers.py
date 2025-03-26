from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post
import base64
import datetime as dt
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка 
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')  
            # И извлечь расширение файла.
            ext = format.split('/')[-1]  
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    #author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        fields = ('id', 'text', 'image', 'author', 'pub_date')
        model = Post
        read_only_fields = ('author',)
    
    


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username'
    # )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author',)

