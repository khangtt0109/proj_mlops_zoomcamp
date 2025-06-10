FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

RUN pip install pandas pyarrow scikit-learn==1.6.1

COPY predict.py .

ENTRYPOINT ["python", "predict.py"]