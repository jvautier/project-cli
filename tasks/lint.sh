echo "Linting ..."
set -eux
flake8 project_cli tests
black --check project_cli tests