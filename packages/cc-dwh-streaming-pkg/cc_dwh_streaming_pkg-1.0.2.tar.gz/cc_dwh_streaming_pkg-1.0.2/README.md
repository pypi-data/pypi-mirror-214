# cc_dwh_streaming_pkg

### for updating package needs

- update `setup.py` file and change the version by `version='<NEW_VERSION>'`
- navigate to root folder - `cd cs/dwh_streaming/share`
- run `python3 setup.py sdist` to build the package locally, the output is `tar.gz` file
- to test locally run `pip3 install ~/PycharmProjects/wix-data-dev-secure/cs/dwh_streaming/share/dist/cc_dwh_streaming_pkg-<NEW_VERSION>.tar.gz`
- run `twine upload dist/*` to upload your package and enter credentials 
if only one version os under `dist` folder, 
if more than one versions exists use - `twine upload dist/cc_dwh_streaming_pkg-<NEW_VERSION>.tar.gz`.
