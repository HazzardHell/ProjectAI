FROM python:3.12-slim

# Instalações do sistema, se necessário
RUN apt-get update && apt-get install -y \
    ffmpeg portaudio19-dev libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão
CMD ["python", "app/main.py"]
