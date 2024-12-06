# FROM python:3.12-slim
FROM cnstark/pytorch:2.0.1-py3.10.11-ubuntu22.04
WORKDIR /app

COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY artefacts artefacts
COPY backend/app.py .
COPY backend/utils.py .
COPY frontend frontend

RUN --mount=source=dist,target=/dist PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir /dist/*.whl

EXPOSE 80

CMD ["python", "app.py"]
