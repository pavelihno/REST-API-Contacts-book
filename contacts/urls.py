from django.urls import path, re_path

from contacts.views import ContactsAPIView, ContactAPIView, ContactsListView, ContactDetailView

urlpatterns = [
    path('', ContactsAPIView.as_view()),
    path('<int:pk>', ContactAPIView.as_view()),
    path('list/', ContactsListView.as_view()),
    path('list/<int:pk>', ContactDetailView.as_view(), name='contact_detail')
]
