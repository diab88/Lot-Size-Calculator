FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install flask

EXPOSE 5050

CMD ["python", "hedging_strategy_app.py"]
