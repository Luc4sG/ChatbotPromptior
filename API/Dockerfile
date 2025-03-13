FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY=/run/secrets/openai_api_key
ENV LANGSMITH_API_KEY=/run/secrets/langsmith_api_key

EXPOSE 5500

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 