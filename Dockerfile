# Base image: Python 3.11 slim variant to avoid scikit-learn compilation issues
FROM python:3.11-slim

# Create a non-root user specifically for Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user

# Set the working directory to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Copy requirements.txt first to leverage Docker layer caching
COPY --chown=user:user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user:user . .

# Expose port 7860 as required by Hugging Face Spaces
EXPOSE 7860

# Run the Flask app with Gunicorn
# Using --timeout 120 to ensure the ML model has ample time to load into memory
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "app:app"]
