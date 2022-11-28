from rest_framework import serializers

from orders.models import Blanket


class BlanketSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    menu = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Blanket
        fields = '__all__'
