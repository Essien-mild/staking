# Dockerfile
FROM python:3.12-slim

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files into /app/staticfiles
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "Staking.wsgi:application", "--bind", "0.0.0.0:8000"]
