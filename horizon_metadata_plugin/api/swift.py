from datetime import datetime
import six.moves.urllib.parse as urlparse
import swiftclient

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base


FOLDER_DELIMITER = "/"
CHUNK_SIZE = getattr(settings, 'SWIFT_FILE_TRANSFER_CHUNK_SIZE', 512 * 1024)
# Swift ACL
GLOBAL_READ_ACL = ".r:*"
LIST_CONTENTS_ACL = ".rlistings"

def _metadata_to_header(metadata):
    headers = {}
    public = metadata.get('is_public')

    if public is True:
        public_container_acls = [GLOBAL_READ_ACL, LIST_CONTENTS_ACL]
        headers['x-container-read'] = ",".join(public_container_acls)
    elif public is False:
        headers['x-container-read'] = ""

    for key, value in metadata.items():
        if key.startswith("X-Container-Meta-"):
            headers[key] = value

    return headers


def swift_get_container(request, container_name, with_data=True):
    if with_data:
        headers, data = swift_api(request).get_object(container_name, "")
    else:
        data = None
        headers = swift_api(request).head_container(container_name)
    timestamp = None
    is_public = False
    public_url = None
    try:
        is_public = GLOBAL_READ_ACL in headers.get('x-container-read', '')
        if is_public:
            swift_endpoint = base.url_for(request,
                                          'object-store',
                                          endpoint_type='publicURL')
            parameters = urlparse.quote(container_name.encode('utf8'))
            public_url = swift_endpoint + '/' + parameters
        ts_float = float(headers.get('x-timestamp'))
        timestamp = datetime.utcfromtimestamp(ts_float).isoformat()
    except Exception:
        pass
    container_info = {
        'name': container_name,
        'container_object_count': headers.get('x-container-object-count'),
        'container_bytes_used': headers.get('x-container-bytes-used'),
        'timestamp': timestamp,
        'data': data,
        'is_public': is_public,
        'public_url': public_url,
    }
    metadata = {}
    for header, value in headers.items():
        if 'x-container-meta-' in header:
            key = header.partition('x-container-meta-')[2]
            metadata.update({key: value})
    container_info.update({'metadata': metadata})
    return Container(container_info)



def swift_create_container(request, name, metadata=({})):
    if swift_container_exists(request, name):
        raise exceptions.AlreadyExists(name, 'container')
    headers = _metadata_to_header(metadata)
    swift_api(request).put_container(name, headers=headers)
    return Container({'name': name})


def swift_update_container(request, name, metadata=({})):
    headers = _metadata_to_header(metadata)
    swift_api(request).post_container(name, headers=headers)
    return Container({'name': name})


