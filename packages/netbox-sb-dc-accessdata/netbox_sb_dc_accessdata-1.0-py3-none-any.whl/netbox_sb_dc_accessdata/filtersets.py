from netbox.filtersets import NetBoxModelFilterSet
from .models import Keycard, Key

class KeycardFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Keycard
        fields = ('id', 'tenant', 'cardnumber', 'firstname', 'lastname')

class KeyFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Key
        fields = ('id', 'tenant', 'keynumber', 'firstname', 'lastname')