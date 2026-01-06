from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, permissions, filters
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
import re
from .serializers import *
from .filters import ContractorFilter


EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
            
class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer
    
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer



class UserProfileDetailView(APIView):
    """
    نمایش پروفایل هوشمند بر اساس نقش کاربر
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        is_contractor = user.groups.filter(name='contractor').exists()

        if is_contractor:
            contractor_data = User.objects.filter(pk=pk).annotate(
                avg_rate=Avg('comments__rate'),
                done_ads_count=Count('provided_ads', filter=Q(provided_ads__status='done'))
            ).first()

            serializer = ContractorProfileSerializer(contractor_data)
            return Response(serializer.data)
        
        else:
            serializer = CustomerProfileSerializer(user)
            return Response(serializer.data)
        
class ContractorListView(generics.ListAPIView):
    serializer_class = ContractorListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    
    filterset_class = ContractorFilter
    
    ordering_fields = ['avg_rate', 'done_ads_count', 'date_joined']
    
    search_fields = ['username', 'first_name', 'last_name']

    def get_queryset(self):
        return User.objects.filter(groups__name='contractor').annotate(
            avg_rate=Avg('comments__rate'),
            done_ads_count=Count('provided_ads', filter=Q(provided_ads__status='done'))
        ).order_by('-date_joined')