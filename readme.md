## CrisostomoCore
![default.png](media/img/author/default.png)
Biblioteca digital en Python basada en Clean Architecture. Proyecto modular pensado para usarse como librería o servicio HTTP, con capas separadas: Domain, Application, Infrastructure y Presentation. Incluye gestión de autores, categorías y usuarios, autenticación y acceso asíncrono a PostgreSQL.

Descripción
CrisostomoCore es una biblioteca digital diseñada con principios de Clean Architecture para facilitar la construcción de aplicaciones de gestión bibliográfica y servicios relacionados. Su objetivo es ofrecer una base sólida, modular y fácil de mantener que se pueda reutilizar como librería o desplegar como servicio HTTP. La arquitectura separa claramente la lógica de negocio (Use Cases y Domain) de las dependencias de infraestructura (DAO, proveedores) y de la capa de presentación (rutas, DTOs, middleware).

Puntos clave de la descripción:

Propósito: proporcionar una base reutilizable y bien estructurada para desarrollar una biblioteca digital con buenas prácticas arquitectónicas.

Diseño: capas independientes (Domain, Application, Infrastructure, Presentation) para facilitar pruebas, mantenimiento y evolución.

Funcionalidad: gestión de autores, categorías y usuarios; autenticación; acceso a PostgreSQL mediante pool asíncrono; logging centralizado.

Uso: puede emplearse como librería en otros proyectos o desplegarse como servicio (por ejemplo con FastAPI + Uvicorn).

Estructura del repositorio
Código
.
├── .env
├── .env-example
├── .gitignore
├── Application
│   ├── Helpers
│   └── UseCases
├── Config
│   └── Settings.py
├── Domain
│   ├── Entities
│   ├── IDAO
│   └── kernel
├── Infrastructure
│   ├── DAO
│   └── Providers
├── Presentation
│   ├── DTOS
│   ├── MIddleWare
│   ├── Routes
│   └── Services
├── main.py
├── media
└── requirements
Quickstart
1. Crear y activar entorno virtual

bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
2. Instalar dependencias

bash
pip install -r requirements
3. Configurar variables de entorno

bash
cp .env-example .env
# editar .env con DATABASE_URL, JWT_SECRET, APP_NAME, LOG_LEVEL, etc.
4. Inicializar base de datos Aplica migraciones o ejecuta los scripts SQL que uses en tu flujo de trabajo.

5. Ejecutar la aplicación

bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
6. Documentación Accede a la documentación automática en /docs o /redoc según la configuración.

Características principales
Clean Architecture: separación clara entre dominio, casos de uso, infraestructura y presentación.

Use Cases: lógica de negocio organizada en Application/UseCases.

Entidades y contratos: Domain/Entities y Domain/IDAO definen modelos y contratos para facilitar pruebas y mocks.

Implementaciones de persistencia: Infrastructure/DAO contiene adaptadores concretos para PostgreSQL.

Providers: Infrastructure/Providers incluye AppLogger, JwtProvider y PostgreSQLPoolMaster.

Presentation: rutas, DTOs y middleware en Presentation para exponer la API y validar/transformar datos.

Recursos estáticos: media/ para imágenes y recursos por defecto.

Buenas prácticas y recomendaciones
Mantén la lógica de negocio en Application y Domain; evita dependencias de infraestructura en esas capas.

Mockea las interfaces de Domain/IDAO en pruebas unitarias.

Usa PostgreSQLPoolMaster para gestionar conexiones asíncronas y evitar fugas.

Centraliza logs con AppLogger y registra eventos relevantes para trazabilidad.

Protege secretos: no subas .env al repositorio; usa .env-example para documentar variables.

Aplica formateo y linters: black, isort, flake8.

Añade tests con pytest y cubre los Use Cases con mocks de DAO.

Comandos útiles
bash
# formatear código
black .

# ordenar imports
isort .

# linter
flake8

# ejecutar tests
pytest
Contribuir
Abre issues para bugs o mejoras.

Envía PRs pequeñas y con pruebas.

Actualiza .env-example si agregas nuevas variables de configuración.

Añade documentación y ejemplos de uso para nuevas funcionalidades.