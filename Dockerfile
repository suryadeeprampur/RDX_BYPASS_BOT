FROM python:3.10-slim-buster

WORKDIR /app

# Fix Buster repo URLs and install git
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
    && echo 'Acquire::Check-Valid-Until "0";' > /etc/apt/apt.conf.d/99no-check-valid-until \
    && apt-get -qq update --fix-missing \
    && apt-get -qq upgrade -y \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt flask gunicorn

# Copy application code
COPY . .

# Expose Render PORT
EXPOSE 5000

# Start using Gunicorn (runs Flask) and your bot in one process
CMD ["python3", "main.py"]
