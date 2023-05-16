FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir audio

COPY . .
ENV username=your_username
ENV password=your_password

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]