import os

from django import forms
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import six

from horizon import exceptions
from horizon_metadata_plugin import api
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from openstack_dashboard.api import swift

@urls.register
class Container_Metadata(generic.View):
    """API for swift container level information
    """

    url_regex = r'swift/containers/(?P<container>[^/]+)/update_metadata/$'


    @rest_utils.ajax()
    def get(self, request, container):
        """Get the container details
        """
        return api.swift_with_meta.swift_get_container(request, container).to_dict()

    @rest_utils.ajax(data_required=True)
    def put(self, request, container):
        metadata = {}
        for key, value in request.DATA.items():
            if key.startswith("X-Container-Meta-") or key == 'is_public':
                metadata[key] = value
        api.swift_with_meta.swift_update_container(request, container, metadata=metadata)

