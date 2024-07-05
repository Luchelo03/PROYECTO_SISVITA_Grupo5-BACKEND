# Usa una imagen base oficial de Python
FROM python:3.12.3

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos requeridos para la aplicación
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Expon el puerto en el que la aplicación correrá
EXPOSE 5000

# Comando para correr la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
