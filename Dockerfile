# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia el archivo de requerimientos
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Establece las variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expone el puerto
EXPOSE 5000

# Comando para correr la aplicación
CMD ["flask", "run", "--port", "5000"]
