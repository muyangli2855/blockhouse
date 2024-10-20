# Base image
FROM python:3.12

# Set the working directory
WORKDIR /blockhouse

# Copy the requirements file to the working directory
COPY requirements.txt /blockhouse/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . /blockhouse/

# Expose the port that Django will run on
EXPOSE 8000

# Set environment variables (for production use .env files)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]