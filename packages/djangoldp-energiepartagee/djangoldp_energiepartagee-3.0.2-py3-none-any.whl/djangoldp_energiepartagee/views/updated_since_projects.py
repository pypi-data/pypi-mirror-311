from djangoldp.views import LDPViewSet

from djangoldp_energiepartagee.filters import UpdatedSinceFilterBackend
from djangoldp_energiepartagee.models import CitizenProject


class UpdatedSinceProjectsViewset(LDPViewSet):
    model = CitizenProject
    queryset = CitizenProject.objects.none()
    filter_backends = [UpdatedSinceFilterBackend]
