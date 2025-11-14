# -*- coding: utf-8 -*-
"""
REMForge Lite: An optimized version of REMForge Ultra for low-spec systems.

This version uses lighter models to ensure compatibility with systems with limited resources (e.g., i5 CPU, 8GB RAM).
"""

import json
import os
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
from PIL import Image
import torch
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from torchvision import transforms
from torchvision.models import mobilenet_v2
import librosa

# ============================================
# REMForge Lite System
# ============================================

class REMForgeLite:
    """A lightweight version of REMForge for phenomenological data conversion."""

    def __init__(self, config: Optional[Dict] = None, device: str = "cpu"):
        """Initializes the REMForge Lite system.

        Args:
            config (Optional[Dict]): A configuration dictionary for models.
            device (str): The device to run the models on ('cpu' or 'cuda').
        """
        self.device = device
        self.config = config or self._get_default_config()
        self.models = {}
        print(f"REMForge Lite initialized on device: {self.device}")

        self._load_models()

    def _get_default_config(self) -> Dict:
        """Returns the default model configuration."""
        return {
            "text": {
                "spacy_model": "en_core_web_sm",
                "sentiment_model": "distilbert-base-uncased-finetuned-sst-2-english"
            },
            "vision": {
                "model_name": "mobilenet_v2",
                "pretrained": True
            }
        }

    def _load_models(self):
        """Loads the lightweight models required for analysis based on the config."""
        print("Loading lightweight models...")

        # Text analysis
        try:
            spacy_model = self.config['text']['spacy_model']
            self.models['nlp'] = spacy.load(spacy_model)
            print(f"  - spaCy model '{spacy_model}' loaded.")
        except OSError:
            print(f"  - spaCy model not found. Please run: python -m spacy download {self.config['text']['spacy_model']}")
            self.models['nlp'] = None
        except Exception as e:
            print(f"  - Error loading spaCy model: {e}")
            self.models['nlp'] = None

        try:
            sentiment_model = self.config['text']['sentiment_model']
            self.models['sentiment'] = pipeline("sentiment-analysis", model=sentiment_model, device=self.device)
            print(f"  - Sentiment analysis model '{sentiment_model}' loaded.")
        except Exception as e:
            print(f"  - Could not load sentiment analysis model: {e}")
            self.models['sentiment'] = None

        # Vision analysis
        try:
            if self.config['vision']['model_name'] == 'mobilenet_v2':
                self.models['vision'] = mobilenet_v2(pretrained=self.config['vision']['pretrained']).to(self.device)
                self.models['vision'].eval()
                self.models['vision_transform'] = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                ])
                print("  - Vision model 'MobileNetV2' loaded.")
            else:
                print(f"  - Vision model '{self.config['vision']['model_name']}' not supported.")
        except Exception as e:
            print(f"  - Could not load vision model: {e}")
            self.models['vision'] = None

        # Audio analysis
        print("  - Audio analysis enabled via Librosa.")

    def _generate_rem_header(self, modality: str, context: Dict) -> Dict:
        """Generates the header for a REM file."""
        return {
            "rem_id": f"rem_{uuid.uuid4()}",
            "schema_version": "PhenomenalREM-Lite-1.0.0",
            "timestamp_created": datetime.utcnow().isoformat() + "Z",
            "modality_origin": modality,
            "context": context,
            "quality_metrics": {}
        }

    def _create_base_rem_structure(self, header: Dict) -> Dict:
        """Creates the basic dictionary structure for a REM."""
        return {
            "header": header,
            "experiential_stream": {},
            "noetic_layer": {},
            "sensorial_layer": {},
            "semantic_contamination": {},
            "phenomenal_core": {},
            "visualization_layer": {}
        }

    def forge_text(self, text: str, context: Optional[Dict] = None) -> Dict:
        """Converts a text string into a PhenomenalREM-Lite object.

        Args:
            text (str): The input text to analyze.
            context (Optional[Dict]): Additional context for the analysis.

        Returns:
            Dict: A dictionary representing the PhenomenalREM-Lite object.
        """
        header = self._generate_rem_header("text", context or {})
        rem = self._create_base_rem_structure(header)

        # 1. Experiential Stream
        rem["experiential_stream"] = {
            "raw_text": text,
            "clauses": self._analyze_clausal_structure(text)
        }

        # 2. Noetic, Sensorial, and Affective Analysis
        if self.models.get('nlp'):
            doc = self.models['nlp'](text)
            rem["noetic_layer"] = self._analyze_noetic_aspects(doc)
            rem["sensorial_layer"] = self._analyze_sensorial_aspects(doc)

        if self.models.get('sentiment'):
            try:
                sentiment = self.models['sentiment'](text)[0]
                valence = sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score']
                rem['sensorial_layer']['affective_valence'] = valence
            except Exception as e:
                print(f"Could not compute sentiment: {e}")

        # 3. Semantic Contamination
        rem["semantic_contamination"] = self._analyze_semantic_contamination(text)

        # 4. Phenomenal Core
        lexical_anchors = rem["semantic_contamination"].get("lexical_anchors", [])
        rem["phenomenal_core"] = {
            "invariant_features": [anchor.get("text") for anchor in lexical_anchors],
            "qualia_signature": self._build_linguistic_qualia_signature(lexical_anchors)
        }

        # 5. Quality Metrics
        rem['header']['quality_metrics']['phenomenal_resolution'] = np.random.rand()  # Placeholder

        return rem

    def _analyze_clausal_structure(self, text: str) -> List[Dict[str, Any]]:
        """Analyzes the clausal structure of a text using simple punctuation-based splitting.

        Args:
            text (str): The text to analyze.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a clause.
        """
        clauses = re.split(r'[,.;:!?]', text)
        result = []
        for c in clauses:
            if c.strip():
                start_char = text.find(c)
                result.append({
                    'clause_text': c.strip(),
                    'start_char': start_char,
                    'end_char': start_char + len(c)
                })
        return result

    def _analyze_noetic_aspects(self, doc) -> Dict[str, Any]:
        """Analyzes noetic aspects using spaCy's linguistic features.

        Args:
            doc: A spaCy Doc object.

        Returns:
            Dict[str, Any]: A dictionary of noetic aspects.
        """
        num_verbs = len([token for token in doc if token.pos_ == "VERB"])
        num_nouns = len([token for token in doc if token.pos_ == "NOUN"])
        
        # A simple heuristic for intentional mode
        intentional_mode = "active" if num_verbs > num_nouns else "contemplative"
        
        # A simple heuristic for ego involvement
        ego_pronouns = len([token for token in doc if token.lemma_ in ["I", "me", "my", "mine"]])
        ego_involvement = min(1.0, ego_pronouns / 10.0) # Normalize

        return {
            "intentional_mode": intentional_mode,
            "ego_involvement": ego_involvement
        }

    def _analyze_sensorial_aspects(self, doc) -> Dict[str, Any]:
        """Analyzes sensorial aspects using keyword matching.

        Args:
            doc: A spaCy Doc object.

        Returns:
            Dict[str, Any]: A dictionary of sensorial aspects.
        """
        # More comprehensive keyword lists
        keywords = {
            "visual": ["see", "look", "watch", "red", "blue", "green", "bright", "dark", "color", "light"],
            "audio": ["hear", "sound", "listen", "loud", "quiet", "noise", "voice", "music"],
            "somatic": ["feel", "touch", "heavy", "light", "warm", "cold", "texture", "pressure"],
            "olfactory": ["smell", "scent", "aroma", "fragrance"],
            "gustatory": ["taste", "flavor", "sweet", "sour"]
        }

        modality_counts = {modality: 0 for modality in keywords}
        for token in doc:
            for modality, kws in keywords.items():
                if token.lemma_ in kws:
                    modality_counts[modality] += 1
        
        total = sum(modality_counts.values())
        modality_distribution = {m: c / (total + 1e-6) for m, c in modality_counts.items()}

        return {"modality_distribution": modality_distribution}

    def _analyze_semantic_contamination(self, text: str) -> Dict[str, Any]:
        """Analyzes semantic contamination using keyword matching.

        Args:
            text (str): The text to analyze.

        Returns:
            Dict[str, Any]: A dictionary of semantic contamination aspects.
        """
        conceptual_keywords = ["think", "believe", "know", "understand", "idea", "concept", "meaning", "purpose"]
        anchors = []
        for match in re.finditer(r'\b(' + '|'.join(conceptual_keywords) + r')\b', text, re.IGNORECASE):
            anchors.append({
                "text": match.group(0),
                "span": [match.start(), match.end()],
                "salience_score": np.random.rand()  # Placeholder
            })
        
        contamination_strength = len(anchors) / (len(text.split()) + 1e-6)

        return {
            "contamination_strength": contamination_strength,
            "lexical_anchors": anchors
        }

    def _build_linguistic_qualia_signature(self, anchors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Builds a simplified qualia signature from lexical anchors.

        Args:
            anchors (List[Dict[str, Any]]): A list of lexical anchors.

        Returns:
            Dict[str, Any]: A dictionary representing the linguistic qualia signature.
        """
        if not anchors:
            return {"complexity": 0, "intensity": 0}
        
        intensity = np.mean([a.get('salience_score', 0) for a in anchors])
        return {"complexity": len(anchors), "intensity": float(intensity)}

    def forge_image(self, image_path: str, context: Optional[Dict] = None) -> Dict:
        """Converts an image file into a PhenomenalREM-Lite object.

        Args:
            image_path (str): The path to the image file.
            context (Optional[Dict]): Additional context for the analysis.

        Returns:
            Dict: A dictionary representing the PhenomenalREM-Lite object.
        """
        header = self._generate_rem_header("image", context or {})
        rem = self._create_base_rem_structure(header)

        if not self.models.get('vision'):
            print("Vision model not loaded. Skipping image analysis.")
            return rem

        try:
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.models['vision_transform'](image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                features = self.models['vision'](image_tensor)

            # Simplified analysis based on model output
            rem['sensorial_layer']['affective_valence'] = features.mean().item()  # Placeholder
            rem['phenomenal_core']['qualia_signature'] = self._analyze_visual_qualia(image)
            rem['header']['quality_metrics']['clarity_score'] = features.std().item() # Placeholder

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

        return rem

    def _analyze_visual_qualia(self, image: Image.Image) -> Dict:
        """Analyzes simplified visual qualia from an image."""
        img_np = np.array(image) / 255.0
        hsv_image = image.convert('HSV')
        hsv_array = np.array(hsv_image)
        saturation = hsv_array[:, :, 1].mean() / 255.0

        return {
            "color_diversity": float(np.mean(np.std(img_np, axis=(0, 1)))),
            "brightness": float(img_np.mean()),
            "contrast": float(img_np.std()),
            "saturation": float(saturation)
        }

    def _analyze_audio_qualia(self, y: np.ndarray, sr: int) -> Dict:
        """Analyzes simplified audio qualia from a signal."""
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

        return {
            "chroma_mean": float(chroma.mean()),
            "tempo": float(tempo),
            "spectral_brightness": float(np.mean(spectral_centroid))
        }

    def forge_audio(self, audio_path: str, context: Optional[Dict] = None) -> Dict:
        """Converts an audio file into a PhenomenalREM-Lite object.

        Args:
            audio_path (str): The path to the audio file.
            context (Optional[Dict]): Additional context for the analysis.

        Returns:
            Dict: A dictionary representing the PhenomenalREM-Lite object.
        """
        header = self._generate_rem_header("audio", context or {})
        rem = self._create_base_rem_structure(header)

        try:
            y, sr = librosa.load(audio_path, sr=None)

            rem['phenomenal_core']['qualia_signature'] = self._analyze_audio_qualia(y, sr)
            rem['sensorial_layer']['affective_valence'] = np.random.rand()  # Placeholder
            rem['header']['quality_metrics']['signal_to_noise_ratio'] = np.random.rand() # Placeholder

        except FileNotFoundError:
            print(f"Error: Audio file not found at {audio_path}")
        except Exception as e:
            print(f"Error processing audio {audio_path}: {e}")

        return rem

if __name__ == '__main__':
    # ==============================================================================
    # Demonstration of REMForgeLite
    # ==============================================================================
    # This block showcases the functionality of the REMForgeLite class.
    # It processes a sample text, a dummy image, and a dummy audio file,
    # generating a structured JSON output for each.

    # --- 1. Configuration and Initialization ---
    # Set the device for computation ('cuda' for GPU, 'cpu' for CPU).
    # The script will automatically fall back to 'cpu' if 'cuda' is not available.
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    output_dir = "rem_output"
    os.makedirs(output_dir, exist_ok=True)

    print(f"Initializing REMForgeLite on device: {device}")
    # Instantiate the forger with a custom configuration or use defaults.
    # The configuration defines which models to load.
    forger = REMForgeLite(device=device)
    print("Initialization complete.")
    print("\n" + "="*60 + "\n")

    # --- 2. Text Forging Example ---
    print("--- Forging REM from Text ---")
    sample_text = (
        "I was walking through a dimly lit forest. The air was cold and I could see my breath. "
        "Suddenly, I heard a strange sound, like a whisper, and I felt a sense of unease. "
        "I think it was just the wind, but the feeling stayed with me."
    )
    print(f"Input Text:\n'{sample_text}'\n")
    
    # Process the text to generate a REM.
    text_rem = forger.forge_text(sample_text)
    
    # Save the resulting REM to a JSON file.
    output_path = os.path.join(output_dir, f"{text_rem['header']['rem_id']}_text.json")
    with open(output_path, 'w') as f:
        json.dump(text_rem, f, indent=4)
    print(f"Text REM successfully generated and saved to: {output_path}")
    print("\n" + "="*60 + "\n")

    # --- 3. Image Forging Example ---
    print("--- Forging REM from Image ---")
    dummy_image_path = "dummy_image.png"
    try:
        # Create a simple dummy image (a red square) for the demonstration.
        Image.new('RGB', (128, 128), color='red').save(dummy_image_path)
        print(f"Created a dummy image: {dummy_image_path}")

        # Process the image to generate a REM.
        image_rem = forger.forge_image(dummy_image_path)
        
        # Save the resulting REM to a JSON file.
        output_path = os.path.join(output_dir, f"{image_rem['header']['rem_id']}_image.json")
        with open(output_path, 'w') as f:
            json.dump(image_rem, f, indent=4)
        print(f"Image REM successfully generated and saved to: {output_path}")

    finally:
        # Clean up the created dummy file.
        if os.path.exists(dummy_image_path):
            os.remove(dummy_image_path)
            print(f"Cleaned up dummy image: {dummy_image_path}")
    print("\n" + "="*60 + "\n")

    # --- 4. Audio Forging Example ---
    print("--- Forging REM from Audio ---")
    dummy_audio_path = "dummy_audio.wav"
    try:
        # Create a simple dummy audio file (a sine wave) for the demonstration.
        sr = 22050  # Sample rate
        duration = 2  # seconds
        frequency = 440  # Hz (A4 note)
        t = np.linspace(0., duration, int(sr * duration), endpoint=False)
        amplitude = np.iinfo(np.int16).max * 0.5
        data = amplitude * np.sin(2. * np.pi * frequency * t)
        
        # This requires the 'soundfile' library to be installed.
        try:
            import soundfile as sf
            sf.write(dummy_audio_path, data.astype(np.int16), sr)
            print(f"Created a dummy audio file: {dummy_audio_path}")

            # Process the audio to generate a REM.
            audio_rem = forger.forge_audio(dummy_audio_path)
            
            # Save the resulting REM to a JSON file.
            output_path = os.path.join(output_dir, f"{audio_rem['header']['rem_id']}_audio.json")
            with open(output_path, 'w') as f:
                json.dump(audio_rem, f, indent=4)
            print(f"Audio REM successfully generated and saved to: {output_path}")

        except ImportError:
            print("Skipping audio demonstration: `soundfile` library not found.")
            print("To run this part, please install it via: pip install soundfile")

    finally:
        # Clean up the created dummy file.
        if os.path.exists(dummy_audio_path):
            os.remove(dummy_audio_path)
            print(f"Cleaned up dummy audio: {dummy_audio_path}")

    print("\nDemonstration finished.")