from flask_restx import Api

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Agregar "Bearer <token>"'
    }
}

api = Api(   
   #Inicialización de la API de PatitasBog    
    title="PatitasBog - Reputación de Usuarios",
    version="1.0",
    description="Servicio de reportes y respuestas",
    authorizations=authorizations,
)
