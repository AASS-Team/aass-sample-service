from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from samples.models import Sample


class SamplesList(APIView):
    """
    List all samples, or create a new sample.
    """

    serializer_class = serializers.SampleSerializer

    def get(self, request, format=None):
        samples = Sample.objects.all()
        serializer = self.serializer_class(samples, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                    "message": "Nepodarilo sa uložiť vzorku",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(available=True)
        return Response(
            data={
                "message": "Vzorka uložená",
            },
            status=status.HTTP_201_CREATED,
        )


class SampleDetail(APIView):
    """
    Retrieve, update or delete a sample instance.
    """

    def get_object(self, id):
        try:
            return Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            raise NotFound()

    def get(self, request, id, format=None):
        sample = self.get_object(id)
        serializer = serializers.SampleSerializer(sample)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        sample = self.get_object(id)
        serializer = serializers.SampleSerializer(sample, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "message": "Nepodarilo sa uložiť vzorku",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data={"message": "Vzorka uložená"})

    def delete(self, request, id, format=None):
        sample = self.get_object(id)
        sample.delete()

        return Response(
            data={
                "message": "Vzorka vymazaná",
            },
        )
