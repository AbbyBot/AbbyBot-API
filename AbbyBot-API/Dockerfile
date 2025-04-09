FROM python:3.13.2-slim
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python scripts/migrate_tables.py
EXPOSE 5002
CMD ["gunicorn", "-b", "0.0.0.0:5002", "main:app"]
