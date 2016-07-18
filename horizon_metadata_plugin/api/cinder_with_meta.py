from __future__ import absolute_import

import logging

from django.conf import settings
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from cinderclient import exceptions as cinder_exception
from cinderclient.v2.contrib import list_extensions as cinder_list_extensions

from horizon import exceptions
from horizon.utils import functions as utils
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base
from openstack_dashboard.api import nova

LOG = logging.getLogger(__name__)


# API static values
VOLUME_STATE_AVAILABLE = "available"
DEFAULT_QUOTA_NAME = 'default'

# Available consumer choices associated with QOS Specs
CONSUMER_CHOICES = (
    ('back-end', _('back-end')),
    ('front-end', _('front-end')),
    ('both', pgettext_lazy('Both of front-end and back-end', u'both')),
)

VERSIONS = base.APIVersionManager("volume", preferred_version=2)

try:
    from cinderclient.v2 import client as cinder_client_v2
    VERSIONS.load_supported_version(2, {"client": cinder_client_v2,
                                        "version": 2})
except ImportError:
    pass


@memoized
def cinderclient(request):
    api_version = VERSIONS.get_active_version()

    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    cinder_url = ""
    try:
        # The cinder client assumes that the v2 endpoint type will be
        # 'volumev2'.
        if api_version['version'] == 2:
            try:
                cinder_url = base.url_for(request, 'volumev2')
            except exceptions.ServiceCatalogException:
                LOG.warning("Cinder v2 requested but no 'volumev2' service "
                            "type available in Keystone catalog.")
    except exceptions.ServiceCatalogException:
        LOG.debug('no volume service configured.')
        raise
    c = api_version['client'].Client(request.user.username,
                                     request.user.token.id,
                                     project_id=request.user.tenant_id,
                                     auth_url=cinder_url,
                                     insecure=insecure,
                                     cacert=cacert,
                                     http_log_debug=settings.DEBUG)
    c.client.auth_token = request.user.token.id
    c.client.management_url = cinder_url
    return c


def volume_metadata_update(request, volume_id, metadata):
    cinderclient(request).volumes.set_metadata(volume_id, metadata)

def volume_metadata_delete(request, volume_id, keys):
    cinderclient(request).volumes.delete_metadata(volume_id, keys)
