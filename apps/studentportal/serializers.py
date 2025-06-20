# apps/studentportal/serializers.py

from rest_framework import serializers
from .models import StudentPortalImage, Studentprtal
from .models import Notification
from apps.users.models import CustomUser

class StudentPortalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPortalImage
        fields = ['id', 'image']

class StudentprtalSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    extra_images = StudentPortalImageSerializer(many=True, read_only=True)
    extra_images_upload = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Studentprtal
        fields = '__all__'

    def validate_title(self, value):
        qs = Studentprtal.objects.filter(title=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This title already exists")
        return value

    def create(self, validated_data):
        extra_images_data = validated_data.pop('extra_images_upload', [])
        portal = Studentprtal.objects.create(**validated_data)
        for img in extra_images_data:
            StudentPortalImage.objects.create(portal=portal, image=img)
        return portal

    def update(self, instance, validated_data):
        extra_images_data = validated_data.pop('extra_images_upload', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for img in extra_images_data:
            StudentPortalImage.objects.create(portal=instance, image=img)
        return instance




# notifications/serializers.py


class ReceiverInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class NotificationSerializer(serializers.ModelSerializer):
    receiver_info = ReceiverInfoSerializer(source='receiver', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'created_at', 'receiver', 'receiver_info', 'send_to_all']
        read_only_fields = ['id', 'created_at', 'receiver_info']

    def validate(self, data):
        send_to_all = data.get('send_to_all', False)
        receiver = data.get('receiver', None)

        if send_to_all and receiver:
            raise serializers.ValidationError("You cannot select 'Send to all' and select a graduate at the same time.")
        if not send_to_all and not receiver:
            raise serializers.ValidationError("You must select either 'Send to all' or a specific graduate.")
        return data
