from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import Keycard, Key

class KeycardSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_sb_dc_accessdata-api:keycard-detail'
    )
    class Meta:
        model = Keycard
        fields = (
            'id', 'url', 'display', 'tenant', 'cardnumber', 'firstname', 'lastname', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class KeySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_sb_dc_accessdata-api:key-detail'
    )
    class Meta:
        model = Key
        fields = (
            'id', 'url', 'display', 'tenant', 'keynumber', 'firstname', 'lastname', 'tags', 'custom_fields', 'created',
            'last_updated',
        )