from .models import CustomUser


class ProfileService:

    def __init__(self, user):
        self.user = user

    @staticmethod
    def update_profile_data(validated_data, instance: CustomUser):
        instance.status = validated_data.get('status', instance.status)
        instance.name = validated_data.get('name', instance.name)
        instance.img = validated_data.get('img', instance.img)
