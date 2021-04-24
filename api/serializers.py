from rest_framework import serializers
from api.models import *


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingProgram
        fields = '__all__'


class WashingMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingMachine
        exclude = [
            'enabled',
        ]

    available = serializers.BooleanField()
    programs = ProgramSerializer(many=True)
    building = serializers.SlugRelatedField(slug_field='name', read_only=True)

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        exclude=[]

class RunRequestSerializer(serializers.Serializer):
    resident = serializers.SlugRelatedField(many=False,
                                            read_only=False,
                                            required=True,
                                            slug_field='rfid_uid',
                                            queryset=Resident.objects.all())
    program = serializers.PrimaryKeyRelatedField(many=False,
                                                 read_only=False,
                                                 required=True,
                                                 queryset=WashingProgram.objects.all())

    # machine = serializers.PrimaryKeyRelatedField(many=False,read_only=False,queryset=WashingMachine.objects.filter(enabled=True))

    def create(self, validated_data) -> RunRequest:
        return RunRequest(**validated_data)


class RunResponseSerializer(serializers.Serializer):
    operation_status = serializers.BooleanField()
    machine = WashingMachineSerializer()
    resident = ResidentSerializer()
    program = ProgramSerializer()
    errors = serializers.ListSerializer(child=serializers.IntegerField())
    details = serializers.ListSerializer(child=serializers.CharField())
