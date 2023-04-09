VENV=$1
echo "Cleaning ..."
set -eux
rm -rf ${VENV}
rm -rf .pytest_cache
rm -rf tests/__pycache__
rm -rf *.egg-info
rm -rf dist
rm -rf htmlcov
rm -rf .coverage report.xml
find . -type f -name '*.pyc' -delete