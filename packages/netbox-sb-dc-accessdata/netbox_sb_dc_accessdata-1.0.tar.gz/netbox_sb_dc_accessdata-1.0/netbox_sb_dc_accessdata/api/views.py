from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import KeycardSerializer, KeySerializer

class KeycardViewSet(NetBoxModelViewSet):
    queryset = models.Keycard.objects.prefetch_related('tags')
    serializer_class = KeycardSerializer
    filterset_class = filtersets.KeycardFilterSet

class KeyViewSet(NetBoxModelViewSet):
    queryset = models.Key.objects.prefetch_related('tags')
    serializer_class = KeySerializer
    filterset_class = filtersets.KeyFilterSet

