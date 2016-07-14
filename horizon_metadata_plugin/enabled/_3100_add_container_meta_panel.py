# The name of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'containers_with_meta'

PANEL_DASHBOARD = 'project'
# The name of the dashboard the PANEL associated with. Required.
PANEL_GROUP = 'object_store'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'horizon_metadata_plugin.content.containers.panel.Containers'

# A list of applications to be prepended to INSTALLED_APPS
ADD_INSTALLED_APPS = ['horizon_metadata_plugin']

# A list of AngularJS modules to be loaded when Angular bootstraps.
#ADD_ANGULAR_MODULES = ['horizon.dashboard.identity.myplugin.mypanel']
#ADD_ANGULAR_MODULES = ['horizon.dashboard.project.containers_with_meta']

# Automatically discover static resources in installed apps
AUTO_DISCOVER_STATIC_FILES = True
