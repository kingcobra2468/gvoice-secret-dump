# Google Secrets Dump

Selenium-based secret and cookie dumper for Google Voice and YouTube Music.

## Requirements

1. Python 3.10+
2. A Google account that can sign in without 2FA challenge during automation
3. Environment variables:
    1. `GVOICE_EMAIL`
    2. `GVOICE_PASSWORD`

## CLI Usage

Run from the project root:

```bash
python src/secret_dump.py [--chrome-version <major>] <service> <command>
```

Values:

1. `service`: `gvoice` or `ytmusic`
2. `command`: `login` or `refresh`

Examples:

```bash
python src/secret_dump.py gvoice login
python src/secret_dump.py ytmusic refresh
python src/secret_dump.py --chrome-version 151 ytmusic login
```

Output files are written to the current working directory:

1. `<service>_secrets.json`
2. `<service>_cookies.txt`

For `refresh`, run in a directory that already contains `<service>_secrets.json`.

## Local Development Setup

With `uv`:

```bash
uv sync
export GVOICE_EMAIL="you@example.com"
export GVOICE_PASSWORD="your-password"
python src/secret_dump.py gvoice login
```

With `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
export GVOICE_EMAIL="you@example.com"
export GVOICE_PASSWORD="your-password"
python src/secret_dump.py gvoice login
```

## Docker Usage

Build:

```bash
docker build -t gvoice-secret-dump:local .
```

Run login and persist outputs to host:

```bash
mkdir -p output
docker run --rm \
   --shm-size=2g \
   -e GVOICE_EMAIL="you@example.com" \
   -e GVOICE_PASSWORD="your-password" \
   -v "$PWD/output:/home/chromeuser/output" \
   gvoice-secret-dump:local \
   ytmusic login
```

Run with explicit Chrome major version:

```bash
docker run --rm \
   --shm-size=2g \
   -e GVOICE_EMAIL="you@example.com" \
   -e GVOICE_PASSWORD="your-password" \
   -v "$PWD/output:/home/chromeuser/output" \
   gvoice-secret-dump:local \
   --chrome-version=151 ytmusic login
```

Run refresh:

```bash
docker run --rm \
   --shm-size=2g \
   -e GVOICE_EMAIL="you@example.com" \
   -e GVOICE_PASSWORD="your-password" \
   -v "$PWD/output:/home/chromeuser/output" \
   gvoice-secret-dump:local \
   ytmusic refresh
```

Interactive shell workflow:

```bash
docker run --rm -it \
   --shm-size=2g \
   -e GVOICE_EMAIL="you@example.com" \
   -e GVOICE_PASSWORD="your-password" \
   -v "$PWD/output:/home/chromeuser/output" \
   --entrypoint bash \
   gvoice-secret-dump:local
```

Then run commands inside the container:

```bash
/usr/local/bin/entrypoint.sh ytmusic login
/usr/local/bin/entrypoint.sh ytmusic refresh
/usr/local/bin/entrypoint.sh gvoice login
```

Important:

1. Mount `/home/chromeuser/output` only.
2. Do not mount over application paths.
3. Use `--shm-size=2g` to reduce Chrome tab crashes.

## Troubleshooting

### `WebDriverException: tab crashed`

1. Use `--shm-size=2g` with Docker.
2. Pass `--chrome-version <major>` if driver/browser mismatch is suspected.
3. Rebuild image after Dockerfile changes: `docker build --no-cache -t gvoice-secret-dump:local .`

### `PermissionError` writing output files

This is typically a host bind-mount permissions issue on `./output`.

```bash
mkdir -p output
chmod 777 output
```

Or create output with your own user and avoid root-owned files from earlier runs.
