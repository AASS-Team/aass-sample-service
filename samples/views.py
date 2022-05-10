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
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            data=serializer.data,
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
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        sample = self.get_object(id)
        serializer = serializers.SampleSerializer(sample, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        sample = self.get_object(id)
        deleted_rows = sample.delete()

        if len(deleted_rows) <= 0:
            return Response(
                data={
                    "errors": {"global": "Nepodarilo sa vymazať vzorku"},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class BulkSamplesList(APIView):
    """
    Bulk list sample
    """

    serializer_class = serializers.SampleSerializer

    def post(self, request, format=None):
        if not isinstance(request.data, list):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        samples = Sample.objects.filter(id__in=request.data)
        serializer = self.serializer_class(samples, many=True)

        return Response(data=serializer.data)
