from rest_framework import serializers
from .models import Animal, Owner
from datetime import date

class AnimalSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    father = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), required=False, allow_null=True)
    mother = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Animal
        fields = '__all__'

    def get_age(self, obj):
        return obj.calculate_age()

class AnimalSearchSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ['id', 'name', 'species', 'breed', 'birth_date', 'age']

    def get_age(self, obj):
        return obj.calculate_age()

class AnimalTreeSerializer(serializers.ModelSerializer):
    father = serializers.SerializerMethodField()
    mother = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ['id', 'name', 'species', 'breed', 'father', 'mother']

    def get_father(self, obj):
        if obj.father:
            return AnimalTreeSerializer(obj.father).data
        return None

    def get_mother(self, obj):
        if obj.mother:
            return AnimalTreeSerializer(obj.mother).data
        return None

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'