from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Uuid, String
from spyne.service import Service
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel

from samples import models

NS = "aass_samples"


class Sample(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = models.Sample


class SampleService(Service):
    def get_object(self, id):
        try:
            return Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            raise ResourceNotFoundError("Sample")

    @rpc(_returns=Sample)
    def list(self):
        """
        List all samples
        """
        return Sample.objects.all()

    @rpc(Uuid, _returns=Sample)
    def get(self, id):
        """
        Retrieve sample instance
        """
        return self.get_object(id)

    @rpc(Sample, _returns=None)
    def create(self, sample):
        """
        Create new sample
        """
        try:
            Sample.objects.create(**sample.as_dict())
        except IntegrityError:
            raise ResourceAlreadyExistsError("Container")
        return
        # return Response(message="Vzorka vytvorená")

    @rpc(Uuid, Sample, _returns=None)
    def update(self, id, sample):
        """
        Update existing sample
        """
        self.get_object(id).update(sample)
        return
        # return Response(message="Vzorka uložená")

    @rpc(Uuid, _returns=None)
    def delete(self, id):
        """
        Delete sample
        """
        sample = self.get_object(id)
        sample.delete()
        return
        # return Response(message="Vzorka vymazaná")


SampleApp = Application(
    services=[SampleService],
    tns=NS,
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

sample_service = csrf_exempt(DjangoApplication(SampleApp))
