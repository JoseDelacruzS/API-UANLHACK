# Configuración de Google Sheets

## 1. Crear un Proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google Sheets:
   - Ve a "APIs & Services" > "Library"
   - Busca "Google Sheets API"
   - Haz clic en "Enable"

## 2. Crear Credenciales de Servicio

1. Ve a "APIs & Services" > "Credentials"
2. Haz clic en "Create Credentials" > "Service Account"
3. Llena los detalles y crea la cuenta
4. En la cuenta de servicio creada, ve a "Keys" > "Add Key" > "JSON"
5. Descarga el archivo JSON de credenciales

## 3. Compartir la Hoja de Cálculo

1. Abre tu Google Sheet
2. Copia el ID de la hoja desde la URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   ```
3. Comparte la hoja con el email de la cuenta de servicio (encontrarás el email en el archivo JSON)
4. Dale permisos de "Editor"

## 4. Configurar Variables de Entorno

```bash
# Opción 1: Usar archivo de credenciales
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=tu_sheet_id_aqui

# Opción 2: Usar JSON directamente (para Docker/producción)
GOOGLE_CREDENTIALS_JSON='{"type": "service_account", "project_id": "tu-proyecto", ...}'
GOOGLE_SHEET_ID=tu_sheet_id_aqui
```

## 5. Estructura de la Hoja

Asegúrate de que tu hoja tenga headers en la primera fila:

| ID | Nombre | Email | Fecha | Estado |
|----|--------|-------|-------|--------|
| 1  | Juan   | juan@email.com | 2024-01-01 | Activo |

## Endpoints Disponibles

- `POST /api/v1/sheets/data` - Obtener datos
- `POST /api/v1/sheets/add` - Agregar fila
- `PUT /api/v1/sheets/update` - Actualizar fila
- `POST /api/v1/sheets/search` - Buscar registros
- `GET /api/v1/sheets/columns/{sheet_name}` - Obtener columnas
- `POST /api/v1/sheets/refresh/{sheet_name}` - Refrescar caché
