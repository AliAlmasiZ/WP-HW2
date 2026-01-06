from rest_framework import serializers
from .models import Comment



class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'rate']
        read_only_fields = ['owner', 'ad', 'created_at']