from netbox.views import generic
from . import filtersets, forms, models, tables

class KeycardView(generic.ObjectView):
    queryset = models.Keycard.objects.all()

class KeycardListView(generic.ObjectListView):
    queryset = models.Keycard.objects.all()
    table = tables.KeycardTable
    filterset = filtersets.KeycardFilterSet
    filterset_form = forms.KeycardFilterForm

class KeycardEditView(generic.ObjectEditView):
    queryset = models.Keycard.objects.all()
    form = forms.KeycardForm

class KeycardDeleteView(generic.ObjectDeleteView):
    queryset = models.Keycard.objects.all()



class KeyView(generic.ObjectView):
    queryset = models.Key.objects.all()

class KeyListView(generic.ObjectListView):
    queryset = models.Key.objects.all()
    table = tables.KeyTable

class KeyEditView(generic.ObjectEditView):
    queryset = models.Key.objects.all()
    form = forms.KeyForm

class KeyDeleteView(generic.ObjectDeleteView):
    queryset = models.Key.objects.all()

