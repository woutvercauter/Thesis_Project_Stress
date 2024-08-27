# Gebruik een lichtgewicht Python basisimage
FROM python:3.11-slim

# Stel de werkdirectory in
WORKDIR /app

# Kopieer de requirements.txt naar de werkdirectory
COPY requirements.txt .

# Installeer de afhankelijkheden
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer alle Python scripts en andere benodigde bestanden naar de container
COPY . .

# Voer het hoofdscript uit
CMD ["python", "main.py"]