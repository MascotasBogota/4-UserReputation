# 4-UserReputation

## Descripción

Este módulo es un servicio para gestionar la reputación de los usuarios basado
en las respuestas a reportes. Permite calificar respuestas como útiles o no
útiles, y aplica cambios en la reputación del autor de la respuesta.

## Funcionalidades principales

- Calificar respuestas a reportes como útiles o no útiles.
- Actualizar la reputación del autor de la respuesta.
- Validar permisos del usuario para calificar respuestas.

## Endpoints

### `POST /api/rate-response/<report_id>/<response_id>`

Este endpoint permite calificar una respuesta a un reporte.

#### Parámetros

- **Path Parameters:**
  - `report_id` (string): Identificador único del reporte.
  - `response_id` (string): Identificador único de la respuesta a calificar.
- **Body:**
  ```json
  {
    "rating": "useful"
  }
  ```
  - `rating` (string):
    - Para respuestas de tipo "avistamiento":
      - `useful`: Marca la respuesta como útil.
      - `not_useful`: Quita la marca de útil (solo si previamente fue marcada
        como útil).
    - Para respuestas de tipo "hallazgo":
      - `useful`: Marca la respuesta como útil.
      - `false_finding`: Marca la respuesta como hallazgo falso.

#### Respuestas

- **200 OK:**
  ```json
  {
    "status": "success",
    "new_reputation": 10
  }
  ```
- **400 Bad Request:** Parámetros inválidos o faltantes.
- **401 Unauthorized:** El usuario no está autenticado.
- **403 Forbidden:** El usuario no tiene permisos para calificar esta respuesta.
- **503 Service Unavailable:** Error al conectar con servicios dependientes.

## Documentación Swagger

El módulo incluye documentación Swagger accesible en:

```
http://<host>:5100/apidocs/
```

### Ejemplo de especificación Swagger para el endpoint `/rate-response`

```yaml
paths:
  /api/rate-response/{report_id}/{response_id}:
    post:
      tags:
        - Reputation
      summary: Calificar una respuesta a un reporte
      description:
        Permite al propietario de un reporte calificar una respuesta como útil o
        un hallazgo como falso.
      security:
        - Bearer: []
      parameters:
        - name: report_id
          in: path
          required: true
          description: Identificador único del reporte
          schema:
            type: string
        - name: response_id
          in: path
          required: true
          description: Identificador único de la respuesta
          schema:
            type: string
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
              rating:
                type: string
                enum: [useful, not_useful, false_finding]
                description: Calificación a aplicar
      responses:
        200:
          description: Calificación aplicada exitosamente
        400:
          description: Parámetros inválidos o faltantes
        401:
          description: Autenticación requerida
        403:
          description: Usuario no autorizado
        503:
          description: Servicio no disponible
```

## Ejecución

Para ejecutar el servicio, utiliza el siguiente comando:

```bash
python app.py
```

El servicio estará disponible en `http://localhost:5100`.

## Dependencias

Asegúrate de instalar las dependencias listadas en `requirements.txt` antes de
ejecutar el servicio:

```bash
pip install -r requirements.txt
```
