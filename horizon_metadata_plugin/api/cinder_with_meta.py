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



def volume_metadata_update(request, volume_id, metadata):
    cinderclient(request).volumes.set_metadata(volume_id, metadata)

def volume_metadata_delete(request, volume_id, keys):
    cinderclient(request).volumes.delete_metadata(volume_id, keys)
