# Configuración de APIs Externas

## APIs de Inteligencia Artificial

### OpenAI
1. Ve a [OpenAI](https://platform.openai.com/)
2. Crea una cuenta y ve a "API Keys"
3. Genera una nueva API key
4. Configura: `OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Modelos disponibles:**
- `gpt-3.5-turbo` (recomendado para desarrollo)
- `gpt-4`
- `gpt-4-turbo-preview`

### Hugging Face
1. Ve a [Hugging Face](https://huggingface.co/)
2. Crea una cuenta y ve a "Settings" > "Access Tokens"
3. Genera un nuevo token
4. Configura: `HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Modelos populares:**
- `sentiment-analysis` (análisis de sentimientos)
- `cardiffnlp/twitter-roberta-base-sentiment-latest`
- `facebook/bart-large-mnli`

## APIs de Datos Externos

### OpenWeatherMap (Clima)
1. Ve a [OpenWeatherMap](https://openweathermap.org/api)
2. Crea una cuenta gratuita
3. Obtén tu API key
4. Configura: `WEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Plan gratuito:** 1,000 llamadas/día

### NewsAPI (Noticias)
1. Ve a [NewsAPI](https://newsapi.org/)
2. Registrate para obtener una API key gratuita
3. Configura: `NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Plan gratuito:** 1,000 requests/día

### Google Maps (Geolocalización)
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Habilita "Geocoding API"
3. Crea credenciales (API Key)
4. Configura: `MAPS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Ejemplo de Configuración Completa

```bash
# .env
GOOGLE_SHEET_ID=1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T
GOOGLE_CREDENTIALS_FILE=credentials.json

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

WEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MAPS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

CACHE_DIR=./cache
CACHE_DURATION=300
```

## Endpoints Disponibles

### IA
- `POST /api/v1/ai/generate-text` - Generar texto con OpenAI
- `POST /api/v1/ai/sentiment-analysis` - Análisis de sentimientos
- `GET /api/v1/ai/models` - Listar modelos disponibles

### APIs Externas
- `POST /api/v1/weather` - Datos del clima
- `POST /api/v1/news` - Obtener noticias
- `POST /api/v1/location` - Geolocalización
- `POST /api/v1/custom-api` - API personalizada

### Caché
- `GET /api/v1/cache/stats` - Estadísticas del caché
- `DELETE /api/v1/cache/clear` - Limpiar caché
- `GET /api/v1/cache/{key}` - Obtener valor
- `POST /api/v1/cache/{key}` - Guardar valor
