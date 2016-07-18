rm dist/*
python setup.py sdist
pip install dist/horizon_metadata_plugin-0.0.1.dev7.tar.gz --upgrade
service apache2 restart
