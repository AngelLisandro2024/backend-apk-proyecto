from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicializamos la aplicación
app = FastAPI(
    title="API Proyecto Universitario",
    description="Backend para conectar con la APK",
    version="1.0.0"
)

# Configuración de CORS para evitar bloqueos cuando la APK pida datos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ideal para desarrollo/APK)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# Endpoint de prueba para verificar que el servidor está vivo
@app.get("/")
def home():
    return {
        "estado": "Conectado con éxito",
        "mensaje": "El backend en FastAPI está funcionando correctamente"
    }

# Endpoint de ejemplo para recibir o enviar datos
@app.get("/api/v1/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}, conexión exitosa desde la APK"}