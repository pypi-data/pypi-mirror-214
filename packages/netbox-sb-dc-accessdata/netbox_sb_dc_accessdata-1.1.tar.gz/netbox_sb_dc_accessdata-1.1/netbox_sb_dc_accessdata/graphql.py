from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models

class KeycardType(NetBoxObjectType):

    class Meta:
        model = models.Keycard
        fields = '__all__'
        filterset_class = filtersets.KeycardFilterSet


class KeyType(NetBoxObjectType):

    class Meta:
        model = models.Key
        fields = '__all__'
        filterset_class = filtersets.KeyFilterSet

class Query(ObjectType):
    keycard = ObjectField(KeycardType)
    keycard_list = ObjectListField(KeycardType)

    key = ObjectField(KeyType)
    key_list = ObjectListField(KeyType)

schema = Query