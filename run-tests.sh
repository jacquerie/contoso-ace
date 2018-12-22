set -e

flake8 app tests
py.test tests
