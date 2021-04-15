
PYTHON = python3
VENV_DIR = .venv

install:
	${PYTHON} -m venv .venv
	${VENV_DIR}/bin/pip install --upgrade pip
	${VENV_DIR}/bin/pip install -r requirements.txt

test:
	. ${VENV_DIR}/bin/activate && ${PYTHON} -m pytest

run:
	. ${VENV_DIR}/bin/activate && ${PYTHON} -m la_ayudante

clean:
	find ./ -type d -name '__pycache__' -exec rm -rv {} +
