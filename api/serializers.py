from rest_framework import serializers

from contacts.models import Contact, PhoneNumber


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('title', 'phone_number')


class ContactSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True)

    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone_numbers')

    @staticmethod
    def __get_phone_numbers(validated_data):
        phone_numbers = PhoneNumber.objects.bulk_create(
            [PhoneNumber(**phone_number_data) for phone_number_data in validated_data.get('phone_numbers')]
        )
        del validated_data['phone_numbers']

        return phone_numbers

    def create(self, validated_data):
        phone_numbers = self.__get_phone_numbers(validated_data)

        contact = Contact.objects.create(**validated_data)
        contact.phone_numbers.set(phone_numbers)
        contact.save()

        return contact

    def update(self, instance, validated_data):
        phone_numbers = self.__get_phone_numbers(validated_data)

        for field_name, field_value in validated_data.items():
            setattr(instance, field_name, field_value)

        instance.phone_numbers.set(phone_numbers)
        instance.save()

        return instance

