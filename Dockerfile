# Dockerfile
FROM python:3.11-slim

# 1. Cria diretório de trabalho
WORKDIR /app

# 2. Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia todo o código da aplicação
COPY . .

# 4. Expõe a porta que o Streamlit usa por padrão
EXPOSE 8501

# 5. Define o comando de entrada, apontando para o seu home.py
ENTRYPOINT ["streamlit", "run", "src/home.py", "--server.port=8501", "--server.address=0.0.0.0"]
