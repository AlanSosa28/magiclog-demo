# Usar una imagen base de Python oficial, versión slim para reducir el tamaño de la imagen
FROM python:3.9-slim

# Instalar dependencias del sistema necesarias y luego limpiar la cache del gestor de paquetes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear un usuario no root para ejecutar la aplicación
RUN useradd -m alan
USER alan

# Definir el directorio de trabajo en el contenedor
WORKDIR /home/alan/app

# Copiar los archivos requirements.txt y app.py al directorio de trabajo del contenedor
# Asegúrate de que el contexto de construcción de Docker sea el directorio padre de la carpeta 'docker'
COPY --chown=alan:alan ../requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt
COPY --chown=alan:alan ../app.py ./

# Exponer el puerto que Flask utiliza por defecto
EXPOSE 5000

# Definir las variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Ejecutar la aplicación Flask utilizando el comando flask
CMD ["python", "-m", "flask", "run"]
