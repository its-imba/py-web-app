FROM python:3.8-alpine
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app
EXPOSE 5000
ENTRYPOINT ["python", "main.py"]
