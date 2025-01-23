FROM python:3.10

WORKDIR /app

COPY requirements_prd.txt ./
RUN pip install -r requirements_prd.txt

# COPY example.py ./
COPY ETL_process.py ./
COPY config.py ./

CMD ["python", "ETL_process.py"]