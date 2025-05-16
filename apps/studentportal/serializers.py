# apps/studentportal/serializers.py

from rest_framework import serializers
from .models import Studentprtal
from .models import Notification
from apps.users.models import CustomUser

class StudentprtalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Studentprtal
        fields = '__all__'

    def validate_title(self, value):
        qs = Studentprtal.objects.filter(title=value)
        if self.instance:  # يعني في حالة التعديل
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This title already exists")
        return value
    def get_image(self, obj):
        return self._abs_url(obj.image) if obj.image else None





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
