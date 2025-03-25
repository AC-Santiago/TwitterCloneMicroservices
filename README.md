# Twitter Clone Microservices

Este proyecto es una implementación de un clon de Twitter utilizando una arquitectura de microservicios en Python. El proyecto utiliza uv como gestor de paquetes para un manejo más eficiente de las dependencias.

## 📂 Estructura del Proyecto
Este proyecto es una implementación de un clon de Twitter utilizando una arquitectura de microservicios en Python. El proyecto utiliza uv como gestor de paquetes para un manejo más eficiente de las dependencias.

```
TwitterCloneMicroservices/
├── auth_service/           # Servicio de autenticación
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── tweet_service/          # Servicio de tweets
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── interaction_service/    # Servicio de interacciones
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── bff_service/           # Backend for Frontend
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── database/              # Scripts de base de datos
│   └── init/
│       └── 01_init_tables.sql
├── docker-compose.yml     # Configuración de Docker Compose
├── pyproject.toml        # Dependencias del proyecto principal
└── uv.lock              # Lock file de dependencias
```

## 🚀 Microservicios

El proyecto está dividido en los siguientes microservicios:

1. **Auth Service**: Maneja la autenticación y autorización de usuarios.
2. **Tweet Service**: Gestiona la creación, lectura y eliminación de tweets.
3. **Interaction Service**: Maneja las interacciones como likes, retweets y comentarios.
4. **BFF Service**: Backend for Frontend que actúa como una capa de agregación para el cliente.

## 📦 Gestión de Dependencias con uv

Este proyecto utiliza [uv](https://github.com/astral-sh/uv) como gestor de paquetes, que es una alternativa más rápida a pip. Cada microservicio tiene su propio `pyproject.toml` y `uv.lock` para manejar sus dependencias de manera aislada.

### Ventajas de usar uv:
- Instalación de paquetes más rápida
- Resolución de dependencias determinista
- Mejor manejo de entornos virtuales

### Instalación de dependencias:

```bash
# Instalar uv
pip install uv

# Instalar dependencias de un servicio
cd [nombre_servicio]
uv sync
```

## 🐳 Docker

Cada microservicio está containerizado usando Docker y orquestado con Docker Compose. Para ejecutar el proyecto:

```bash
docker-compose up --build
```

## 🗄️ Base de Datos

La estructura de la base de datos se inicializa mediante los scripts ubicados en `database/init/`. El archivo `01_init_tables.sql` contiene la definición de las tablas necesarias para el funcionamiento del sistema.

## 🛠️ Desarrollo

Para comenzar a desarrollar:

1. Clona el repositorio
2. Instala uv: En su documentacion se explicampo como se instala [uv-docs](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
3. Para cada servicio:
   - Navega al directorio del servicio
   - Crea un entorno virtual: `uv venv .venv --python 3.11`
   - Activa el entorno virtual: `source .venv/bin/activate`
   - Instala las dependencias: `uv sync`

## 🔄 Flujo de Trabajo

1. Las peticiones del cliente son recibidas por el BFF Service
2. El BFF coordina con los diferentes microservicios según sea necesario
3. Cada microservicio maneja su propia lógica de negocio y datos
4. La autenticación es manejada por el Auth Service



