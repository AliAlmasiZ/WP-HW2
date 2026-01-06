from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model.

    This serializer handles the serialization and deserialization of Ticket instances.
    It automatically sets the 'owner' field to the username of the user creating the ticket
    and ensures that sensitive or system-managed fields cannot be modified during creation.

    Attributes:
        owner (ReadOnlyField): Display the username of the ticket owner instead of the ID.

    Meta:
        model (Ticket): The model class associated with this serializer.
        fields (str): '__all__' indicates all model fields are included.
        read_only_fields (list): Fields that cannot be set by the user during write operations:
            - owner: Automatically set based on the request user.
            - status: Defaults to a system-defined initial status.
            - answer: Admin-only field for responding to tickets.
            - created_at: Automatically set by the timestamp of creation.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['owner', 'status', 'answer', 'created_at']


class TicketReplySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Ticket
        fields = ['answer', 'status']