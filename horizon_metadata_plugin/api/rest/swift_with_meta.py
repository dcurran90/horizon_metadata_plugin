import os

from django import forms
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import six

from horizon import exceptions
from openstack_dashboard import api
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from openstack_dashboard.api import swift

@urls.register
class Container(generic.View):
    """API for swift container level information
    """

    url_regex = r'swift/containers/(?P<container>[^/]+)/metadata/$'

    @rest_utils.ajax()
    def get(self, request, container):
        """Get the container details
        """
        return api.swift.swift_get_container(request, container).to_dict()

    @rest_utils.ajax()
    def post(self, request, container):
        metadata = {}

        if 'is_public' in request.DATA:
            metadata['is_public'] = request.DATA['is_public']

        # This will raise an exception if the container already exists
        try:
            api.swift.swift_create_container(request, container,
                                             metadata=metadata)
        except exceptions.AlreadyExists as e:
            # 409 Conflict
            return rest_utils.JSONResponse(str(e), 409)

        return rest_utils.CreatedResponse(
            u'/api/swift/containers/%s' % container,
        )

    @rest_utils.ajax()
    def delete(self, request, container):
        api.swift.swift_delete_container(request, container)

    @rest_utils.ajax(data_required=True)
    def put(self, request, container):
        metadata = {}
        for key, value in request.DATA.items():
            if key.startswith("X-Container-Meta-") or key == 'is_public':
                metadata[key] = value
        api.swift.swift_update_container(request, container, metadata=metadata)

