from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from tenancy.forms import TenancyForm
from .models import Keycard, Key

class KeycardForm(TenancyForm, NetBoxModelForm):
    class Meta:
        model = Keycard
        fields = ('cardnumber', 'tenant_group', 'tenant', 'firstname', 'lastname')

class KeyForm(TenancyForm, NetBoxModelForm):
    class Meta:
        model = Key
        fields = ('keynumber', 'tenant_group', 'tenant', 'firstname', 'lastname')

class KeycardFilterForm(NetBoxModelFilterSetForm):
    model = Keycard

class KeyFilterForm(NetBoxModelFilterSetForm):
    model = Key