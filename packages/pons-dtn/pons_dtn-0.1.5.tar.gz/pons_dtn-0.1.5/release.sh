#!/bin/sh

python3 -m build
twine upload dist/pons_dtn-0.1.5*
