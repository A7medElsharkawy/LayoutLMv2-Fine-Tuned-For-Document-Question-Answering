# # Use the official Python base image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy application files into the container
# COPY app.py app.py
# COPY requirements.txt requirements.txt

# # Install necessary dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     tesseract-ocr \                  
#     git \                             
#     && apt-get clean && rm -rf /var/lib/apt/lists/* \  
#     && python -m pip install --upgrade pip \            
#     && pip install --no-cache-dir -r requirements.txt \  
#     && pip install --no-cache-dir 'git+https://github.com/facebookresearch/detectron2.git'  

# # Expose the port Streamlit will run on
# EXPOSE 8501

# # Command to run the application (assuming you're using Streamlit)
# CMD ["streamlit", "run", "app.py"]


# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files into the container
COPY app.py app.py
COPY requirements.txt requirements.txt

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    git \
    gcc \
    python3-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir 'git+https://github.com/facebookresearch/detectron2.git'

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the application (assuming you're using Streamlit)
CMD ["streamlit", "run", "app.py"]
