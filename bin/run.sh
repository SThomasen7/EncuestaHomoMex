#!/bin/bash
# run.sh
# Run the survey

set -Eeuo pipefail

#export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_APP=HomoMex

flask run --host 0.0.0.0 --port 8000
