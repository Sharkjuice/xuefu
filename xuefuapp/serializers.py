from rest_framework.serializers import HyperlinkedModelSerializer,ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class CarSerializer(ModelSerializer):
     #created_by = serializers.ReadOnlyField(source='created_by.username')
    ground_queue_info = serializers.PrimaryKeyRelatedField(many=True, 
       read_only=True)
    underground_queue_info = serializers.PrimaryKeyRelatedField(many=True, 
        read_only=True)    
    applicant_name = serializers.SerializerMethodField()

    def get_applicant_name(self, obj):
         return obj.applicant_name[0] + "**"

    class Meta:
        model = models.Car
        fields = [f.name for f in model._meta.get_fields()] + \
            ['underground_queue_info','ground_queue_info', 'underground_queue_info_2']
        read_only_fields = fields

class GroundQueueSerializer(ModelSerializer):
     #created_by = serializers.ReadOnlyField(source='created_by.username')
     car = serializers.ReadOnlyField(source='car.car_id')
     class Meta:
        model = models.GroundQueue
        fields = [f.name for f in model._meta.get_fields()]
        read_only_fields = fields  

class UndergroundQueueSerializer(ModelSerializer):
     #created_by = serializers.ReadOnlyField(source='created_by.username')
     car = serializers.ReadOnlyField(source='car.car_id')
     class Meta:
        model = models.UndergroundQueue
        fields = [f.name for f in model._meta.get_fields()]
        read_only_fields = fields


class FeeSerializer(ModelSerializer):
     class Meta:
        model = models.Fee
        fields = [f.name for f in model._meta.get_fields()]
        read_only_fields = fields

class OwnerSerializer(ModelSerializer):
     def validate(self, attrs):
        room_id = attrs['room_id']
        for letter in room_id:
           if letter >= 'a' and letter <= 'z':
               raise serializers.ValidationError('房号不能有小写字母')
        return attrs
     class Meta:
        model = models.Owner
        fields = [f.name for f in model._meta.get_fields()]
        #read_only_fields = fields


