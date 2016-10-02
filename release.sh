pip install wheel
pip install mock
pip install coverage
pip install sphinx
ant release
git tag v`jenkinsapi_version`
ant doc
git push --tags
