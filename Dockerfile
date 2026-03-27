FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ARG MODEL_FILE=iris_model.joblib
ENV MODEL_PATH=${MODEL_FILE}

COPY main.py ${MODEL_FILE} ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
