echo "Coverage ..."
set -eux
  coverage run --parallel-mode --module pytest --junitxml report.xml
  coverage combine
  coverage html
  coverage report --show-missing --fail-under 1