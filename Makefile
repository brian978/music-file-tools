SCRIPT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

install:
	python3 -m venv .venv
	source "${SCRIPT_DIR}/.venv/bin/activate"
	pip3 install -r "${SCRIPT_DIR}/requirements.txt"

upgrade:
	source "${SCRIPT_DIR}/.venv/bin/activate"
	pip3 install --upgrade pip

normalize:
	echo "Running normalize.py"
	source "${SCRIPT_DIR}/.venv/bin/activate"
	python3 "${SCRIPT_DIR}/normalize.py"