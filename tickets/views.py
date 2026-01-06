from rest_framework import generics, permissions
from .serializers import TicketSerializer, TicketReplySerializer
from .models import Ticket
from .permissions import canAnswerTicket, canEditTicket
from drf_spectacular.utils import extend_schema

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.has_perm('tickets.can_see_all_tickets') or user.is_superuser:
            return Ticket.objects.all()
        
        return Ticket.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        summary="List Tickets / Create Ticket",
        description="Standard users see only their own tickets. Support users see all tickets."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, canEditTicket]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH'] and self.request.user.has_perm('tickets.can_answer_ticket'):
            return TicketReplySerializer
        return TicketSerializer
    
