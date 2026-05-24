FROM python:3.11-slim

# Buat user non-root sesuai best practice HuggingFace
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements terlebih dahulu untuk caching layer
COPY --chown=user requirements.txt requirements.txt

# Install dependensi tanpa cache untuk hemat ruang
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy seluruh isi project
COPY --chown=user . /app

# HuggingFace Spaces wajib expose port 7860
EXPOSE 7860

# Jalankan Flask dengan gunicorn pada port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "120", "app:app"]
