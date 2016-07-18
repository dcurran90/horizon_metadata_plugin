
from __future__ import absolute_import

import logging

from django.conf import settings
from django.utils.functional import cached_property  # noqa
from django.utils.translation import ugettext_lazy as _
import six

from novaclient import client as nova_client
from novaclient import exceptions as nova_exceptions
from novaclient.v2.contrib import instance_action as nova_instance_action
from novaclient.v2.contrib import list_extensions as nova_list_extensions
from novaclient.v2 import security_group_rules as nova_rules
from novaclient.v2 import security_groups as nova_security_groups
from novaclient.v2 import servers as nova_servers

from horizon import conf
from horizon import exceptions as horizon_exceptions
from horizon.utils import functions as utils
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base
from openstack_dashboard.api import network_base


LOG = logging.getLogger(__name__)

# Supported compute versions
VERSIONS = base.APIVersionManager("compute", preferred_version=2)
VERSIONS.load_supported_version(1.1, {"client": nova_client, "version": 1.1})
VERSIONS.load_supported_version(2, {"client": nova_client, "version": 2})

# API static values
INSTANCE_ACTIVE_STATE = 'ACTIVE'
VOLUME_STATE_AVAILABLE = "available"
DEFAULT_QUOTA_NAME = 'default'


@memoized
def novaclient(request):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    c = nova_client.Client(VERSIONS.get_active_version()['version'],
                           request.user.username,
                           request.user.token.id,
                           project_id=request.user.tenant_id,
                           auth_url=base.url_for(request, 'compute'),
                           insecure=insecure,
                           cacert=cacert,
                           http_log_debug=settings.DEBUG)
    c.client.auth_token = request.user.token.id
    c.client.management_url = base.url_for(request, 'compute')
    return c


def snapshot_create(request, instance_id, name, metadata):
    return novaclient(request).servers.create_image(instance_id, name, metadata)

