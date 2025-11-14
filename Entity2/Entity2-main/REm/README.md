# REMForge Ultra - Sistema de Conversión Multimodal

## Descripción General

REMForge Ultra es un sistema avanzado que convierte cualquier tipo de dato digital (texto, imágenes, audio, video) en **Registros Experienciales Multimodales (REMs)** con análisis fenomenológico profundo. El sistema está diseñado para capturar y estructurar experiencias sensoriales de manera que refleje la riqueza cualitativa de la conciencia humana.

## Características Principales

### 🧠 **Conversión Universal**
- **Texto**: Archivos .txt, .md, strings en memoria
- **Imágenes**: .png, .jpg, .jpeg, .bmp, arrays/tensores
- **Audio**: .wav, .mp3, arrays/tensores
- **Video**: .mp4, .avi, .mov (extrae keyframes + audio)
- **Detección automática**: `forge_from_file()` detecta el tipo automáticamente

### 🔬 **Análisis Fenomenológico Profundo**
- **Qualia Detection**: Identifica experiencias sensoriales puras
- **Intentionality Analysis**: Determina el modo intencional de la experiencia
- **Temporal Structure**: Analiza la estructura temporal de las experiencias
- **Affective Computing**: Mide valencia afectiva y emociones
- **Spatial Horizon**: Determina el espacio perceptual de la experiencia

### 📊 **Visualización Interactiva**
- **Dashboard Web**: Interfaz profesional con gráficos interactivos
- **Análisis en Tiempo Real**: Procesamiento y visualización simultánea
- **Múltiples Visualizaciones**: Distribución de modalidades, evolución temporal, análisis afectivo
- **Exportación**: JSON, CSV, HTML reports

### 🛠️ **Arquitectura Técnica**
- **Modelos Inteligentes**: DeBERTaV3, CLIP, Wav2Vec2, Whisper
- **Fallbacks Robutos**: Funciona sin GPUs ni modelos pesados
- **Extensible**: Fácil añadir nuevos tipos de datos
- **Estandarizado**: Todos los outputs tienen el mismo esquema JSON

## Instalación y Uso

### Requisitos Previos

```bash
# Instalar dependencias principales
pip install torch torchvision torchaudio
pip install transformers  # Para DeBERTa, CLIP, etc.
pip install pillow  # Para imágenes
pip install opencv-python  # Para video
pip install moviepy  # Para audio en video
pip install plotly  # Para visualizaciones
pip install pandas numpy  # Para análisis de datos
```

### Uso Básico

```python
from remforge_ultra import REMForgeUltra

# Inicializar el sistema
forge = REMForgeUltra(device="auto", enable_advanced_models=True)

# Procesar diferentes tipos de archivos
rem_text = forge.forge_from_text("Veo un color rojo intenso...")
rem_image = forge.forge_from_image("imagen.jpg")
rem_audio = forge.forge_from_audio("audio.wav")
rem_video = forge.forge_from_video("video.mp4")

# Detección automática de tipo
rem_auto = forge.forge_from_file("archivo.txt")

# Exportar resultados
forge.export_to_json(rem_text, "output/rem_text.json")
```

### Uso de la Interfaz Web

1. **Abrir la aplicación**: Abrir `index.html` en un navegador web
2. **Subir archivos**: Arrastrar o seleccionar archivos para procesar
3. **Configurar análisis**: Elegir tipo de análisis y opciones
4. **Procesar**: Click en "Procesar Archivos"
5. **Explorar resultados**: Ver gráficos interactivos y estadísticas
6. **Exportar**: Descargar datos en diferentes formatos

## Estructura de Datos REM

Cada REM generado contiene:

```json
{
  "rem_id": "uuid único",
  "timestamp": "2024-01-15T10:30:00Z",
  "narrative_stream": "Descripción textual de la experiencia",
  "intentional_act": {
    "mode": "perception|memory|imagination|reflection|language|action|contemplation",
    "directedness": "tipo de intencionalidad",
    "temporal_phase": "present|past|future|timeless|transition"
  },
  "sensorium": {
    "modality_confidence": {
      "visual": 0.95,
      "auditory": 0.20,
      "haptic": 0.10,
      "affective": 0.60,
      "proprioceptive": 0.30
    },
    "affective_valence": 0.7,
    "spatial_horizon": "peripersonal_space|extrapersonal_space|bodily_space|imaginal_space|digital_space|ambiental_space"
  },
  "semantic_contamination": {
    "lexical_anchors": ["palabras", "clave", "semánticas"],
    "contamination_strength": 0.6,
    "qualia_tokens": [
      {"token": "brillante", "is_sensorial": true, "is_affective": false}
    ]
  },
  "modality_specific": {
    "características": "específicas del tipo de dato"
  }
}
```

## Ejemplos de Uso

### Análisis de Texto

```python
# Texto con contenido fenomenológico
text = """
Veo un color rojo intenso en la superficie de la mesa mientras 
escucho el sonido suave de la lluvia contra la ventana. 
La textura del papel bajo mis dedos me trae recuerdos de infancia.
"""

rem = forge.forge_from_text(text, context="Experiencia sensorial en interiores")
print(f"Qualia detectados: {len(rem.semantic_contamination['qualia_tokens'])}")
print(f"Modalidad dominante: {max(rem.sensorium['modality_confidence'].items(), key=lambda x: x[1])}")
```

### Análisis de Imagen

```python
# Procesar imagen con análisis avanzado
rem = forge.forge_from_image(
    "foto.jpg",
    viewpoint="first_person",
    color_analysis=True,
    depth_estimation=True
)

print(f"Complejidad de textura: {rem.modality_specific['image_features']['texture_complexity']}")
print(f"Diversidad de color: {rem.modality_specific['image_features']['color_diversity']}")
```

### Análisis de Audio

```python
# Audio con análisis de prosodia y emoción
rem = forge.forge_from_audio(
    "grabacion.wav",
    acoustic_context="conversacional",
    extract_emotion=True,
    prosody_analysis=True
)

print(f"Emoción detectada: {rem.semantic_contamination.get('emotion_data', {}).get('primary_emotion')}")
print(f"F0 promedio: {rem.modality_specific['audio_features']['f0_mean']} Hz")
```

### Análisis de Video

```python
# Video con análisis temporal
rem_sequence = forge.forge_from_video(
    "video.mp4",
    keyframe_interval=0.5,  # 2 REMs por segundo
    motion_analysis=True,
    scene_boundary_detection=True,
    temporal_coherence=True
)

print(f"Secuencia generada: {len(rem_sequence)} REMs")
stats = forge.analyze_rem_statistics(rem_sequence)
print(f"Valencia promedio: {stats['affective_profile']['mean_valence']}")
```

## Visualizaciones Disponibles

### Dashboard Web

La interfaz web incluye:

1. **Distribución de Modalidades**: Gráfico de barras con confianza por modalidad
2. **Evolución Temporal**: Línea de valencia afectiva a lo largo del tiempo
3. **Análisis Afectivo**: Histograma de distribución de valencia
4. **Horizontes Espaciales**: Gráfico de pastel de distribución espacial
5. **Modos Intencionales**: Barras horizontales de frecuencias modales
6. **Red de Qualia**: Frecuencia de qualia detectados

### Exportación de Datos

- **JSON**: Datos completos con todos los campos
- **CSV**: Datos tabulares para análisis estadístico
- **HTML Report**: Reporte completo con visualizaciones integradas

## Arquitectura del Sistema

### Componentes Principales

1. **REMForgeUltra**: Clase principal de procesamiento
2. **REMForgeVisualizer**: Sistema de visualización web
3. **REMForgeInterface**: Interfaz de usuario interactiva
4. **REMForgeUtils**: Utilidades y funciones auxiliares

### Flujo de Procesamiento

1. **Carga de Archivos**: Detección automática de tipo
2. **Preprocesamiento**: Normalización y validación
3. **Análisis Modal**: Extracción de features específicas por modalidad
4. **Síntesis Fenomenológica**: Integración de qualia e intencionalidad
5. **Generación REM**: Creación del registro estructurado
6. **Visualización**: Representación interactiva de los datos

## Análisis Fenomenológico

### Qualia Detection

El sistema identifica palabras y características que denotan experiencias sensoriales puras:

- **Visuales**: "rojo", "brillante", "oscuro", "luminoso"
- **Auditivas**: "alto", "bajo", "suave", "sordo"
- **Hápticas**: "áspero", "liso", "cálido", "frío"
- **Afectivas**: "feliz", "triste", "emocionado", "tranquilo"

### Intentionalidad

Analiza el modo de conciencia de la experiencia:

- **Percepción**: Experiencias sensoriales inmediatas
- **Memoria**: Recuerdos y experiencias pasadas
- **Imaginación**: Experiencias posibles o inventadas
- **Reflexión**: Análisis y pensamiento conceptual
- **Contemplación**: Estados de conciencia alterada

### Estructura Temporal

- **Presente**: Experiencias inmediatas
- **Pasado**: Recuerdos y memoria
- **Futuro**: Expectativas e imaginación
- **Atemporal**: Experiencias sin referencia temporal

## Aplicaciones

### Investigación Científica
- **Neurociencia**: Estudio de correlatos neurales de la conciencia
- **Psicología**: Análisis de experiencias subjetivas
- **Fenomenología**: Investigación de estructuras de la experiencia

### Tecnología
- **IA Consciente**: Sistemas con conciencia artificial
- **Interfaz Cerebro-Computadora**: Decodificación de experiencias
- **Realidad Virtual**: Experiencias inmersivas cualitativas

### Aplicaciones Prácticas
- **Terapia**: Análisis de experiencias terapéuticas
- **Educación**: Sistemas de aprendizaje experiencial
- **Entretenimiento**: Contenido con conciencia de qualia

## Limitaciones y Consideraciones

### Limitaciones Técnicas
- **Procesamiento**: Requiere recursos computacionales significativos
- **Precisión**: Los modelos pueden tener sesgos culturales y lingüísticos
- **Interpretación**: Los qualia son subjetivos y difíciles de cuantificar

### Consideraciones Éticas
- **Privacidad**: Los datos de experiencia son altamente personales
- **Consentimiento**: Requiere consentimiento informado para análisis
- **Uso Responsable**: Evitar aplicaciones que puedan manipular experiencias

## Contribución y Desarrollo

### Arquitectura Extensible

El sistema está diseñado para ser fácilmente extensible:

```python
# Añadir nuevo tipo de dato
class REMForgeCustom(REMForgeUltra):
    def forge_from_custom(self, data):
        # Implementar análisis específico
        return PhenomenalREM(...)

# Añadir nuevo modelo
class REMForgeWithCustomModel(REMForgeUltra):
    def _load_custom_model(self):
        # Cargar modelo personalizado
        self._models['custom'] = load_model()
```

### Mejores Prácticas

1. **Modularidad**: Mantener componentes separados y reutilizables
2. **Documentación**: Documentar todos los métodos y parámetros
3. **Testing**: Incluir tests para nuevas funcionalidades
4. **Compatibilidad**: Mantener retrocompatibilidad con versiones anteriores

## Futuras Mejoras

### Características Planificadas
- **Streaming en Tiempo Real**: Procesamiento de datos de cámara/web en directo
- **IoT Integration**: Conexión directa a sensores físicos
- **Modelos Cuantizados**: Optimización para dispositivos edge
- **Multilingüe**: Soporte extendido para diferentes idiomas

### Investigación en Curso
- **Validación Fenomenológica**: Ajuste de heurísticos con bases de datos anotadas
- **Correlatos Neuronales**: Integración con datos de EEG y fMRI
- **Conciencia Artificial**: Desarrollo de sistemas con conciencia genuina

## Licencia y Créditos

Este sistema está diseñado para avanzar la comprensión de la conciencia y las experiencias subjetivas. Se alienta su uso para investigación científica y aplicaciones beneficiosas para la humanidad.

---

**REMForge Ultra** - Convirtiendo datos en experiencias, una cualidad a la vez.

*"La ciencia de la conciencia requiere no solo medir, sino comprender la riqueza cualitativa de la experiencia subjetiva."*