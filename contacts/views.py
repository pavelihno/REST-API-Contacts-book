from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ContactSerializer
from contacts.models import Contact


class ContactsAPIView(APIView):
    def get(self, request):
        contacts = Contact.objects.all()

        serializer = ContactSerializer(contacts, many=True)

        return Response({'contacts': serializer.data})

    def post(self, request):
        contact = request.data.get('contacts')

        serializer = ContactSerializer(data=contact)

        if serializer.is_valid(raise_exception=False):
            saved_contact = serializer.save()

            return Response({
                'success': f"Contact '{saved_contact.name}' was successfully created!"
            })
        return Response({
            'error': f"Contact wasn't created! {serializer.errors}"
        })

    def delete(self, request):
        contacts = Contact.objects.all()

        contacts.delete()

        return Response({
            'success:': f'All contacts were successfully deleted!'
        })


class ContactAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        try:
            contact = Contact.objects.get(pk=pk)
            serializer_data = ContactSerializer(contact, many=False).data

        except Contact.DoesNotExist:
            serializer_data = []

        return Response({'contacts': serializer_data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        try:
            saved_contact = Contact.objects.get(pk=pk)

            serializer = ContactSerializer(instance=saved_contact, data=request.data.get('contacts'), partial=True)

            if serializer.is_valid(raise_exception=False):
                saved_contact = serializer.save()
                return Response({
                    'success': f"Contact '{saved_contact.name}' was successfully updated!"
                })
            return Response({
                'error': f"Contact wasn't updated! {serializer.errors}"
            })

        except Contact.DoesNotExist:
            pass

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        try:
            contact = Contact.objects.get(pk=pk)
            contact_name = contact.name
            contact.delete()

            return Response({
                'success:': f"Contact '{contact_name}' was successfully deleted!"
            })

        except Contact.DoesNotExist:
            pass

        return Response({
            'error:': f"Contact doesn't exist!"
        })


class ContactsListView(ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'contacts_list.html'


class ContactDetailView(DetailView):
    model = Contact
    slug_url_kwarg = 'pk'
    context_object_name = 'contact'
    template_name = 'contact.html'
