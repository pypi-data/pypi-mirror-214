from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (
    path('keycard/', views.KeycardListView.as_view(), name='keycard_list'),
    path('keycard/add/', views.KeycardEditView.as_view(), name='keycard_add'),
    path('keycard/<int:pk>/', views.KeycardView.as_view(), name='keycard'),
    path('keycard/<int:pk>/edit/', views.KeycardEditView.as_view(), name='keycard_edit'),
    path('keycard/<int:pk>/delete/', views.KeycardDeleteView.as_view(), name='keycard_delete'),
    path('keycard/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='keycard_changelog', kwargs={
        'model': models.Keycard
    }),

    path('key/', views.KeyListView.as_view(), name='key_list'),
    path('key/add/', views.KeyEditView.as_view(), name='key_add'),
    path('key/<int:pk>/', views.KeyView.as_view(), name='key'),
    path('key/<int:pk>/edit/', views.KeyEditView.as_view(), name='key_edit'),
    path('key/<int:pk>/delete/', views.KeyDeleteView.as_view(), name='key_delete'),
    path('key/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='key_changelog', kwargs={
        'model': models.Key
    }),
)
