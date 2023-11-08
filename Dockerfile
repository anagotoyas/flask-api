# Usar una imagen base de Python
FROM python:3.11

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor en /app
COPY requirements.txt requirements.txt

# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Copiar el contenido de la aplicación al contenedor en /app
COPY . .

# Exponer el puerto 5000 para Flask (ajusta el puerto según tu configuración)
EXPOSE 5002

# Comando para iniciar la aplicación Flask
CMD ["python", "app.py"]
