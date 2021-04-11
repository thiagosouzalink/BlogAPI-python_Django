from rest_framework import serializers

from ..models import CustomUser, Post


# Serializar model post
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'text',
            'created_date',
            'updated_date'
        )


# Serializar model usuário
class CustomUserSerializer(serializers.ModelSerializer):

    posts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-detail'
    )

    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }

        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'facebook',
            'instagram',
            'twitter',
            'posts'
        )