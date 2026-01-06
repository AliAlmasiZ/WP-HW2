from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password
from .models import User
from comments.serializers import CommentSerializer  


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context.get("request")
        
        return data
    

class TokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context.get("request")
        
        return data
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])


    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone_number')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user



class ContractorProfileSerializer(serializers.ModelSerializer):
    avg_rate = serializers.FloatField(read_only=True)
    done_ads_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avg_rate', 'done_ads_count', 'comments')


class CustomerProfileSerializer(serializers.ModelSerializer):
    my_ads = serializers.SerializerMethodField()

    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'my_ads')

    def get_my_ads(self, obj):
        from ads.serializers import AdSerializer
        from ads.models import Ad
        
        ads = Ad.objects.filter(owner=obj)
        return AdSerializer(ads, many=True).data
    

class ContractorListSerializer(serializers.ModelSerializer):
    avg_rate = serializers.FloatField(read_only=True)
    done_ads_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avg_rate', 'done_ads_count')