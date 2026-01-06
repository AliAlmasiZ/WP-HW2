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
        content = request.data.get('content', '').strip()

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, ad=ad)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    