FROM python:3.8-slim

WORKDIR /be_dj

# Cài đặt PostgreSQL client và các package cần thiết trước khi cài đặt dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Cài đặt pip trước để sử dụng cache khi cài đặt dependencies
RUN pip install --upgrade pip

# Sao chép requirements.txt và cài đặt dependencies
COPY requirements.txt . 
RUN pip install -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Set môi trường không có buffer cho Python output
ENV PYTHONUNBUFFERED 1

# Mở port 8000 cho ứng dụng Django
EXPOSE 8000

# Lệnh chạy ứng dụng Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
