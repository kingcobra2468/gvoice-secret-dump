FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the exact Chrome version you want to hardcode
# You can find valid versions at: https://googlechromelabs.github.io/chrome-for-testing/
ENV CHROME_VERSION="151.0.7922.77"

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    libxss1 \
    libnss3 \
    libnspr4 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" \
    && unzip chrome-linux64.zip -d /opt/ \
    && rm chrome-linux64.zip \
    && ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Xvfb needs this root-owned sticky directory to create the display socket.
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

RUN useradd -m chromeuser
USER chromeuser
WORKDIR /opt/google-secret-dump

COPY --chown=chromeuser:chromeuser pyproject.toml uv.lock setup.cfg README.md ./
COPY --chown=chromeuser:chromeuser src ./src

RUN uv sync --frozen --no-dev

ENV VIRTUAL_ENV="/opt/google-secret-dump/.venv"
ENV PATH="/opt/google-secret-dump/.venv/bin:${PATH}"

ENV PATH="/home/chromeuser/.local/bin:${PATH}"

RUN mkdir -p /home/chromeuser/output
ENV OUTPUT_DIR="/home/chromeuser/output"

ENV DISPLAY=:99

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]