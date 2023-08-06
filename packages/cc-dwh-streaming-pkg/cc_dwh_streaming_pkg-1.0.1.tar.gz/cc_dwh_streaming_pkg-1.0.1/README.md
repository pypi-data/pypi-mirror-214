# cc_dwh_streaming_pkg

### for updating package needs

- update `setup.py` file
- navigate to root folder - `cd cs/dwh_streaming/share`
- run `python3 setup.py sdist` to build the package locally, the output is `tar.gz` file
- run `twine upload dist/*` to upload your package and enter credentials
