#!/bin/bash
set -euo pipefail

# Start Xvfb in the background with a 1920x1080 resolution
Xvfb :99 -screen 0 1920x1080x24 &

# Wait a moment to ensure the virtual display is fully initialized
sleep 2

# Execute the Python automation script
OUTPUT_DIR="${OUTPUT_DIR:-/home/chromeuser/output}"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

HAS_CHROME_VERSION_ARG=false
for arg in "$@"; do
	case "$arg" in
		--chrome-version|--chrome-version=*)
			HAS_CHROME_VERSION_ARG=true
			break
			;;
	esac
done

if [[ "$HAS_CHROME_VERSION_ARG" = false ]] && [[ -n "${CHROME_VERSION:-}" ]]; then
	CHROME_MAJOR="${CHROME_VERSION%%.*}"
	exec python /opt/google-secret-dump/src/secret_dump.py --chrome-version "$CHROME_MAJOR" "$@"
fi

exec python /opt/google-secret-dump/src/secret_dump.py "$@"