
function _do() {
    
pip-compile \
    --verbose \
    --rebuild \
    --upgrade \
    --no-annotate \
    --no-emit-trusted-host \
    --no-emit-index-url \
    --no-header \
    --output-file $2 \
    $1
}

_do requirements.in requirements.txt
_do dev/requirements.in dev/requirements.txt
_do tests/requirements.in tests/requirements.txt