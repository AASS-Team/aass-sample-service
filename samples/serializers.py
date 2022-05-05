from rest_framework import serializers

from samples.models import Sample


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return round(value.timestamp() * 1000)


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"

    available = serializers.ReadOnlyField()
    created_at = TimestampField(required=False)
