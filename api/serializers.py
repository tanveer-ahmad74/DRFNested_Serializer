from rest_framework import serializers
from .models import Profile, Hobby, Job



class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['user', 'name', 'created_at', 'updated_at']

class ProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True)
    job = JobSerializer(many=True)

    class Meta:
        model = Profile
        fields = ("id", "name", "email", "mobile_number", "status", "created_at", "updated_at", "hobby", "job")



