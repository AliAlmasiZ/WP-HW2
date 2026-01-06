from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .models import Ad
from .serializers import AdSerializer, AdAssignSerializer
from .permissions import IsOwnerOrReadOnly, HasApplyPermission, HasAssignPermission
from rest_framework.response import Response


class AdListCreateView(generics.ListCreateAPIView):
    """
    Listing all ads and creating a new ad.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    @extend_schema(
        summary="List Ads / Create Ad",
        description="Retrieve a list of all ads or create a new ad. New ads are set to 'Open' status by default."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(summary="Create a new Ad")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


    
class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an ad instance.
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class AdApplyView(APIView):
    """
    View to apply for an ad.
    """

    permission_classes = [permissions.IsAuthenticated, HasApplyPermission]

    @extend_schema(
        summary="Apply for an Ad (Contractor)",
        description="Contractors use this endpoint to add themselves to the applicants list of an open ad.",
        responses={200: None, 400: None}
    )
    def post(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)

        if ad.status != 'open':
            return Response(
                {'detail': 'This ad is not open for applications.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ad.applicants.add(request.user)
        ad.save()

        return Response(
            {'detail': 'Application submitted successfully.'},
            status=status.HTTP_200_OK
        )
    
    
    def delete(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)

        if request.user not in ad.applicants.all():
            return Response(
                {'detail': 'You have not applied for this ad.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ad.applicants.remove(request.user)
        ad.save()

        return Response(
            {'detail': 'Application withdrawn successfully.'},
            status=status.HTTP_200_OK
        )
    

class AdAssignProviderView(APIView):
    """
    View to assign a provider to an ad.
    """

    permission_classes = [HasAssignPermission]

    @extend_schema(
        summary="Assign Provider (Customer)",
        description="The ad owner selects a provider from the applicants. Ad status changes to 'Assigned'.",
        request=AdAssignSerializer 
    )
    def post(self, request, pk):
        """
        assign a provider to the ad
        """

        ad = get_object_or_404(Ad, pk=pk)

        if ad.owner != request.user:
            return Response(
                {'detail': 'Only the ad owner can assign a provider.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AdAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider_id = serializer.validated_data.get('provider_id')

        from accounts.models import User

        provider = get_object_or_404(User, pk=provider_id)

        if provider not in ad.applicants.all():
            return Response(
                {'detail': 'The selected provider has not applied for this ad.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ad.provider = provider
        ad.status = Ad.AdStatus.PENDING
        ad.applicants.clear()
        ad.save()

        return Response(
            {'detail': 'Provider assigned successfully.'},
            status=status.HTTP_200_OK
        )
    


class AdProvideFinishView(APIView):
    """
    View for provider to mark the ad as done.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)

        if ad.provider != request.user:
            return Response(
                {'detail': 'Only the assigned provider can mark this ad as done.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if ad.status != Ad.AdStatus.ASSIGNED:
            return Response(
                {'detail': 'This ad is not in assigned status.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        ad.status = Ad.AdStatus.WAITING
        ad.save()
        return Response(
            {'detail': 'Ad marked as done, waiting for owner confirmation.'},
            status=status.HTTP_200_OK
        )
    

class AdOwnerConfirmView(APIView):
    """
    View for ad owner to confirm the completion of the ad.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)

        if ad.owner != request.user:
            return Response(
                {'detail': 'Only the ad owner can confirm completion.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if ad.status != Ad.AdStatus.WAITING:
            return Response(
                {'detail': 'This ad is not waiting for confirmation.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        ad.status = Ad.AdStatus.DONE
        ad.save()
        return Response(
            {'detail': 'Ad marked as done successfully.'},
            status=status.HTTP_200_OK
        )
    

class AdCancelView(APIView):
    """
    لغو آگهی توسط مشتری (صاحب آگهی)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)

        if ad.owner != request.user:
            return Response(
                {'detail': 'Only the owner can cancel this ad.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if ad.status == Ad.AdStatus.DONE:
            return Response(
                {'detail': 'Cannot cancel a completed ad.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # ۳. تغییر وضعیت به لغو شده
        ad.status = Ad.AdStatus.CANCELLED
        # اگر بخواهید لیست متقاضیان را هم پاک کنید:
        ad.applicants.clear() 
        ad.save()

        return Response(
            {'detail': 'Ad cancelled successfully.'},
            status=status.HTTP_200_OK
        )