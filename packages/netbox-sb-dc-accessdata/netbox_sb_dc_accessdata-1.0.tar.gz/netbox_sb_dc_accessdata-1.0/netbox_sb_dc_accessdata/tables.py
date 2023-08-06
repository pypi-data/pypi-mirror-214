import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn
from tenancy.tables import ContactsColumnMixin, TenancyColumnsMixin
from .models import Keycard, Key

class KeycardTable(TenancyColumnsMixin, ContactsColumnMixin, NetBoxTable):
    cardnumber = tables.Column(
        linkify=True
    )
    class Meta(NetBoxTable.Meta):
        model = Keycard
        fields = ('id', 'tenant', 'tenant_group', 'cardnumber', 'firstname', 'lastname', 'created')
        default_columns = ('id', 'tenant', 'cardnumber', 'firstname', 'lastname', 'created')

class KeyTable(TenancyColumnsMixin, ContactsColumnMixin,NetBoxTable):
    keynumber = tables.Column(
        linkify=True
    )
    class Meta(NetBoxTable.Meta):
        model = Key
        fields = ('id', 'tenant', 'tenant_group', 'keynumber', 'firstname', 'lastname', 'created')
        default_columns = ('id', 'tenant', 'keynumber', 'firstname', 'lastname', 'created')