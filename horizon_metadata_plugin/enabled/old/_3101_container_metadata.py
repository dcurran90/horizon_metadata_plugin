# The name of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'containers'

# The name of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'project'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'horizon_metadata_plugin.content.containers.panel.Containers'

# A list of AngularJS modules to be loaded when Angular bootstraps.
#ADD_ANGULAR_MODULES = ['horizon.dashboard.identity.myplugin.mypanel']
ADD_ANGULAR_MODULES = ['horizon.dashboard.project.horizon_metadata_plugin.containers']

# Automatically discover static resources in installed apps
AUTO_DISCOVER_STATIC_FILES = True

