echo "Formating ..."
set -eux
black project_cli
autoflake --in-place --remove-all-unused-imports project_cli/*.py tests/*.py