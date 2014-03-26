#!/bin/bash
#tools_path=${tools_path:-$(dirname $0)}
#APP_PATH=$(dirname $tools_path)
#venv_path=${venv_path:-${tools_path}}
#venv_dir=${venv_name:-/../.venv}
#TOOLS=${tools_path}
#VENV=${venv:-${venv_path}/${venv_dir}}
#export PYTHONPATH=$APP_PATH
#export APP_PATH
##source ${VENV}/bin/activate && exec "$@"
#source ${VENV}/bin/activate && "$@"


TOOLS=`dirname $0`
VENV=$TOOLS/../.venv
source $VENV/bin/activate && "$@"
#source $VENV/bin/activate && "$@"
#source .venv/bin/activate && /usr/bin/which qmonitor_flush && deactivate
