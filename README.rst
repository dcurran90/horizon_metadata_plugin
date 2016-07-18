cp horizon_metadata_plugin/templates/horizon_metadata_plugin/_metadata.html /opt/stack/horizon/horizon/templates/horizon/common/_metadata.html
cp horizon_metadata_plugin/templates/horizon_metadata_plugin/_modal_form_metadata.html /opt/stack/horizon/horizon/templates/horizon/common/_modal_form_metadata.html

rm horizon/openstack_dashboard/enabled/_1040_project_volumes_panel.py
rm horizon/openstack_dashboard/enabled/_1050_project_images_panel.py

cp -rv horizon_metadata_plugin/horizon_metadata_plugin/enabled/ horizon/openstack_dashboard/local/


