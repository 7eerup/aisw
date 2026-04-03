FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY main.py .

ENV PORT=8000
ENV MODE=development

EXPOSE ${PORT}

# Python 코드에서 처리하도록 변경
CMD ["python", "main.py"]