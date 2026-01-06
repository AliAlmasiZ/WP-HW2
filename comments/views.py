from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ads.models import Ad
from .serializers import CommentSerializer

class AdCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    