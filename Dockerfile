FROM python:3.12.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN python -m pip install --no-cache-dir streamlit openai moviepy==2.1.2 edge-tts pillow requests python-dotenv numpy

RUN python -c "import openai; print('OPENAI INSTALLED')"

COPY . .

EXPOSE 8501

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
