"""
Google Cloud Speech-to-Text and Text-to-Speech integration
Provides production-grade models with native Nigerian accents
"""

from google.cloud import speech_v1 as speech
from google.cloud import texttospeech_v1 as texttospeech
from languages import Language
import logging

logger = logging.getLogger(__name__)


# Google Cloud STT language codes with regional support
GOOGLE_STT_LANGUAGE_CODES = {
    Language.ENGLISH: "en-NG",  # English (Nigeria)
    Language.FRENCH: "fr-FR",   # French (France) - also works for West African French
    Language.PIDGIN: "en-NG",   # Use Nigerian English for Pidgin (closest match)
    Language.IGBO: "en-NG",      # Igbo not natively supported, fallback to Nigerian English
    Language.HAUSA: "ha-Latn-NG",  # Hausa (Latin script, Nigeria) - NATIVE SUPPORT
    Language.YORUBA: "en-NG"      # Yoruba STT not available, use Nigerian English
}


# Google Cloud TTS voice configurations with native regional voices
GOOGLE_TTS_VOICES = {
    Language.ENGLISH: {
        "language_code": "en-NG",
        "name": "en-NG-Standard-A",  # Nigerian English voice
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
    },
    Language.FRENCH: {
        "language_code": "fr-FR",  # French (France) - clear accent
        "name": "fr-FR-Neural2-A",  # Neural voice for best quality with proper accent
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
    },
    Language.PIDGIN: {
        "language_code": "en-NG",
        "name": "en-NG-Standard-B",  # Nigerian English voice (Male)
        "ssml_gender": texttospeech.SsmlVoiceGender.MALE
    },
    Language.IGBO: {
        "language_code": "en-NG",  # Igbo TTS not available, use Nigerian English
        "name": "en-NG-Standard-A",
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
    },
    Language.HAUSA: {
        "language_code": "ha-Latn-NG",  # NATIVE HAUSA VOICE!
        "name": "ha-Latn-NG-Standard-A",
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
    },
    Language.YORUBA: {
        "language_code": "yo-NG",  # NATIVE YORUBA VOICE!
        "name": "yo-NG-Standard-A",
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
    }
}


class GoogleCloudSTT:
    """Google Cloud Speech-to-Text wrapper for Nigerian languages"""

    def __init__(self):
        """Initialize Google Cloud Speech client"""
        try:
            self.client = speech.SpeechClient()
            logger.info("Google Cloud Speech-to-Text client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud Speech client: {e}")
            logger.warning("Falling back to OpenAI Whisper")
            self.client = None

    def get_recognition_config(self, language: Language) -> speech.RecognitionConfig:
        """
        Get speech recognition configuration for specified language

        Args:
            language: The language to use for recognition

        Returns:
            RecognitionConfig object with optimal settings
        """
        language_code = GOOGLE_STT_LANGUAGE_CODES.get(language, "en-NG")

        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="default",  # Use default model for best quality
            use_enhanced=True  # Use enhanced model for better accuracy
        )

    def transcribe_audio(self, audio_content: bytes, language: Language) -> str:
        """
        Transcribe audio to text using Google Cloud Speech-to-Text

        Args:
            audio_content: Raw audio bytes (LINEAR16, 16kHz)
            language: Language to use for transcription

        Returns:
            Transcribed text
        """
        if not self.client:
            raise Exception("Google Cloud Speech client not initialized")

        config = self.get_recognition_config(language)
        audio = speech.RecognitionAudio(content=audio_content)

        try:
            response = self.client.recognize(config=config, audio=audio)

            # Combine all transcription results
            transcripts = [result.alternatives[0].transcript
                         for result in response.results
                         if result.alternatives]

            return " ".join(transcripts)
        except Exception as e:
            logger.error(f"Google Cloud STT error: {e}")
            raise


class GoogleCloudTTS:
    """Google Cloud Text-to-Speech wrapper with native Nigerian voices"""

    def __init__(self):
        """Initialize Google Cloud Text-to-Speech client"""
        try:
            self.client = texttospeech.TextToSpeechClient()
            logger.info("Google Cloud Text-to-Speech client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud TTS client: {e}")
            logger.warning("Falling back to OpenAI TTS")
            self.client = None

    def get_voice_config(self, language: Language) -> texttospeech.VoiceSelectionParams:
        """
        Get voice configuration for specified language

        Args:
            language: The language to use for synthesis

        Returns:
            VoiceSelectionParams with optimal voice for the language
        """
        voice_config = GOOGLE_TTS_VOICES.get(language, GOOGLE_TTS_VOICES[Language.ENGLISH])

        return texttospeech.VoiceSelectionParams(
            language_code=voice_config["language_code"],
            name=voice_config["name"],
            ssml_gender=voice_config["ssml_gender"]
        )

    def synthesize_speech(self, text: str, language: Language) -> bytes:
        """
        Convert text to speech using Google Cloud TTS

        Args:
            text: Text to convert to speech
            language: Language to use for synthesis

        Returns:
            Audio content as bytes (MP3 format)
        """
        if not self.client:
            raise Exception("Google Cloud TTS client not initialized")

        # Prepare the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Get voice configuration
        voice = self.get_voice_config(language)

        # Configure audio output
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,  # Normal speed
            pitch=0.0,  # Normal pitch
            volume_gain_db=0.0  # Normal volume
        )

        try:
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            return response.audio_content
        except Exception as e:
            logger.error(f"Google Cloud TTS error: {e}")
            raise

    def list_available_voices(self, language: Language = None):
        """
        List all available voices for a language (useful for testing)

        Args:
            language: Optional language filter

        Returns:
            List of available voices
        """
        if not self.client:
            return []

        if language:
            voice_config = GOOGLE_TTS_VOICES.get(language)
            if voice_config:
                language_code = voice_config["language_code"]
            else:
                language_code = "en-NG"
        else:
            language_code = None

        response = self.client.list_voices(language_code=language_code)

        voices = []
        for voice in response.voices:
            voices.append({
                "name": voice.name,
                "language_codes": voice.language_codes,
                "gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name
            })

        return voices


def get_supported_languages_info():
    """
    Get information about which languages have native support

    Returns:
        Dictionary with language support details
    """
    return {
        Language.ENGLISH: {
            "name": "English (Nigerian)",
            "stt_native": True,
            "tts_native": True,
            "stt_code": "en-NG",
            "tts_voice": "en-NG-Standard-A",
            "quality": "★★★★★"
        },
        Language.FRENCH: {
            "name": "Français",
            "stt_native": True,
            "tts_native": True,
            "stt_code": "fr-FR",
            "tts_voice": "fr-FR-Neural2-A",
            "quality": "★★★★★",
            "note": "Neural voice with authentic French accent"
        },
        Language.PIDGIN: {
            "name": "Nigerian Pidgin",
            "stt_native": False,  # Uses Nigerian English
            "tts_native": False,  # Uses Nigerian English
            "stt_code": "en-NG",
            "tts_voice": "en-NG-Standard-B",
            "quality": "★★★★☆",
            "note": "Uses Nigerian English voice (very close to Pidgin)"
        },
        Language.IGBO: {
            "name": "Igbo",
            "stt_native": False,  # Not available
            "tts_native": False,  # Not available
            "stt_code": "en-NG",
            "tts_voice": "en-NG-Standard-A",
            "quality": "★★★☆☆",
            "note": "Falls back to Nigerian English (accent may not be perfect)"
        },
        Language.HAUSA: {
            "name": "Hausa",
            "stt_native": True,  # NATIVE SUPPORT!
            "tts_native": True,  # NATIVE SUPPORT!
            "stt_code": "ha-Latn-NG",
            "tts_voice": "ha-Latn-NG-Standard-A",
            "quality": "★★★★★"
        },
        Language.YORUBA: {
            "name": "Yoruba",
            "stt_native": False,  # Not available
            "tts_native": True,  # NATIVE SUPPORT!
            "stt_code": "en-NG",
            "tts_voice": "yo-NG-Standard-A",
            "quality": "★★★★☆",
            "note": "Native TTS voice, STT uses Nigerian English"
        }
    }


# Convenience function to check if credentials are configured
def check_google_cloud_credentials():
    """
    Check if Google Cloud credentials are properly configured

    Returns:
        Boolean indicating if credentials are valid
    """
    try:
        # Try to initialize both clients
        speech_client = speech.SpeechClient()
        tts_client = texttospeech.TextToSpeechClient()
        logger.info("✓ Google Cloud credentials are properly configured")
        return True
    except Exception as e:
        logger.error(f"✗ Google Cloud credentials error: {e}")
        logger.info("Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        return False


if __name__ == "__main__":
    # Test script
    print("Google Cloud Models Configuration")
    print("=" * 50)
    print("\nSupported Languages:")
    for lang, info in get_supported_languages_info().items():
        print(f"\n{lang.value}: {info['name']}")
        print(f"  STT Native: {'✓' if info['stt_native'] else '✗'} ({info['stt_code']})")
        print(f"  TTS Native: {'✓' if info['tts_native'] else '✗'} ({info['tts_voice']})")
        print(f"  Quality: {info['quality']}")
        if 'note' in info:
            print(f"  Note: {info['note']}")

    print("\n" + "=" * 50)
    print("\nChecking credentials...")
    if check_google_cloud_credentials():
        print("✓ Ready to use Google Cloud models!")
    else:
        print("✗ Please configure Google Cloud credentials")
        print("  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json")
