# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""sample API over neutron 
"""

from django.views import generic

from openstack_dashboard.api import neutron
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils


from openstack_dashboard import api
from openstack_dashboard.api import cinder as metadata_cinder


CLIENT_KEYWORDS = {'marker', 'sort_dir', 'paginate'}


@urls.register
class SampleNetwork(generic.View):
    """ sample interface for networks
    """
    url_regex = r'sample-network/networks/$'

    @rest_utils.ajax()
    def get(self, request):
        """List networks for current project.
        The listing result is an object with property "items".
        """
        networks = neutron.network_list(request)
        return {'items': networks}



@urls.register
class VolumeMetadata(generic.View):
    """API for volume metadata.
    """
    url_regex = r'cinder/volumes/(?P<volume_id>[^/]+|default)/metadata$'

    @rest_utils.ajax()
    def get(self, request, volume_id):
        """Get a specific volume's metadata
        http://localhost/api/cinder/volumes/1/metadata
        """
        return api.cinder.volume_get(request,
                                   volume_id).to_dict().get('metadata')

'''
    @rest_utils.ajax()
    def patch(self, request, volume_id):
        """Update metadata items for a server
        http://localhost/api/cinder/volumes/1/metadata
        """
        updated = request.DATA['updated']
        removed = request.DATA['removed']
        if updated:
            metadata_cinder.volume_metadata_update(request, volume_id, updated)
        if removed:
            metadata_cinder.volume_metadata_delete(request, volume_id, removed)



'''
