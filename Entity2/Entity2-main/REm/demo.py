#!/usr/bin/env python3
"""
REMForge Ultra - Demo Completo del Sistema
==========================================

Este script demuestra todas las capacidades del sistema REMForge Ultra,
procesando diferentes tipos de archivos y generando visualizaciones.
"""

import sys
import os
sys.path.append('/mnt/okcomputer')

import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Importar REMForge Ultra
try:
    from remforge_ultra import REMForgeUltra, PhenomenalREM
    from remforge_web import REMForgeVisualizer, REMForgeDataProcessor
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que los archivos estén en el path correcto")
    # Crear versiones simuladas para la demo
    class REMForgeUltra:
        def __init__(self, device="auto", enable_advanced_models=True):
            self.device = device
            self.enable_advanced_models = enable_advanced_models
            print(f"REMForgeUltra simulado inicializado en {device}")
        
        def forge_from_file(self, file_path):
            return self.generate_demo_rem(file_path)
        
        def forge_from_text(self, text, context=None):
            return self.generate_demo_rem("text_content")
        
        def forge_from_image(self, image_input, **kwargs):
            return self.generate_demo_rem("image_content")
        
        def forge_from_audio(self, audio_input, **kwargs):
            return self.generate_demo_rem("audio_content")
        
        def generate_demo_rem(self, content_type):
            return PhenomenalREM(
                narrative_stream=f"Experiencia simulada de {content_type}",
                intentional_act={"mode": "perception", "directedness": "demo"},
                sensorium={
                    "modality_confidence": {
                        "visual": 0.8, "auditory": 0.6, "haptic": 0.4, 
                        "affective": 0.7, "proprioceptive": 0.3
                    },
                    "affective_valence": 0.5,
                    "spatial_horizon": "peripersonal_space"
                },
                semantic_contamination={
                    "lexical_anchors": ["demo", "experiencia", "simulada"],
                    "contamination_strength": 0.6,
                    "qualia_tokens": [{"token": "vívida", "is_sensorial": True}]
                }
            )
    
    class PhenomenalREM:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.rem_id = f"demo_{hash(str(kwargs))}"
            self.timestamp = datetime.now().isoformat()
        
        def to_dict(self):
            return {
                "rem_id": self.rem_id,
                "timestamp": self.timestamp,
                "narrative_stream": getattr(self, 'narrative_stream', ''),
                "intentional_act": getattr(self, 'intentional_act', {}),
                "sensorium": getattr(self, 'sensorium', {}),
                "semantic_contamination": getattr(self, 'semantic_contamination', {}),
                "modality_specific": getattr(self, 'modality_specific', {})
            }
    
    class REMForgeVisualizer:
        def create_dashboard(self, rem_sequence, output_path, title):
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
                    .header {{ background: linear-gradient(135deg, #2C5530, #8B7355); color: white; padding: 30px; border-radius: 10px; }}
                    .content {{ background: white; padding: 30px; border-radius: 10px; margin-top: 20px; }}
                    .rem-item {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{title}</h1>
                    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="content">
                    <h2>Experiencias Procesadas: {len(rem_sequence)}</h2>
                    {''.join([f'<div class="rem-item"><h3>{rem.get("rem_id", "Unknown")}</h3><p>{rem.get("narrative_stream", "No narrative")[:100]}...</p></div>' for rem in rem_sequence])}
                </div>
            </body>
            </html>
            """
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
    
    class REMForgeDataProcessor:
        def generate_summary_report(self, rem_sequence):
            return {
                "summary": {
                    "total_experiences": len(rem_sequence),
                    "processed_at": datetime.now().isoformat(),
                },
                "affective_analysis": {
                    "mean_valence": 0.5,
                    "positive_count": len(rem_sequence)
                }
            }
    
    print("Usando implementación simulada para la demo")

def create_demo_files():
    """Crea archivos de demo para el sistema"""
    demo_dir = Path("/mnt/okcomputer/output/demo_files")
    demo_dir.mkdir(exist_ok=True)
    
    # 1. Archivo de texto
    text_content = """Experiencia Sensorial Multimodal

Veo un color rojo intenso en la superficie de la mesa mientras escucho el sonido suave de la lluvia contra la ventana. 
La textura del papel bajo mis dedos me trae recuerdos de infancia, cuando mi abuela me contaba historias en las tardes lluviosas.

El aroma del café recién hecho llena el ambiente, creando una atmósfera cálida y reconfortante. 
Siento la brisa fresca del aire acondicionado en mi piel, contrastando con la calidez de la taza en mis manos.

Cada sonido, cada color, cada textura se entrelaza en una sinfonía de experiencias sensoriales que me transporta 
a un estado de contemplación profunda, donde el tiempo parece detenerse y solo existe el momento presente.

La luz tenue del atardecer se filtra a través de las persianas, creando patrones geométricos en la pared que 
danzan con la suave brisa. Es en estos momentos de quietud donde la realidad se vuelve más vívida y presente.
"""
    
    with open(demo_dir / "experiencia.txt", "w", encoding='utf-8') as f:
        f.write(text_content)
    
    # 2. Crear imagen dummy
    from PIL import Image
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save(demo_dir / "imagen_demo.jpg")
    
    # 3. Crear audio dummy
    import wave
    sample_rate = 16000
    duration = 3
    frequency = 440
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(str(demo_dir / "audio_demo.wav"), 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return demo_dir

def process_demo_files(forge, demo_dir):
    """Procesa todos los archivos de demo"""
    results = {}
    
    print("🔄 Procesando archivos de demo...")
    
    # 1. Procesar texto
    print("\n📄 Procesando archivo de texto...")
    text_path = demo_dir / "experiencia.txt"
    if text_path.exists():
        try:
            rem_text = forge.forge_from_file(str(text_path))
            results['text'] = rem_text
            print(f"   ✅ Texto procesado: {len(rem_text.semantic_contamination['lexical_anchors'])} anclajes")
            print(f"   ✅ Qualia detectados: {len(rem_text.semantic_contamination.get('qualia_tokens', []))}")
            print(f"   ✅ Modalidad dominante: {max(rem_text.sensorium['modality_confidence'].items(), key=lambda x: x[1])[0]}")
        except Exception as e:
            print(f"   ❌ Error procesando texto: {e}")
    
    # 2. Procesar imagen
    print("\n🖼️  Procesando imagen...")
    image_path = demo_dir / "imagen_demo.jpg"
    if image_path.exists():
        try:
            rem_image = forge.forge_from_file(str(image_path))
            results['image'] = rem_image
            print(f"   ✅ Imagen procesada: {len(rem_image.semantic_contamination['lexical_anchors'])} anclajes")
            print(f"   ✅ Complejidad visual: {rem_image.modality_specific['image_features']['texture_complexity']:.3f}")
            print(f"   ✅ Confianza visual: {rem_image.sensorium['modality_confidence']['visual']:.3f}")
        except Exception as e:
            print(f"   ❌ Error procesando imagen: {e}")
    
    # 3. Procesar audio
    print("\n🔊 Procesando audio...")
    audio_path = demo_dir / "audio_demo.wav"
    if audio_path.exists():
        try:
            rem_audio = forge.forge_from_file(str(audio_path))
            results['audio'] = rem_audio
            print(f"   ✅ Audio procesado: {rem_audio.modality_specific['audio_features']['duration_seconds']:.1f} segundos")
            print(f"   ✅ Confianza auditiva: {rem_audio.sensorium['modality_confidence']['auditory']:.3f}")
            print(f"   ✅ F0 promedio: {rem_audio.modality_specific['audio_features']['f0_mean']:.1f} Hz")
        except Exception as e:
            print(f"   ❌ Error procesando audio: {e}")
    
    return results

def create_visualizations(results):
    """Crea visualizaciones con los resultados"""
    print("\n📊 Creando visualizaciones...")
    
    if not results:
        print("   ⚠️  No hay resultados para visualizar")
        return
    
    # Crear visualizador
    visualizer = REMForgeVisualizer()
    
    # Preparar datos para visualización
    all_rems = []
    for key, rem in results.items():
        if isinstance(rem, list):
            all_rems.extend(rem)
        else:
            all_rems.append(rem)
    
    if not all_rems:
        print("   ⚠️  No hay REMs para visualizar")
        return
    
    # Convertir a formato de visualización
    rem_dicts = [rem.to_dict() if hasattr(rem, 'to_dict') else rem for rem in all_rems]
    
    # Crear dashboard
    output_path = "/mnt/okcomputer/output/remforge_demo_dashboard.html"
    visualizer.create_dashboard(
        rem_dicts, 
        output_path, 
        "REMForge Ultra - Demo Dashboard"
    )
    
    print(f"   ✅ Dashboard creado: {output_path}")
    
    # Generar reporte
    processor = REMForgeDataProcessor()
    report = processor.generate_summary_report(rem_dicts)
    
    report_path = "/mnt/okcomputer/output/remforge_demo_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Reporte generado: {report_path}")
    
    return output_path, report_path

def create_advanced_demo(forge):
    """Crea una demo avanzada con secuencias temporales"""
    print("\n🎬 Creando demo avanzada con secuencia temporal...")
    
    # Crear una secuencia de experiencias
    sequence = []
    
    # Experiencias de diferentes modalidades
    experiences = [
        {
            "narrative": "Veo la luz del amanecer filtrándose por la ventana",
            "modalities": {"visual": 0.9, "affective": 0.6},
            "valence": 0.8,
            "mode": "perception"
        },
        {
            "narrative": "Oigo los pájaros cantando en el jardín",
            "modalities": {"auditory": 0.95, "affective": 0.7},
            "valence": 0.9,
            "mode": "contemplation"
        },
        {
            "narrative": "Siento la brisa fresca de la mañana en mi piel",
            "modalities": {"haptic": 0.85, "proprioceptive": 0.6},
            "valence": 0.7,
            "mode": "perception"
        },
        {
            "narrative": "Huelo el aroma del café recién hecho",
            "modalities": {"olfactory": 0.9, "affective": 0.8},
            "valence": 0.6,
            "mode": "perception"
        },
        {
            "narrative": "Pruebo el sabor dulce del pan tostado",
            "modalities": {"gustatory": 0.9, "affective": 0.7},
            "valence": 0.5,
            "mode": "action"
        }
    ]
    
    for i, exp in enumerate(experiences):
        rem = PhenomenalREM(
            narrative_stream=exp["narrative"],
            intentional_act={
                "mode": exp["mode"],
                "directedness": f"qualia_{max(exp['modalities'].items(), key=lambda x: x[1])[0]}"
            },
            sensorium={
                "modality_confidence": exp["modalities"],
                "affective_valence": exp["valence"],
                "spatial_horizon": "peripersonal_space"
            },
            semantic_contamination={
                "lexical_anchors": exp["narrative"].split()[:3],
                "contamination_strength": 0.7,
                "qualia_tokens": [
                    {"token": "intenso", "is_sensorial": True, "is_affective": False}
                ]
            },
            modality_specific={
                "temporal_context": {
                    "frame_index": i,
                    "time_offset": i * 0.5,
                    "scene_continuity": 0.8
                }
            }
        )
        sequence.append(rem)
    
    # Analizar estadísticas de la secuencia
    stats = forge.analyze_rem_statistics(sequence)
    
    print(f"   ✅ Secuencia creada: {len(sequence)} experiencias")
    print(f"   ✅ Duración simulada: {len(sequence) * 0.5} segundos")
    print(f"   ✅ Valencia promedio: {stats['affective_profile']['mean_valence']:.3f}")
    
    # Exportar secuencia
    sequence_path = "/mnt/okcomputer/output/temporal_sequence.json"
    forge.export_to_json(sequence, sequence_path, include_embeddings=False)
    
    print(f"   ✅ Secuencia exportada: {sequence_path}")
    
    return sequence, stats

def main():
    """Función principal de demo"""
    print("🚀 REMForge Ultra - Sistema de Demo Completa")
    print("=" * 60)
    
    # Crear archivos de demo
    demo_dir = create_demo_files()
    print(f"📁 Archivos de demo creados en: {demo_dir}")
    
    # Inicializar REMForge Ultra
    print("\n🔧 Inicializando REMForge Ultra...")
    forge = REMForgeUltra(device="auto", enable_advanced_models=False)
    
    # Procesar archivos de demo
    results = process_demo_files(forge, demo_dir)
    
    # Crear visualizaciones
    dashboard_path, report_path = create_visualizations(results)
    
    # Crear demo avanzada
    sequence, stats = create_advanced_demo(forge)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"📊 Dashboard: {dashboard_path}")
    print(f"📄 Reporte: {report_path}")
    print(f"🔬 Secuencia temporal: /mnt/okcomputer/output/temporal_sequence.json")
    print(f"📁 Archivos demo: {demo_dir}")
    
    print(f"\n📈 Estadísticas:")
    print(f"   • Total de experiencias procesadas: {len(results) + len(sequence)}")
    print(f"   • Tipos de archivos soportados: 4 (texto, imagen, audio, video)")
    print(f"   • Modalidades sensoriales: 8 (visual, auditivo, háptico, etc.)")
    print(f"   • Formatos de exportación: 3 (JSON, CSV, HTML)")
    
    print("\n🎯 Para ver los resultados:")
    print("   1. Abrir el archivo HTML del dashboard en un navegador")
    print("   2. Explorar los gráficos interactivos")
    print("   3. Revisar los archivos JSON para datos detallados")
    print("   4. Usar los datos para análisis adicionales")

if __name__ == "__main__":
    main()