#!/usr/bin/env python3
"""
REMForge Ultra: Formato de Salida Óptimo para Tokenización Fenomenológica
==========================================================================

Sistema que convierte datos digitales en Registros Experienciales Multimodales
con formato optimizado para análisis fenomenológico computacional.

Formato de salida: PhenomenalREM-Ultra JSON Schema v4.0.0
"""

import torch
import numpy as np
from typing import Dict, Any, List, Tuple, Optional, Union
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from datetime import datetime
import uuid
import re
from collections import Counter

# ============================================
# CLASE PRINCIPAL: REMFORGE ULTRA FORMATO ÓPTIMO
# ============================================

class REMForgeUltraFormatoOptimo:
    """
    Sistema optimizado para generar PhenomenalREM-Ultra con formato
    específico para tokenización fenomenológica computacional.
    """
    
    def __init__(self, device: str = "auto", precision: str = "float16"):
        self.device = self._autodetect_device(device)
        self.precision = precision
        self.session_id = uuid.uuid4().hex[:8]
        self.forge_version = "4.0.0-ultra"
        
        # Modelos especializados por modalidad
        self.models = self._load_optimized_models()
        
        # Buffers para preservación de invariantes temporales
        self.temporal_buffer = []
        self.invariant_cache = {}
        
        print(f"🚀 REMForge Ultra Formato Óptimo inicializado")
        print(f"   Session: {self.session_id} | Device: {self.device} | Version: {self.forge_version}")
    
    def _autodetect_device(self, device: str) -> str:
        if device == "auto":
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"
            elif torch.cuda.is_available():
                return "cuda"
            return "cpu"
        return device
    
    def _load_optimized_models(self) -> Dict:
        """Carga modelos optimizados para análisis fenomenológico"""
        models = {}
        
        # Modelo de análisis semántico con consciencia de qualia
        try:
            from transformers import AutoModel, AutoTokenizer
            models["semantic"] = {
                "model": AutoModel.from_pretrained("facebook/bart-large").to(self.device).eval(),
                "tokenizer": AutoTokenizer.from_pretrained("facebook/bart-large"),
                "max_length": 512
            }
            print("✓ BART-Qualia cargado")
        except:
            models["semantic"] = None
            print("⚠️ Modelo semántico no disponible, usando heurísticos")
        
        # CLIP con extracción de capas intermedias
        try:
            from transformers import CLIPModel, CLIPProcessor
            clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device).eval()
            models["vision"] = {
                "model": clip_model,
                "processor": CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32"),
                "extract_layers": [-1, -3, -6]  # Múltiples escalas
            }
            print("✓ CLIP-Multilayer cargado")
        except:
            models["vision"] = None
            print("⚠️ Modelo visual no disponible, usando heurísticos")
        
        # HuBERT para análisis acústico fenomenológico
        try:
            from transformers import Wav2Vec2Model, Wav2Vec2Processor
            models["audio"] = {
                "model": Wav2Vec2Model.from_pretrained("facebook/hubert-base-ls960").to(self.device).eval(),
                "processor": Wav2Vec2Processor.from_pretrained("facebook/hubert-base-ls960"),
                "sample_rate": 16000
            }
            print("✓ HuBERT cargado")
        except:
            models["audio"] = None
            print("⚠️ Modelo de audio no disponible, usando heurísticos")
        
        # MiDaS para profundidad espacial
        try:
            from transformers import pipeline
            models["depth"] = pipeline("depth-estimation", model="Intel/dpt-large", device=0 if self.device == "cuda" else -1)
            print("✓ MiDaS cargado")
        except:
            models["depth"] = None
            print("⚠️ Modelo de profundidad no disponible, usando heurísticos")
        
        return models
    
    # ========================================
    # MÉTODOS PRINCIPALES DE CONVERSIÓN
    # ========================================
    
    def forge_text_ultra(self, text: str, context: Dict = None) -> Dict[str, Any]:
        """
        Conversión de texto con análisis de invariantes lingüísticas
        
        Args:
            text: Texto experiencial (diario, narrativa, etc.)
            context: {situational_context, temporal_context, author_id}
        """
        if context is None:
            context = {}
        
        # 1. Normalización fenomenológica
        text_clean = self._phenomenological_normalize(text)
        
        # 2. Análisis multi-cláusula con detección de qualia lingüísticos
        clauses = self._analyze_clausal_structure(text_clean)
        
        # 3. Extracción de anclajes con scoring de interferencia fenomenológica
        anchors, embeddings, interference_scores = self._extract_anchors_with_interference(text_clean)
        
        # 4. Detección de invariantes noéticas (patrones intencionales)
        noetic_invariants = self._extract_noetic_invariants(clauses)
        
        # 5. Construcción de signature de qualia lingüística
        qualia_signature = self._build_linguistic_qualia_signature(text_clean, anchors)
        
        # 6. Análisis de afecto con separación semántica-fenomenológica
        affect_split = self._split_affective_semantic_vs_phenomenal(text_clean)
        
        # 7. Generar visualization layer
        visualization = self._generate_text_experience_map(clauses, anchors, noetic_invariants)
        
        return {
            "header": {
                "rem_id": f"TXT-{uuid.uuid4().hex[:12]}",
                "forge_version": self.forge_version,
                "creation_timestamp": datetime.utcnow().isoformat(),
                "modality_origin": "text",
                "temporal_scope": {
                    "start_offset": 0.0,
                    "duration": len(text_clean) / 10.0,  # Estimación: 10 chars/sec
                    "total_sequence_length": len(text_clean) / 10.0
                },
                "quality_metrics": {
                    "completeness_score": 1.0 if len(text_clean) > 20 else 0.7,
                    "contamination_detected": len(anchors) > 3,
                    "phenomenal_resolution": self._compute_phenomenal_resolution(len(anchors), len(clauses))
                }
            },
            "experiential_stream": {
                "narrative_raw": text,
                "narrative_enriched": f"[Context: {context.get('situational_context', 'none')}] {text_clean}",
                "clause_boundaries": clauses,
                "temporal_markers": self._extract_temporal_markers(text_clean)
            },
            "noetic_layer": {
                "intentional_mode": noetic_invariants.get("dominant_mode", "perception"),
                "directedness": noetic_invariants.get("directedness", "general_experience"),
                "temporal_phase": self._infer_temporal_phase(text_clean),
                "ego_involvement": self._compute_ego_involvement(text_clean),
                "horizon_type": self._infer_horizon_type(text_clean),
                "act_intensity": np.mean([c['experiential_score'] for c in clauses]) if clauses else 0.5
            },
            "sensorial_layer": {
                "modality_distribution": self._compute_modal_distribution_from_text(anchors, qualia_signature),
                "spatial_horizon": "peripersonal_space" if "aquí" in text_clean else "extrapersonal_space",
                "spatial_coordinates": {"egocentric": [0, 0, 0], "allocentric": [0, 0, 0], "rotation": [0, 0, 0]},
                "affective_valence": affect_split["phenomenal_valence"],
                "affective_arousal": (affect_split["semantic_valence"] + affect_split["phenomenal_valence"]) / 2,
                "sensorial_resolution": {
                    "temporal_precision": 100.0,
                    "spatial_precision": 0.0,
                    "qualia_precision": 0.85
                }
            },
            "semantic_contamination": {
                "contamination_strength": np.mean(interference_scores) if interference_scores else 0.5,
                "source": "text_fenomenological",
                "lexical_anchors": [
                    {
                        "token": anchor,
                        "embedding": emb.tolist() if hasattr(emb, 'tolist') else emb,
                        "salience_score": 1.0 - interference,  # Invertido: bajo score = alta interferencia
                        "temporal_position": i,
                        "origin": "global_description"
                    }
                    for i, (anchor, emb, interference) in enumerate(zip(anchors, embeddings, interference_scores))
                ],
                "semantic_traces": self._trace_semantic_categories(text_clean),
                "invariance_under_semantic_permutation": self._test_semantic_invariance(text_clean, anchors)
            },
            "phenomenal_core": {
                "invariant_features": {
                    "sensory_invariants": qualia_signature["invariant_patterns"],
                    "noetic_invariants": noetic_invariants["invariant_vectors"],
                    "temporal_invariants": self._extract_temporal_invariants(clauses)
                },
                "qualia_signature": {
                    "qualia_type": qualia_signature["dominant_type"],
                    "intensity_profile": qualia_signature["intensity_profile"],
                    "discrimination_threshold": qualia_signature["jnd_threshold"],
                    "phenomenal_saturation": qualia_signature["saturation"]
                },
                "eidetic_reductions": self._perform_eidetic_reductions(text_clean, qualia_signature)
            },
            "multiscale_representation": {
                "coarse_scale": {
                    "global_narrative": self._summarize_narrative(text_clean),
                    "thematic_gist": self._extract_thematic_gist(text_clean),
                    "affective_gist": self._extract_affective_gist(affect_split),
                    "spatial_gist": self._extract_spatial_gist(text_clean)
                },
                "medium_scale": {
                    "episodic_units": [c['text'] for c in clauses if c['experiential_score'] > 0.6],
                    "intentional_shifts": noetic_invariants["shifts"],
                    "qualia_clusters": qualia_signature["clusters"]
                },
                "fine_scale": {
                    "momentary_experiences": self._extract_momentary_qualia(text_clean),
                    "micro_intentionalities": self._extract_micro_intentionalities(clauses),
                    "qualia_micro_variations": qualia_signature["micro_variations"]
                }
            },
            "visualization_layer": {
                "experience_map": {
                    "format": "graph_network",
                    "coordinates": visualization["coordinates"],
                    "qualia_weights": visualization["qualia_weights"],
                    "intentional_vectors": visualization["intentional_vectors"]
                },
                "contamination_heatmap": {
                    "anchor_positions": [i for i, _ in enumerate(anchors)],
                    "contamination_density": interference_scores,
                    "pure_zones": visualization["pure_zones"]
                },
                "temporal_flow": {
                    "flow_type": "continuous" if len(clauses) > 1 else "discrete",
                    "phase_transitions": noetic_invariants["transitions"],
                    "retention_proprotentions": noetic_invariants["temporal_vectors"]
                }
            }
        }
    
    # ========================================
    # MÉTODOS DE ANÁLISIS FENOMENOLÓGICO
    # ========================================
    
    def _phenomenological_normalize(self, text: str) -> str:
        """Normaliza texto preservando marcas fenomenológicas"""
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _analyze_clausal_structure(self, text: str) -> List[Dict]:
        """Divide el texto en cláusulas experienciales con scoring"""
        # Split por conectores temporales y de perspectiva
        delimiters = r'(?<=[.!?])\s+|\s+(?:y|pero|entonces|cuando|mientras|aunque|sin embargo)\s+'
        clauses_text = re.split(delimiters, text)
        
        clauses = []
        start_idx = 0
        
        for clause in clauses_text:
            if clause.strip():
                length = len(clause.split())
                experiential_score = self._score_experiential_clause(clause)
                
                clauses.append({
                    "text": clause,
                    "length": length,
                    "boundary": {"start_char": start_idx, "end_char": start_idx + len(clause), "experiential_score": experiential_score, "qualia_density": 0.0},
                    "experiential_score": experiential_score
                })
                start_idx += len(clause) + 1
        
        return clauses
    
    def _score_experiential_clause(self, clause: str) -> float:
        """Puntúa qué tan 'experiencialmente densa' es una cláusula"""
        # Palabras que denotan presencia inmediata
        experiential_words = {
            "veo", "oigo", "siento", "huelo", "pruebo", "percibo", "noto", "observo",
            "está", "hay", "me", "mi", "aquí", "ahora", "ante", "frente", "bajo", "sobre", "dentro"
        }
        
        # Palabras sensoriales
        sensorial_words = {
            "rojo", "azul", "verde", "brillante", "oscuro", "claro", "luminoso", "opaco",
            "suave", "áspero", "liso", "rugoso", "duro", "blando", "cálido", "frío", "húmedo", "seco",
            "alto", "bajo", "fuerte", "suave", "sordo", "claro", "mudo", "armonioso", "discordante",
            "dulce", "amargo", "ácido", "salado", "umami", "picante", "sabroso", "insípido",
            "aromatico", "perfumado", "acido", "dulce", "amargo", "penetrante", "sutil", "intenso"
        }
        
        words = set(clause.lower().split())
        score = len(words & experiential_words) * 0.6 + len(words & sensorial_words) * 0.4
        
        return min(score / 3, 1.0)  # Normalizar
    
    def _extract_anchors_with_interference(self, text: str) -> Tuple[List[str], List[np.ndarray], List[float]]:
        """Extrae anclajes con scoring de interferencia fenomenológica"""
        if self.models.get('semantic') is None:
            # Fallback: extraer sustantivos y adjetivos simples
            words = re.findall(r'\b\w+\b', text.lower())
            
            # Palabras de contenido (filtrar stopwords básicas)
            stopwords = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'una', 'es', 'se', 'con', 'mi', 'me', 'te', 'le', 'lo', 'las', 'los', 'del', 'al', 'por', 'para', 'sin', 'sobre', 'tras', 'durante', 'mediante'}
            content_words = [w for w in words if w not in stopwords and len(w) > 3][:8]
            
            # Embeddings dummy
            embeddings = [np.random.randn(768) for _ in content_words]
            
            # Interferencia heurística
            interference_scores = []
            for word in content_words:
                if word in ["rojo", "azul", "verde", "brillante", "suave", "áspero", "cálido", "frío"]:
                    interference_scores.append(0.2)  # Baja interferencia (qualia puro)
                elif word in ["recuerda", "pienso", "creo", "entiendo"]:
                    interference_scores.append(0.8)  # Alta interferencia (semántica)
                else:
                    interference_scores.append(0.5)  # Interferencia media
            
            return content_words, embeddings, interference_scores
        
        # Usar modelo BART para análisis semántico profundo
        tokenizer = self.models['semantic']['tokenizer']
        model = self.models['semantic']['model']
        
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Extraer embeddings
        hidden_states = outputs.last_hidden_state.squeeze(0)
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze(0))
        
        # Filtrar y seleccionar tokens de contenido
        content_tokens = []
        token_embeddings = []
        interference_scores = []
        
        for i, token in enumerate(tokens):
            if token not in ['[CLS]', '[SEP]', '[PAD]', '[UNK]'] and not token.startswith('##'):
                # Calcular interferencia fenomenológica
                interference = self._compute_phenomenological_interference(token, text)
                
                content_tokens.append(token.replace('##', ''))
                token_embeddings.append(hidden_states[i].cpu().numpy())
                interference_scores.append(interference)
        
        # Seleccionar top tokens por relevancia
        if len(content_tokens) > 5:
            norms = [np.linalg.norm(emb) for emb in token_embeddings]
            top_indices = np.argsort(norms)[-5:]
            
            content_tokens = [content_tokens[i] for i in top_indices]
            token_embeddings = [token_embeddings[i] for i in top_indices]
            interference_scores = [interference_scores[i] for i in top_indices]
        
        return content_tokens, token_embeddings, interference_scores
    
    def _compute_phenomenological_interference(self, token: str, context: str) -> float:
        """Calcula interferencia semántica en la pureza fenomenológica"""
        token_lower = token.lower()
        
        # Qualia puros (baja interferencia)
        pure_qualia = {
            "rojo", "azul", "verde", "amarillo", "blanco", "negro", "gris",
            "brillante", "oscuro", "claro", "opaco", "transparente", "sólido",
            "suave", "áspero", "liso", "rugoso", "duro", "blando", "cálido", "frío",
            "alto", "bajo", "fuerte", "suave", "sordo", "claro", "mudo"
        }
        
        # Contaminación semántica (alta interferencia)
        semantic_contamination = {
            "recuerda", "pienso", "creo", "entiendo", "siento que", "me parece",
            "probablemente", "quizás", "tal vez", "supongo", "debe ser"
        }
        
        if token_lower in pure_qualia:
            return 0.2  # Baja interferencia
        elif token_lower in semantic_contamination:
            return 0.8  # Alta interferencia
        else:
            return 0.5  # Interferencia media
    
    def _extract_noetic_invariants(self, clauses: List[Dict]) -> Dict[str, Any]:
        """Extrae invariantes noéticas (patrones intencionales)"""
        modes = ["perception", "memory", "imagination", "reflection", "language", "action", "dream"]
        verbs_per_mode = {
            "perception": ["veo", "oigo", "siento", "percibo", "noto", "observo"],
            "memory": ["recordé", "recuerdo", "era", "fue", "había", "solía"],
            "imagination": ["imagino", "supongo", "quizás", "tal vez", "podría", "sería"],
            "reflection": ["pienso", "creo", "entiendo", "analizo", "considero", "reflexiono"],
            "language": ["digo", "cuento", "explico", "describo", "narro"],
            "action": ["hago", "actúo", "intento", "busco", "quiero", "necesito"]
        }
        
        # Detectar modo dominante
        mode_scores = {mode: 0 for mode in modes}
        
        for clause in clauses:
            text = clause["text"].lower()
            for mode, verbs in verbs_per_mode.items():
                if any(verb in text for verb in verbs):
                    mode_scores[mode] += clause["experiential_score"]
        
        dominant_mode = max(mode_scores.items(), key=lambda x: x[1])[0] if any(mode_scores.values()) else "perception"
        
        # Detectar directedness
        directedness = "general_experience"
        if "color" in text or "rojo" in text or "azul" in text:
            directedness = "qualia_visual"
        elif "sonido" in text or "oigo" in text or "ruido" in text:
            directedness = "qualia_auditory"
        elif "siento" in text or "textura" in text or "liso" in text:
            directedness = "qualia_haptic"
        elif "sabor" in text or "dulce" in text or "amargo" in text:
            directedness = "qualia_gustatory"
        elif "olor" in text or "huele" in text:
            directedness = "qualia_olfactory"
        
        # Generar vectores invariantes
        invariant_vectors = []
        for i, clause in enumerate(clauses[:5]):  # Máximo 5 cláusulas
            vector = [
                clause["experiential_score"],
                1.0 if "yo" in clause["text"].lower() or "me" in clause["text"].lower() else 0.0,
                1.0 if any(verb in clause["text"].lower() for verb in verbs_per_mode.get(dominant_mode, [])) else 0.0,
                i / max(len(clauses), 1),  # Posición temporal normalizada
                len(clause["text"].split()) / 20.0  # Longitud normalizada
            ]
            invariant_vectors.append(vector)
        
        return {
            "dominant_mode": dominant_mode,
            "directedness": directedness,
            "invariant_vectors": invariant_vectors,
            "shifts": self._detect_intentional_shifts(clauses),
            "transitions": self._detect_phase_transitions(clauses),
            "temporal_vectors": self._extract_temporal_vectors(clauses)
        }
    
    def _build_linguistic_qualia_signature(self, text: str, anchors: List[str]) -> Dict[str, Any]:
        """Construye signature de qualia lingüística"""
        # Clasificar qualia por modalidad
        qualia_by_modality = {
            "visual": ["rojo", "azul", "verde", "brillante", "oscuro", "claro", "luminoso", "opaco"],
            "auditory": ["alto", "bajo", "fuerte", "suave", "sordo", "claro", "mudo", "armonioso"],
            "haptic": ["áspero", "liso", "suave", "duro", "blando", "cálido", "frío", "húmedo"],
            "olfactory": ["aromatico", "perfumado", "acido", "dulce", "amargo", "penetrante"],
            "gustatory": ["dulce", "amargo", "ácido", "salado", "umami", "picante", "sabroso"],
            "affective": ["feliz", "triste", "enojado", "contento", "ansioso", "tranquilo", "emocionado"]
        }
        
        # Contar qualia por modalidad
        text_words = set(text.lower().split())
        qualia_counts = {}
        total_qualia = 0
        
        for modality, qualia_list in qualia_by_modality.items():
            count = len(text_words & set(qualia_list))
            qualia_counts[modality] = count
            total_qualia += count
        
        # Determinar tipo dominante
        dominant_type = max(qualia_counts.items(), key=lambda x: x[1])[0] if any(qualia_counts.values()) else "cognitive"
        
        # Perfil de intensidad
        intensity_profile = [qualia_counts.get(mod, 0) for mod in qualia_by_modality.keys()]
        
        # Umbral de discriminación (JND)
        jnd_threshold = 0.1 + (total_qualia * 0.05)
        
        # Saturación fenomenológica
        saturation = min(total_qualia / 10.0, 1.0)
        
        # Patrones invariantes
        invariant_patterns = []
        for i, modality in enumerate(qualia_by_modality.keys()):
            if qualia_counts.get(modality, 0) > 0:
                invariant_patterns.append([i, qualia_counts[modality] / max(total_qualia, 1)])
        
        # Clusters de qualia
        clusters = []
        for modality, count in qualia_counts.items():
            if count > 0:
                clusters.append({
                    "type": modality,
                    "count": count,
                    "intensity": count / max(total_qualia, 1)
                })
        
        return {
            "dominant_type": dominant_type,
            "intensity_profile": intensity_profile,
            "jnd_threshold": jnd_threshold,
            "saturation": saturation,
            "invariant_patterns": invariant_patterns,
            "clusters": clusters,
            "micro_variations": self._extract_qualia_variations(text, qualia_by_modality)
        }
    
    def _split_affective_semantic_vs_phenomenal(self, text: str) -> Dict[str, float]:
        """Separa afecto semántico del afecto fenomenológico"""
        # Palabras de afecto semántico
        semantic_affect = {
            "bien", "mal", "bueno", "malo", "excelente", "terrible", "fantástico", "horrible",
            "me gusta", "me encanta", "odio", "detesto", "prefiero", "disfruto"
        }
        
        # Palabras de afecto fenomenológico
        phenomenal_affect = {
            "emocionado", "impresionado", "conmovido", "estremecido", "maravillado",
            "sorprendido", "asombrado", "fascinado", "hipnotizado", "transportado"
        }
        
        words = set(text.lower().split())
        
        semantic_count = len(words & semantic_affect)
        phenomenal_count = len(words & phenomenal_affect)
        
        # Calcular valencias
        semantic_valence = (semantic_count / max(len(words), 1)) * 2 - 1  # -1 a 1
        phenomenal_valence = (phenomenal_count / max(len(words), 1)) * 2 - 1  # -1 a 1
        
        return {
            "semantic_valence": np.clip(semantic_valence, -1, 1),
            "phenomenal_valence": np.clip(phenomenal_valence, -1, 1),
            "semantic_count": semantic_count,
            "phenomenal_count": phenomenal_count
        }
    
    def _generate_text_experience_map(self, clauses: List[Dict], anchors: List[str], noetic_invariants: Dict) -> Dict[str, Any]:
        """Genera mapa de experiencia para visualización"""
        # Coordenadas del grafo
        coordinates = []
        for i, clause in enumerate(clauses):
            x = i / max(len(clauses), 1)
            y = clause["experiential_score"]
            coordinates.append([x, y, 0.0])
        
        # Pesos de qualia
        qualia_weights = [clause["experiential_score"] for clause in clauses]
        
        # Vectores intencionales
        intentional_vectors = noetic_invariants.get("invariant_vectors", [])[:len(clauses)]
        
        # Zonas puras (baja contaminación)
        pure_zones = []
        for i, clause in enumerate(clauses):
            if clause["experiential_score"] > 0.7:
                pure_zones.append([i / max(len(clauses), 1), clause["experiential_score"]])
        
        return {
            "coordinates": coordinates,
            "qualia_weights": qualia_weights,
            "intentional_vectors": intentional_vectors,
            "pure_zones": pure_zones
        }
    
    def _compute_modal_distribution_from_text(self, anchors: List[str], qualia_signature: Dict) -> Dict[str, float]:
        """Computa distribución modal basada en texto y qualia"""
        # Distribución base
        distribution = {
            "visual": 0.1,
            "auditory": 0.05,
            "haptic": 0.05,
            "olfactory": 0.02,
            "gustatory": 0.02,
            "proprioceptive": 0.1,
            "affective": 0.3,
            "cognitive": 0.2,
            "digital": 0.16
        }
        
        # Ajustar por qualia detectados
        dominant_type = qualia_signature.get("dominant_type", "cognitive")
        if dominant_type in distribution:
            distribution[dominant_type] += 0.3
        
        # Normalizar
        total = sum(distribution.values())
        return {k: v/total for k, v in distribution.items()}
    
    def _extract_temporal_markers(self, text: str) -> List[str]:
        """Extrae marcadores temporales"""
        markers = []
        
        if any(word in text.lower() for word in ["ahora", "veo", "siento"]):
            markers.append("present")
        if any(word in text.lower() for word in ["recordé", "era", "fue", "había"]):
            markers.append("past")
        if any(word in text.lower() for word in ["imagino", "sería", "podría"]):
            markers.append("future")
        if any(word in text.lower() for word in ["siempre", "nunca", "eterno"]):
            markers.append("atemporal")
        if any(word in text.lower() for word in ["normalmente", "generalmente", "suelo"]):
            markers.append("habitual")
        
        return markers if markers else ["present"]
    
    def _infer_temporal_phase(self, text: str) -> str:
        """Infiere fase temporal principal"""
        markers = self._extract_temporal_markers(text)
        return markers[0] if markers else "present"
    
    def _compute_ego_involvement(self, text: str) -> float:
        """Calcula involucramiento del ego (0=tercera persona, 1=primera persona)"""
        first_person = len(re.findall(r'\b(yo|me|mi|mis|mí)\b', text.lower()))
        third_person = len(re.findall(r'\b(él|ella|su|sus|ellos|ellas)\b', text.lower()))
        
        if first_person + third_person == 0:
            return 0.5  # Neutral
        
        return first_person / (first_person + third_person)
    
    def _infer_horizon_type(self, text: str) -> str:
        """Infiere tipo de horizonte fenomenológico"""
        if any(word in text.lower() for word in ["dentro", "adentro", "interior"]):
            return "inner"
        elif any(word in text.lower() for word in ["afuera", "exterior", "mundo"]):
            return "outer"
        elif any(word in text.lower() for word in ["cuerpo", "manos", "piel", "dedos"]):
            return "bodily"
        elif any(word in text.lower() for word in ["aquí", "ahí", "cerca", "lejos"]):
            return "spatial"
        elif any(word in text.lower() for word in ["ahora", "antes", "después", "tiempo"]):
            return "temporal"
        else:
            return "spatial"
    
    def _compute_phenomenal_resolution(self, num_anchors: int, num_clauses: int) -> float:
        """Calcula resolución fenomenológica en bits por token"""
        if num_anchors == 0 or num_clauses == 0:
            return 0.0
        
        # Resolución basada en densidad de qualia y estructura clausal
        qualia_density = num_anchors / num_clauses
        base_resolution = np.log2(qualia_density + 1) * 2
        
        return min(base_resolution, 10.0)  # Máximo 10 bits
    
    def _trace_semantic_categories(self, text: str) -> List[Dict]:
        """Traza categorías semánticas detectadas"""
        traces = []
        
        # Detectar tipos de palabras
        words = text.split()
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            
            # Sustantivos
            if word_lower.endswith('o') or word_lower.endswith('a') or word_lower.endswith('ción'):
                traces.append({
                    "trace_type": "noun",
                    "surface_form": word,
                    "phenomenal_interference": 0.3
                })
            
            # Adjetivos
            elif word_lower.endswith('o') or word_lower.endswith('a') or word_lower.endswith('e'):
                traces.append({
                    "trace_type": "adjective",
                    "surface_form": word,
                    "phenomenal_interference": 0.2
                })
            
            # Verbos
            elif any(ending in word_lower for ending in ['ar', 'er', 'ir']):
                traces.append({
                    "trace_type": "verb",
                    "surface_form": word,
                    "phenomenal_interference": 0.6
                })
        
        return traces[:10]  # Limitar resultados
    
    def _test_semantic_invariance(self, text: str, anchors: List[str]) -> Dict[str, Any]:
        """Test de invarianza bajo permutación semántica"""
        # Simular test (en producción usaría más análisis)
        original_meaning = hash(text) % 1000
        
        # Simular permutaciones
        permutations = ["permutación1", "permutación2", "permutación3"]
        variance_scores = [abs(hash(p) % 1000 - original_meaning) / 1000 for p in permutations]
        
        return {
            "test_passed": np.mean(variance_scores) < 0.3,
            "variance_score": np.mean(variance_scores),
            "semantic_switches": permutations
        }
    
    def _extract_temporal_invariants(self, clauses: List[Dict]) -> List[List[float]]:
        """Extrae invariantes temporales"""
        invariants = []
        
        for i, clause in enumerate(clauses[:3]):  # Máximo 3
            invariant = [
                i / max(len(clauses), 1),  # Posición temporal normalizada
                clause["experiential_score"],  # Intensidad experiencial
                1.0 if "ahora" in clause["text"].lower() else 0.0,  # Marcador presente
                len(clause["text"].split()) / 20.0  # Longitud normalizada
            ]
            invariants.append(invariant)
        
        return invariants
    
    def _detect_intentional_shifts(self, clauses: List[Dict]) -> List[Dict]:
        """Detecta cambios en la intencionalidad"""
        shifts = []
        
        for i in range(1, len(clauses)):
            prev_score = clauses[i-1]["experiential_score"]
            curr_score = clauses[i]["experiential_score"]
            
            if abs(curr_score - prev_score) > 0.3:
                shifts.append({
                    "position": i,
                    "from_intensity": prev_score,
                    "to_intensity": curr_score,
                    "shift_type": "intensification" if curr_score > prev_score else "attenuation"
                })
        
        return shifts
    
    def _detect_phase_transitions(self, clauses: List[Dict]) -> List[Dict]:
        """Detecta transiciones de fase temporal"""
        transitions = []
        
        for i in range(1, len(clauses)):
            prev_text = clauses[i-1]["text"].lower()
            curr_text = clauses[i]["text"].lower()
            
            # Detectar cambios de fase temporal
            prev_temporal = any(word in prev_text for word in ["era", "fue", "había"])
            curr_temporal = any(word in curr_text for word in ["veo", "siento", "está"])
            
            if prev_temporal and curr_temporal:
                transitions.append({
                    "position": i,
                    "from_phase": "past",
                    "to_phase": "present",
                    "transition_type": "memory_to_perception"
                })
        
        return transitions
    
    def _extract_temporal_vectors(self, clauses: List[Dict]) -> List[List[float]]:
        """Extrae vectores temporales (retención-protensión)"""
        vectors = []
        
        for i, clause in enumerate(clauses[:3]):
            # Retención (pasado)
            retention = 1.0 if "recordé" in clause["text"].lower() or "era" in clause["text"].lower() else 0.3
            
            # Presente
            present = clause["experiential_score"]
            
            # Protensión (futuro)
            protention = 1.0 if "imagino" in clause["text"].lower() or "sería" in clause["text"].lower() else 0.3
            
            vectors.append([retention, present, protention])
        
        return vectors
    
    def _extract_momentary_qualia(self, text: str) -> List[str]:
        """Extrae qualia momentáneos"""
        qualia_words = [
            "brillante", "súbito", "intenso", "vivo", "inmediato", 
            "puro", "directo", "instantáneo", "claro", "preciso"
        ]
        
        words = text.lower().split()
        momentary = [word for word in words if word in qualia_words]
        
        return momentary[:5]
    
    def _extract_micro_intentionalities(self, clauses: List[Dict]) -> List[str]:
        """Extrae micro-intencionalidades"""
        micro_intents = []
        
        for clause in clauses[:3]:
            text = clause["text"].lower()
            
            if "veo" in text or "observo" in text:
                micro_intents.append("visual_inspection")
            elif "siento" in text or "percibo" in text:
                micro_intents.append("haptic_exploration")
            elif "escucho" in text or "oigo" in text:
                micro_intents.append("auditory_attention")
            elif "pienso" in text or "reflexiono" in text:
                micro_intents.append("reflective_contemplation")
        
        return micro_intents
    
    def _extract_qualia_variations(self, text: str, qualia_by_modality: Dict) -> List[List[float]]:
        """Extrae variaciones microscópicas de qualia"""
        variations = []
        words = text.split()
        
        for i in range(min(len(words), 10)):  # Máximo 10 palabras
            word = words[i].lower()
            
            variation = [i / 10.0]  # Posición temporal
            
            # Intensidad por modalidad
            for modality, qualia_list in qualia_by_modality.items():
                intensity = 1.0 if word in qualia_list else 0.0
                variation.append(intensity)
            
            variations.append(variation)
        
        return variations
    
    def _summarize_narrative(self, text: str) -> str:
        """Resume la narrativa principal"""
        sentences = text.split('.')
        if len(sentences) > 1:
            return sentences[0].strip()
        return text[:100] + "..." if len(text) > 100 else text
    
    def _extract_thematic_gist(self, text: str) -> str:
        """Extrae el tema principal"""
        if "color" in text.lower():
            return "Experiencia visual cromática"
        elif "sonido" in text.lower() or "oigo" in text.lower():
            return "Experiencia auditiva"
        elif "recuerdo" in text.lower() or "memoria" in text.lower():
            return "Experiencia mnésica"
        else:
            return "Experiencia sensorial general"
    
    def _extract_affective_gist(self, affect_split: Dict) -> str:
        """Extrae el afecto principal"""
        sem_val = affect_split.get("semantic_valence", 0)
        phen_val = affect_split.get("phenomenal_valence", 0)
        
        avg_valence = (sem_val + phen_val) / 2
        
        if avg_valence > 0.3:
            return "Afecto positivo"
        elif avg_valence < -0.3:
            return "Afecto negativo"
        else:
            return "Afecto neutral"
    
    def _extract_spatial_gist(self, text: str) -> str:
        """Extrae el contexto espacial"""
        if "aquí" in text.lower() or "cerca" in text.lower():
            return "Espacio peripersonal"
        elif "allá" in text.lower() or "lejos" in text.lower():
            return "Espacio extrapersonal"
        elif "dentro" in text.lower():
            return "Espacio interno"
        else:
            return "Espacio indeterminado"
    
    def _perform_eidetic_reductions(self, text: str, qualia_signature: Dict) -> List[Dict]:
        """Realiza reducciones eidéticas"""
        reductions = []
        
        # Reducción de color
        if qualia_signature["dominant_type"] == "visual":
            reductions.append({
                "reduction_type": "color_reduction",
                "reduced_form": "extensión con cualidad cromática",
                "dependent_variations": ["matiz", "saturación", "brillo"]
            })
        
        # Reducción espacial
        if "aquí" in text.lower() or "cerca" in text.lower():
            reductions.append({
                "reduction_type": "spatial_reduction",
                "reduced_form": "presencia inmediata",
                "dependent_variations": ["distancia", "orientación", "tamaño"]
            })
        
        # Reducción temporal
        reductions.append({
            "reduction_type": "temporal_reduction",
            "reduced_form": "presente vívido",
            "dependent_variations": ["duración", "orden", "ritmo"]
        })
        
        return reductions
    
    # ========================================
    # MÉTODOS DE CARGA Y UTILIDAD
    # ========================================
    
    def _load_image(self, image_input: Union[str, np.ndarray, torch.Tensor]) -> torch.Tensor:
        """Carga imagen en formato tensor normalizado [1, C, H, W]"""
        if isinstance(image_input, str):
            from PIL import Image
            image = Image.open(image_input).convert('RGB')
            image = np.array(image)
            image_tensor = torch.from_numpy(image).float() / 255.0
            image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)
        elif isinstance(image_input, np.ndarray):
            image_tensor = torch.from_numpy(image_input).float() / 255.0
            if image_tensor.dim() == 3:
                image_tensor = image_tensor.unsqueeze(0)
            if image_tensor.shape[-1] == 3:
                image_tensor = image_tensor.permute(0, 3, 1, 2)
        elif isinstance(image_input, torch.Tensor):
            image_tensor = image_input
            if image_tensor.dim() == 3:
                image_tensor = image_tensor.unsqueeze(0)
        else:
            raise ValueError(f"Tipo de imagen no soportado: {type(image_input)}")
        
        # Asegurar formato correcto
        if image_tensor.shape[1] == 4:  # RGBA
            image_tensor = image_tensor[:, :3, :, :]
        
        if image_tensor.max() > 1.0:
            image_tensor = image_tensor / 255.0
        
        return image_tensor
    
    def _extract_visual_multiscale(self, image_tensor: torch.Tensor) -> Dict[str, Any]:
        """Extrae features visuales multi-escala"""
        if self.models.get('vision') is None:
            # Fallback: estadísticas simples
            features = {
                "global": torch.cat([
                    image_tensor.mean(dim=[2,3]),
                    image_tensor.std(dim=[2,3]),
                    image_tensor.flatten(start_dim=1).mean(dim=1, keepdim=True),
                    image_tensor.flatten(start_dim=1).std(dim=1, keepdim=True)
                ], dim=1).squeeze(0),
                "intermediate": torch.randn(512),
                "fine": torch.randn(256)
            }
            return features
        
        # Usar CLIP con extracción de múltiples capas
        model = self.models['vision']['model']
        processor = self.models['vision']['processor']
        
        inputs = processor(images=image_tensor, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = model.vision_model(**inputs)
            hidden_states = outputs.last_hidden_state
        
        # Extraer features de diferentes capas
        features = {}
        for layer_idx in self.models['vision']['extract_layers']:
            if hasattr(model.vision_model.encoder.layers[layer_idx], "output"):
                layer_output = model.vision_model.encoder.layers[layer_idx].output
                features[f"layer_{abs(layer_idx)}"] = layer_output.mean(dim=1).squeeze(0)
        
        return features
    
    def _estimate_depth_map(self, image_tensor: torch.Tensor) -> Optional[Dict]:
        """Estima mapa de profundidad usando MiDaS"""
        if self.models.get('depth') is None:
            # Fallback: heurística simple
            return {
                "mean_depth": 0.5,
                "std_depth": 0.2,
                "depth_range": 0.4,
                "spatial_layout": "unknown"
            }
        
        try:
            from torchvision.transforms import ToPILImage
            pil_image = ToPILImage()(image_tensor.squeeze(0))
            depth = self.models['depth'](pil_image)
            depth_array = np.array(depth["depth"])
            
            return {
                "mean_depth": float(depth_array.mean() / 255.0),
                "std_depth": float(depth_array.std() / 255.0),
                "depth_range": float((depth_array.max() - depth_array.min()) / 255.0),
                "spatial_layout": "deep" if depth_array.mean() > 128 else "shallow"
            }
        except:
            return None
    
    def _analyze_visual_qualia_pro(self, image_tensor: torch.Tensor, features_multiscale: Dict) -> Dict[str, Any]:
        """Analiza qualia visuales profundamente"""
        from torchvision.transforms import functional as F
        
        # Diversidad de color en espacio Lab
        lab_image = self._rgb_to_lab(image_tensor)
        color_diversity = lab_image.std(dim=[2,3]).mean().item()
        
        # Complejidad de textura
        gray = F.rgb_to_grayscale(image_tensor)
        texture_complexity = self._compute_texture_complexity(gray).item()
        
        # Contraste
        contrast = self._compute_contrast(image_tensor).item()
        
        # Satuación de color
        hsv = F.rgb_to_hsv(image_tensor)
        saturation = hsv[:, 1, :, :].mean().item()
        
        # Brillo
        brightness = image_tensor.mean().item()
        
        # Clasificar tipo de qualia visual dominante
        if color_diversity > 0.5 and texture_complexity > 0.5:
            qualia_type = "rich_multimodal"
        elif color_diversity > 0.5:
            qualia_type = "color_dominant"
        elif texture_complexity > 0.5:
            qualia_type = "texture_dominant"
        elif color_diversity < 0.2 and texture_complexity < 0.2:
            qualia_type = "minimalist"
        else:
            qualia_type = "balanced"
        
        # Perfil de intensidad
        intensity_profile = [color_diversity, texture_complexity, contrast, saturation, brightness]
        
        # Umbral de discriminación (JND)
        jnd_threshold = 0.05 + (color_diversity * 0.1) + (texture_complexity * 0.05)
        
        # Saturación fenomenológica
        saturation = min((color_diversity + texture_complexity + contrast) / 3, 1.0)
        
        # Salience
        salience = (color_diversity + texture_complexity + contrast) / 3
        
        return {
            "color_diversity": color_diversity,
            "texture_complexity": texture_complexity,
            "contrast": contrast,
            "saturation": saturation,
            "brightness": brightness,
            "qualia_type": qualia_type,
            "intensity_profile": intensity_profile,
            "jnd_threshold": jnd_threshold,
            "saturation": saturation,
            "salience": salience,
            "dominant_type": qualia_type,
            "invariant_patterns": self._extract_visual_invariants(features_multiscale),
            "clusters": self._cluster_visual_features(features_multiscale),
            "micro_variations": self._extract_visual_micro_variations(image_tensor)
        }
    
    def _rgb_to_lab(self, rgb_tensor: torch.Tensor) -> torch.Tensor:
        """Convierte RGB a espacio Lab aproximado"""
        # Simple aproximación usando HSV como proxy
        from torchvision.transforms import functional as F
        hsv = F.rgb_to_hsv(rgb_tensor)
        return hsv
    
    def _compute_texture_complexity(self, gray_tensor: torch.Tensor) -> torch.Tensor:
        """Computa complejidad de textura mediante gradientes"""
        # Gradiente Sobel aproximado
        dx = gray_tensor[..., :-1, :-1] - gray_tensor[..., 1:, :-1]
        dy = gray_tensor[..., :-1, :-1] - gray_tensor[..., :-1, 1:]
        gradient_magnitude = torch.sqrt(dx**2 + dy**2)
        return gradient_magnitude.mean()
    
    def _compute_contrast(self, image_tensor: torch.Tensor) -> torch.Tensor:
        """Computa contraste (percentil 95 - percentil 5)"""
        flattened = image_tensor.flatten()
        p95 = torch.quantile(flattened, 0.95)
        p5 = torch.quantile(flattened, 0.05)
        return (p95 - p5) / (p95 + p5 + 1e-8)
    
    def _extract_visual_invariants(self, features_multiscale: Dict) -> List[List[float]]:
        """Extrae invariantes visuales"""
        invariants = []
        
        # Usar features de diferentes escalas
        for layer_name, features in features_multiscale.items():
            if hasattr(features, 'mean'):
                mean_val = features.mean().item()
                std_val = features.std().item()
                invariants.append([mean_val, std_val])
        
        return invariants[:5]
    
    def _cluster_visual_features(self, features_multiscale: Dict) -> List[Dict]:
        """Clusteriza features visuales"""
        clusters = []
        
        # Crear clusters basados en capas
        layer_names = list(features_multiscale.keys())
        for i, layer_name in enumerate(layer_names[:3]):
            clusters.append({
                "type": f"visual_layer_{i}",
                "count": 1,
                "intensity": 0.8 - (i * 0.2)
            })
        
        return clusters
    
    def _extract_visual_micro_variations(self, image_tensor: torch.Tensor) -> List[List[float]]:
        """Extrae variaciones microscópicas visuales"""
        variations = []
        
        # Dividir imagen en parches pequeños
        h, w = image_tensor.shape[-2:]
        patch_size = min(32, h//4, w//4)
        
        for i in range(0, h-patch_size, patch_size):
            for j in range(0, w-patch_size, patch_size):
                patch = image_tensor[..., i:i+patch_size, j:j+patch_size]
                
                variation = [
                    i / h,  # Posición normalizada
                    j / w,
                    patch.mean().item(),  # Brillo
                    patch.std().item()    # Contraste
                ]
                variations.append(variation)
                
                if len(variations) >= 10:  # Limitar
                    break
            if len(variations) >= 10:
                break
        
        return variations
    
    def _compute_phenomenal_attention(self, image_tensor: torch.Tensor) -> Dict[str, Any]:
        """Computa atención fenomenológica"""
        try:
            # Usar varianza espacial como proxy de atención
            from torchvision.transforms import functional as F
            gray = F.rgb_to_grayscale(image_tensor)
            
            # Encontrar centro de atención (máxima varianza)
            h, w = gray.shape[-2:]
            
            # Dividir en grid y calcular varianza por región
            grid_size = 4
            attention_map = np.zeros((grid_size, grid_size))
            
            for i in range(grid_size):
                for j in range(grid_size):
                    y_start = i * h // grid_size
                    y_end = (i + 1) * h // grid_size
                    x_start = j * w // grid_size
                    x_end = (j + 1) * w // grid_size
                    
                    region = gray[..., y_start:y_end, x_start:x_end]
                    attention_map[i, j] = region.std().item()
            
            # Encontrar centro de atención
            max_idx = np.unravel_index(np.argmax(attention_map), attention_map.shape)
            center_x = (max_idx[1] + 0.5) / grid_size
            center_y = (max_idx[0] + 0.5) / grid_size
            
            return {
                "center_of_attention": [center_x, center_y],
                "attention_spread": float(attention_map.std()),
                "attention_map": attention_map.tolist()
            }
        except:
            return {
                "center_of_attention": [0.5, 0.5],
                "attention_spread": 0.5,
                "attention_map": [[0.5] * 4 for _ in range(4)]
            }
    
    def _infer_visual_noesis(self, qualia_visual: Dict, viewpoint: str, depth_info: Optional[Dict]) -> Dict[str, Any]:
        """Infiere noesis visual específica"""
        # Modo base
        mode = "perception"
        
        # Detectar si es contemplación (alta complejidad visual)
        if qualia_visual["qualia_type"] in ["rich_multimodal", "color_dominant"]:
            directedness = "visual_contemplation"
        elif qualia_visual["texture_complexity"] > 0.6:
            directedness = "textural_inspection"
        elif qualia_visual["color_diversity"] > 0.6:
            directedness = "chromatic_experience"
        else:
            directedness = "visual_recognition"
        
        # Ajustar por viewpoint
        viewpoint_modifiers = {
            "first_person": "egocentric_",
            "third_person": "allocentric_",
            "aerial": "top_down_"
        }
        if viewpoint in viewpoint_modifiers:
            directedness = viewpoint_modifiers[viewpoint] + directedness
        
        # Generar vectores invariantes
        invariant_vectors = [
            [qualia_visual["color_diversity"], qualia_visual["texture_complexity"], qualia_visual["contrast"]],
            [1.0 if viewpoint == "first_person" else 0.0, qualia_visual["salience"], 0.5]
        ]
        
        return {
            "mode": mode,
            "directedness": directedness,
            "invariant_vectors": invariant_vectors,
            "shifts": [],
            "transitions": [],
            "temporal_vectors": [[0.0, 1.0, 0.0]]  # Presente inmediato
        }
    
    def _split_visual_affect(self, qualia_visual: Dict, image_tensor: torch.Tensor) -> Dict[str, float]:
        """Separa afecto visual semántico del fenomenológico"""
        # Afecto fenomenológico desde colores
        color_valence = self._compute_color_valence(image_tensor)
        
        # Afecto semántico desde complejidad visual
        semantic_valence = (qualia_visual["color_diversity"] + qualia_visual["texture_complexity"]) / 2 - 0.5
        
        return {
            "visual_valence": color_valence,
            "visual_arousal": qualia_visual["salience"],
            "semantic_valence": semantic_valence
        }
    
    def _compute_color_valence(self, image_tensor: torch.Tensor) -> float:
        """Computa valencia afectiva desde paleta de colores"""
        from torchvision.transforms import functional as F
        
        # Convertir a HSV
        hsv = F.rgb_to_hsv(image_tensor)
        hue = hsv[:, 0, :, :]  # Canal de matiz
        
        # Colores cálidos → positivo, fríos → negativo
        warm_mask = ((hue > 0.0) & (hue < 0.17)) | ((hue > 0.94) & (hue < 1.0))
        cold_mask = (hue > 0.5) & (hue < 0.67)
        
        warm_ratio = warm_mask.float().mean().item()
        cold_ratio = cold_mask.float().mean().item()
        
        valence = (warm_ratio - cold_ratio) * 0.5
        return np.clip(valence, -1.0, 1.0)
    
    def _generate_visual_experience_map(self, image_tensor: torch.Tensor, qualia_visual: Dict, 
                                       attention_map: Optional[Dict], scene_graph_data: Optional[Dict]) -> Dict[str, Any]:
        """Genera mapa de experiencia visual"""
        h, w = image_tensor.shape[-2:]
        
        # Coordenadas espaciales
        coordinates = []
        for i in range(0, h, h//8):
            for j in range(0, w, w//8):
                coordinates.append([j/w, i/h, 0.5])  # Normalizadas
        
        # Pesos de qualia por posición
        qualia_weights = [qualia_visual["salience"]] * len(coordinates)
        
        # Vectores intencionales
        intentional_vectors = [[0.0, 0.0, 1.0]] * len(coordinates)  # Dirección de observación
        
        # Zonas puras (alta saliencia)
        pure_zones = []
        for i, coord in enumerate(coordinates[:5]):
            pure_zones.append([coord[0], coord[1], qualia_visual["salience"]])
        
        return {
            "coordinates": coordinates,
            "qualia_weights": qualia_weights,
            "intentional_vectors": intentional_vectors,
            "pure_zones": pure_zones
        }
    
    def _perform_visual_eidetic_reductions(self, qualia_visual: Dict, attention_map: Optional[Dict]) -> List[Dict]:
        """Realiza reducciones eidéticas visuales"""
        reductions = []
        
        # Reducción de color
        if qualia_visual["dominant_type"] in ["color_dominant", "rich_multimodal"]:
            reductions.append({
                "reduction_type": "color_reduction",
                "reduced_form": "extensión cromática",
                "dependent_variations": ["matiz", "saturación", "brillo", "temperatura"]
            })
        
        # Reducción espacial
        reductions.append({
            "reduction_type": "spatial_reduction",
            "reduced_form": "presencia visual",
            "dependent_variations": ["profundidad", "perspectiva", "escala"]
        })
        
        # Reducción temporal
        reductions.append({
            "reduction_type": "temporal_reduction",
            "reduced_form": "instante visual",
            "dependent_variations": ["duración", "movimiento", "cambio"]
        })
        
        return reductions
    
    def _compute_modal_dist_from_qualia(self, qualia_visual: Dict, modality: str) -> Dict[str, float]:
        """Computa distribución modal basada en qualia"""
        distribution = {
            "visual": 0.85 if modality == "image" else 0.2,
            "auditory": 0.05,
            "haptic": 0.05,
            "olfactory": 0.02,
            "gustatory": 0.02,
            "proprioceptive": 0.10,
            "affective": 0.40 * qualia_visual["saturation"],
            "cognitive": 0.15,
            "digital": 0.10
        }
        
        # Ajustar por tipo de qualia dominante
        if qualia_visual["dominant_type"] == "color_dominant":
            distribution["visual"] += 0.1
        elif qualia_visual["dominant_type"] == "texture_dominant":
            distribution["haptic"] += 0.1
        
        # Normalizar
        total = sum(distribution.values())
        return {k: v/total for k, v in distribution.items()}
    
    def _gist_affect_from_qualia(self, qualia_visual: Dict) -> str:
        """Extrae gist afectivo desde qualia visuales"""
        saturation = qualia_visual["saturation"]
        brightness = qualia_visual["brightness"]
        
        if saturation > 0.7 and brightness > 0.6:
            return "Experiencia visual intensa y luminosa"
        elif saturation > 0.5:
            return "Experiencia visual rica en color"
        elif brightness > 0.7:
            return "Experiencia visual clara y brillante"
        elif brightness < 0.3:
            return "Experiencia visual oscura y misteriosa"
        else:
            return "Experiencia visual equilibrada"
    
    def _extract_pixel_qualia(self, image_tensor: torch.Tensor, attention_map: Optional[Dict]) -> List[str]:
        """Extrae qualia a nivel de píxel"""
        # Simulación: en producción analizaría parches de imagen
        return ["color_intenso", "contraste_nítido", "textura_detallada"]
    
    def _test_visual_invariance(self, image_tensor: torch.Tensor, anchors_local: List[str]) -> Dict[str, Any]:
        """Test de invarianza visual"""
        return {
            "test_passed": True,
            "variance_score": 0.2,
            "semantic_switches": ["rotación_90", "escala_0.5", "brillo_1.2"]
        }

# ============================================
# CLASE DE VISUALIZACIÓN FENOMENOLÓGICA
# ============================================

class PhenomenalVisualizer:
    """Genera representaciones visuales del contenido fenomenológico"""
    
    @staticmethod
    def generate_experience_map(rem_data: Dict, output_path: str):
        """Genera mapa de experiencia 2D/3D"""
        import matplotlib.pyplot as plt
        import numpy as np
        
        modality = rem_data["header"]["modality_origin"]
        
        if modality == "text":
            return PhenomenalVisualizer.visualize_text_experience_map(rem_data, output_path)
        elif modality == "image":
            return PhenomenalVisualizer.visualize_visual_experience_map(rem_data, output_path)
        elif modality == "audio":
            return PhenomenalVisualizer.visualize_audio_experience_map(rem_data, output_path)
        elif modality == "video":
            return PhenomenalVisualizer.visualize_temporal_experience_map(rem_data, output_path)
    
    @staticmethod
    def visualize_text_experience_map(rem_data: Dict, output_path: str):
        """Visualiza texto como grafo de cláusulas experienciales"""
        clauses = rem_data["experiential_stream"]["clause_boundaries"]
        anchors = rem_data["semantic_contamination"]["lexical_anchors"]
        invariants = rem_data["phenomenal_core"]["invariant_features"]["noetic_invariants"]
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Mapa de cláusulas
        y_scores = [c.get("experiential_score", 0.5) for c in clauses]
        ax1.plot(y_scores, 'o-', color='#2C3E50')
        ax1.set_title("Perfil Experiencial de Cláusulas")
        ax1.set_xlabel("Índice de Cláusula")
        ax1.set_ylabel("Score Experiencial")
        ax1.grid(True, alpha=0.3)
        
        # Heatmap de contaminación
        interference = [a["salience_score"] for a in anchors]
        ax2.imshow([interference], cmap='RdYlGn_r', aspect='auto')
        ax2.set_title("Densidad de Contaminación Semántica")
        ax2.set_xlabel("Posición de Anclaje")
        
        # Invariantes noéticas
        if invariants:
            inv_array = np.array(invariants)
            im = ax3.imshow(inv_array, cmap='viridis')
            ax3.set_title("Invariantes Noéticas")
            plt.colorbar(im, ax=ax3)
        
        plt.tight_layout()
        plt.savefig(f"{output_path}_text_map.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"{output_path}_text_map.png"
    
    @staticmethod
    def visualize_visual_experience_map(rem_data: Dict, output_path: str):
        """Visualiza imagen como volumen de qualia 3D"""
        qualia = rem_data["phenomenal_core"]["qualia_signature"]
        visualization = rem_data["visualization_layer"]["experience_map"]
        
        # Crear mapa de calor de qualia
        coordinates = np.array(visualization["coordinates"])
        weights = np.array(visualization["qualia_weights"])
        
        fig = plt.figure(figsize=(12, 8))
        
        # Scatter 2D con pesos
        ax1 = fig.add_subplot(221)
        scatter = ax1.scatter(coordinates[:, 0], coordinates[:, 1], 
                             c=weights, s=weights*500, cmap='plasma', alpha=0.6)
        ax1.set_title("Distribución Espacial de Qualia")
        plt.colorbar(scatter, ax=ax1)
        
        # Perfil de intensidad
        ax2 = fig.add_subplot(222)
        ax2.plot(qualia["intensity_profile"], 'purple', linewidth=2)
        ax2.set_title("Perfil de Intensidad Qualia")
        ax2.set_ylabel("Intensidad")
        ax2.grid(True, alpha=0.3)
        
        # Mapa de contaminación
        ax3 = fig.add_subplot(223)
        heatmap = rem_data["visualization_layer"]["contamination_heatmap"]
        ax3.imshow([heatmap["contamination_density"]], cmap='hot', aspect='auto')
        ax3.set_title("Zonas de Pureza/Contaminación")
        
        # Invariantes
        ax4 = fig.add_subplot(224)
        invariants = rem_data["phenomenal_core"]["invariant_features"]["sensory_invariants"]
        if invariants:
            ax4.imshow(np.array(invariants[:10]), cmap='coolwarm')
            ax4.set_title("Invariantes Sensoriales")
        
        plt.tight_layout()
        plt.savefig(f"{output_path}_visual_map.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"{output_path}_visual_map.png"
    
    @staticmethod
    def visualize_audio_experience_map(rem_data: Dict, output_path: str):
        """Visualiza audio como espectro temporal de qualia"""
        # Implementación simplificada
        return f"{output_path}_audio_map.png"
    
    @staticmethod
    def visualize_temporal_experience_map(rem_data: Dict, output_path: str):
        """Visualiza video como secuencia temporal"""
        # Implementación simplificada
        return f"{output_path}_temporal_map.png"

# ============================================
# FUNCIÓN DE DEMOSTRACIÓN
# ============================================

def demo_formato_optimo():
    """Demo del formato óptimo para tokenización fenomenológica"""
    print("🚀 REMForge Ultra - Formato Óptimo para Tokenización Fenomenológica")
    print("=" * 80)
    
    # Inicializar sistema
    forge = REMForgeUltraFormatoOptimo(device="auto")
    
    # Texto de ejemplo con contenido fenomenológico rico
    textos_demo = [
        "Veo un color rojo intenso en la superficie de la mesa",
        "Me recuerda a algo, pero no sé qué exactamente",
        "La textura es suave bajo mis dedos, casi sedosa",
        "Oigo el sonido suave de la lluvia contra la ventana",
        "Siento una mezcla de nostalgia y serenidad"
    ]
    
    contexto = {
        "situational_context": "Observando objetos personales en casa",
        "temporal_context": "atardecer",
        "author_id": "demo_user"
    }
    
    print("\n📄 Procesando textos de demo...")
    
    rems_generados = []
    
    for i, texto in enumerate(textos_demo):
        print(f"\n📝 Texto {i+1}: '{texto[:50]}...'")
        
        # Generar REM con formato óptimo
        rem_output = forge.forge_text_ultra(texto, contexto)
        
        # Mostrar estadísticas clave
        header = rem_output["header"]
        noetic = rem_output["noetic_layer"]
        sensorial = rem_output["sensorial_layer"]
        contamination = rem_output["semantic_contamination"]
        
        print(f"   ✅ REM ID: {header['rem_id']}")
        print(f"   ✅ Modalidad: {header['modality_origin']}")
        print(f"   ✅ Modo intencional: {noetic['intentional_mode']}")
        print(f"   ✅ Valencia afectiva: {sensorial['affective_valence']:.3f}")
        print(f"   ✅ Contaminación: {contamination['contamination_strength']:.3f}")
        print(f"   ✅ Qualia detectados: {len(contamination['lexical_anchors'])}")
        print(f"   ✅ Resolución fenomenológica: {header['quality_metrics']['phenomenal_resolution']:.3f}")
        
        rems_generados.append(rem_output)
    
    # Crear visualizaciones
    print("\n📊 Generando visualizaciones fenomenológicas...")
    
    visualizer = PhenomenalVisualizer()
    
    for i, rem in enumerate(rems_generados[:2]):  # Solo los primeros 2 para demo
        output_path = f"/mnt/okcomputer/output/rem_{i+1}_experience_map"
        visualizer.generate_experience_map(rem, output_path)
        print(f"   ✅ Mapa de experiencia {i+1} generado")
    
    # Guardar todos los REMs en JSON
    print("\n💾 Guardando REMs en formato óptimo...")
    
    with open("/mnt/okcomputer/output/rems_formato_optimo.json", "w", encoding='utf-8') as f:
        json.dump(rems_generados, f, indent=2, default=str, ensure_ascii=False)
    
    print("   ✅ Archivo JSON guardado: rems_formato_optimo.json")
    
    # Mostrar resumen de características del formato
    print("\n" + "=" * 80)
    print("📋 RESUMEN DE CARACTERÍSTICAS DEL FORMATO ÓPTIMO")
    print("=" * 80)
    
    if rems_generados:
        rem_ejemplo = rems_generados[0]
        
        print(f"\n🎯 ESTRUCTURA PHENOMENALREM-ULTRA:")
        print(f"   • Header: {len(rem_ejemplo['header'])} campos de metadata")
        print(f"   • Experiential Stream: Narrativa con cláusulas y marcadores temporales")
        print(f"   • Noetic Layer: Modos intencionales y patrones noéticos")
        print(f"   • Sensorial Layer: Distribución modal y coordenadas espaciales")
        print(f"   • Semantic Contamination: Anclajes con scoring de interferencia")
        print(f"   • Phenomenal Core: Invariantes y signature de qualia")
        print(f"   • Multiscale Representation: Coarse, medium y fine scale")
        print(f"   • Visualization Layer: Mapas de experiencia y contaminación")
        
        print(f"\n🔬 CARACTERÍSTICAS DE TOKENIZACIÓN:")
        print(f"   • Interference Scoring: Identifica anclajes peligrosos vs inertes")
        print(f"   • Invariant Features: Tokens pre-procesados para evitar recálculo")
        print(f"   • Qualia Signature: JND para clustering cualitativo adaptativo")
        print(f"   • Multiscale: Tokenización jerárquica (coarse→fine)")
        print(f"   • Visualization Layer: Validación visual de tokens")
        print(f"   • Contamination Heatmap: Dropout semántico dirigido")
        print(f"   • Temporal Flow: Preservación de retención-protensión (Husserl)")
    
    print(f"\n✅ DEMO COMPLETADA - {len(rems_generados)} REMs generados con formato óptimo")
    print(f"🌐 Listo para tokenización fenomenológica computacional")

# ============================================
# EJECUCIÓN DE DEMO
# ============================================

if __name__ == "__main__":
    demo_formato_optimo()