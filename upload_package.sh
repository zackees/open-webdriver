#!/bin/bash
set -e
set -x
rm -rf build dist
uv pip install wheel twine
uv build --wheel
uv run twine upload dist/* --verbose
# echo Pushing git tags…

