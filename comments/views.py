from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404
from ads.models import Ad
from .serializers import CommentSerializer
from .models import Comment
from django_filters.rest_framework import DjangoFilterBackend

class AdCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Add Comment to Ad",
        description="Leave a comment and rate the provider after the job is done.",
        request=CommentSerializer,
        examples=[
            OpenApiExample(
                'Positive Review',
                value={
                    "content": "کار بسیار عالی و تمیز انجام شد. ممنونم.",
                    "rate": 5
                },
                request_only=True,
            ),
            OpenApiExample(
                'Negative Review',
                value={
                    "content": "با تاخیر آمدند و کیفیت کار پایین بود.",
                    "rate": 2
                },
                request_only=True,
            )
        ]
    )
    def post(self, request, ad_pk):
        """"
        Create a comment for a specific ad.
        """
        
        ad = get_object_or_404(Ad, pk=ad_pk)
        
        
        if ad.owner != request.user:
            return Response(
                {'detail': 'Only the ad owner can leave a comment.'},
                status=status.HTTP_403_FORBIDDEN
            )

       
        if ad.status != Ad.AdStatus.DONE:
            return Response(
                {'detail': 'You can only comment on completed ads.'},
                status=status.HTTP_400_BAD_REQUEST
            )


        if not ad.provider:
            return Response(
                {'detail': 'This ad has no provider.'},
                status=status.HTTP_400_BAD_REQUEST
            )



        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user, 
                ad=ad, 
                provider=ad.provider
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ContractorCommentsListView(generics.ListAPIView):
    """
    لیست نظرات یک پیمانکار خاص با قابلیت فیلتر بر اساس امتیاز.
    مثال: /comments/contractor/5/?rate=5
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny] # دیدن نظرات معمولاً عمومی است
    
    # فعال‌سازی فیلتر
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rate'] # به کاربر اجازه می‌دهیم روی rate فیلتر کند

    def get_queryset(self):
        contractor_id = self.kwargs.get('contractor_pk')
        return Comment.objects.filter(provider_id=contractor_id)