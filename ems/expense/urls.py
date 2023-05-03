from django.urls import path
from .views import *

urlpatterns = [
    # path('add/',add_expense.as_view(),name='add')
    path('update_project/<int:pk>',ProjectUpdateView.as_view(),name='update_project'),
    path('delete_project/<int:pk>',ProjectDeleteView.as_view(),name='delete_project'),
]