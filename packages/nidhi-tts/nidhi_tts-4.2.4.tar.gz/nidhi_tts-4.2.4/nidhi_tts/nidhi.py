import sounddevice as sd
import soundfile as sf
import asyncio
import threading
import keyboard
import logging
import numpy as np
import struct
from pathlib import Path
from termcolor import colored
import textwrap
import requests
import argparse
import sys
import json
from enum import Enum
import queue
from charset_normalizer import detect
from typing import Optional, Dict, Any, Union, List, Callable
from dotenv import load_dotenv
load_dotenv()
import os
# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
URLMAIN = "https://nidhitts.sandeshai.in"
BASE = "/tts"
class PlaybackState(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"

class AudioPipeline:
    def __init__(self, pipeline_file: str = "audio_pipeline.bin"):
        self.pipeline_file: Path = Path(pipeline_file)
        self.write_lock: threading.Lock = threading.Lock()
        self.current_position: int = 0
        self.sample_rate: int = 24000
        self.is_empty: bool = True
        self.initialize_pipeline()

    def initialize_pipeline(self) -> None:
        with open(self.pipeline_file, 'wb') as f:
            f.write(struct.pack('QQ', self.sample_rate, 0))
        self.is_empty = True

    def append_audio(self, audio_data: np.ndarray) -> None:
        with self.write_lock:
            with open(self.pipeline_file, 'ab') as f:
                audio_data = audio_data.astype(np.float32)
                f.write(struct.pack('Q', len(audio_data)))
                f.write(audio_data.tobytes())
                self.is_empty = False

    def read_chunk(self, chunk_size: int) -> Optional[np.ndarray]:
        try:
            with open(self.pipeline_file, 'rb') as f:
                if self.current_position == 0:
                    f.seek(16)
                else:
                    f.seek(self.current_position)

                size_data = f.read(8)
                if not size_data:
                    return None

                chunk_length = struct.unpack('Q', size_data)[0]
                audio_bytes = f.read(chunk_length * 4)
                if not audio_bytes:
                    return None

                self.current_position = f.tell()
                return np.frombuffer(audio_bytes, dtype=np.float32)

        except Exception as e:
            logger.error(f"Error reading audio chunk: {e}")
            return None

class AudioPlaybackManager:
    def __init__(self, pipeline: AudioPipeline):
        self.pipeline: AudioPipeline = pipeline
        self.current_stream: Optional[sd.OutputStream] = None
        self.state: PlaybackState = PlaybackState.STOPPED
        self.audio_buffer: np.ndarray = np.zeros(0, dtype=np.float32)
        self.buffer_lock: threading.Lock = threading.Lock()
        self.buffer_empty_event: threading.Event = threading.Event()
        self.buffer_empty_event.set()
        self.command_queue: queue.Queue = queue.Queue()

    def _audio_callback(self, outdata: np.ndarray, frames: int, time: Any, status: Any) -> None:
        with self.buffer_lock:
            if self.state == PlaybackState.PAUSED:
                outdata.fill(0)
                return

            if len(self.audio_buffer) < frames:
                chunk = self.pipeline.read_chunk(frames)
                if chunk is not None:
                    self.audio_buffer = np.concatenate([self.audio_buffer, chunk])
                    self.buffer_empty_event.clear()
                else:
                    self.buffer_empty_event.set()

            if len(self.audio_buffer) >= frames:
                outdata[:, 0] = self.audio_buffer[:frames]
                self.audio_buffer = self.audio_buffer[frames:]
            else:
                outdata.fill(0)
                if self.pipeline.is_empty:
                    self.buffer_empty_event.set()

    def start_playback(self) -> None:
        if self.state != PlaybackState.PLAYING:
            self.current_stream = sd.OutputStream(
                samplerate=self.pipeline.sample_rate,
                channels=1,
                callback=self._audio_callback
            )
            self.current_stream.start()
            self.state = PlaybackState.PLAYING
            logger.info("Playback started")

    def pause_playback(self) -> None:
        if self.state == PlaybackState.PLAYING:
            self.state = PlaybackState.PAUSED
            logger.info("Playback paused")

    def resume_playback(self) -> None:
        if self.state == PlaybackState.PAUSED:
            self.state = PlaybackState.PLAYING
            logger.info("Playback resumed")

    def stop_playback(self) -> None:
        if self.state != PlaybackState.STOPPED:
            if self.current_stream:
                self.current_stream.stop()
                self.current_stream.close()
                self.current_stream = None
            self.state = PlaybackState.STOPPED
            self.buffer_empty_event.set()
            logger.info("Playback stopped")

class TTSGenerator:
    def __init__(
        self, 
        pipeline: AudioPipeline, 
        voice: str, 
        server_url: str = URLMAIN + BASE,
        api_key: Optional[str] = None  # Add this parameter
    ):
        self.pipeline: AudioPipeline = pipeline
        self.voice: str = voice
        self.server_url: str = server_url
        self.api_key: Optional[str] = api_key  # Store the API key
        self.session: requests.Session = requests.Session()

  
    async def generate_and_pipe(self, text: str) -> None:
        try:
            headers = {}
            if self.api_key:
                headers['X-API-Key'] = self.api_key  # Add API key to headers

            response = self.session.post(
                self.server_url,
                json={"text": text, "voice": self.voice},
                headers=headers,  # Include headers
                stream=True
            )
            
            if response.status_code != 200:
                raise Exception(f"Server error: {response.text}")
            temp_file: Path = Path("temp_audio.wav")
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            audio_data, _ = sf.read(temp_file)
            self.pipeline.append_audio(audio_data)
            
            temp_file.unlink(missing_ok=True)
            
        except Exception as e:
            logger.error(f"TTS generation error: {e}")
            if 'temp_file' in locals():
                temp_file.unlink(missing_ok=True)

class APIManager:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        server_url: str = URLMAIN 
    ):
        self.api_key: Optional[str] = api_key
        self.SERVER_URL: str = server_url
        self.session: requests.Session = requests.Session()

    def make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, str]] = None, 
        method: str = 'GET', 
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP request to the server with optional API key authentication
        """
        url: str = self.SERVER_URL + endpoint
        if headers is None:
            headers = {}
        
        if self.api_key:
            headers['X-API-Key'] = self.api_key

        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params, timeout=10)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            try:
                return response.json()
            except ValueError:
                logger.error(f"HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {e}")
            return None

    
class TTSPipelineManager:
    def __init__(
        self, 
        voice: str, 
        api_key: Optional[str] = None, 
        tts_server_url: str = URLMAIN + BASE
    ):
        self.pipeline: AudioPipeline = AudioPipeline()
        self.generator: TTSGenerator = TTSGenerator(
            self.pipeline, 
            voice, 
            tts_server_url, 
            api_key  # Pass the API key
        )
        self.playback: AudioPlaybackManager = AudioPlaybackManager(self.pipeline)
        self.api_manager: APIManager = APIManager(api_key)
        self.running: bool = True
        self.voice: str = voice
        self.api_key: Optional[str] = api_key

    async def process_text(self, text: str) -> None:
        lines: List[str] = [line.strip() for line in text.split('\n') if line.strip()]
        self.playback.start_playback()

        for line in lines:
            if not self.running:
                break
            await self.generator.generate_and_pipe(line)
            await asyncio.sleep(0.1)

    def setup_keyboard_controls(self) -> None:
        def create_key_handler(action: Callable[[], None]) -> Callable[[Any], None]:
            return lambda _: action()

        keyboard.on_press_key('p', create_key_handler(self.toggle_pause))
        keyboard.on_press_key('s', create_key_handler(self.stop_playback))
        keyboard.on_press_key('q', create_key_handler(self.quit))
       
        
        print("\nControls:")
        print("p - Play/Pause")
        print("s - Stop")
        print("q - Quit")
  



    def toggle_pause(self) -> None:
        if self.playback.state == PlaybackState.PLAYING:
            self.playback.pause_playback()
        elif self.playback.state == PlaybackState.PAUSED:
            self.playback.resume_playback()

    def stop_playback(self) -> None:
        self.playback.stop_playback()

    def quit(self) -> None:
        self.running = False
        self.playback.stop_playback()

    async def run(self, text: str) -> None:
        self.setup_keyboard_controls()
        await self.process_text(text)
        
        while self.running:
            await asyncio.sleep(0.1)
            if self.playback.state == PlaybackState.STOPPED:
                self.running = False
def run_tts_pipeline(
    text: Optional[str] = None, 
    file_path: Optional[str] = None, 
    voice: str = 'en-US', 
    api_key: Optional[str] = None
) -> None:
    """
    Direct method to run the TTS pipeline with flexible input options.
    
    Args:
        text (Optional[str]): Direct text to be converted to speech
        file_path (Optional[str]): Path to a text file to be read
        voice (str): Voice to use for TTS (default 'en-US')
        api_key (Optional[str]): API key for the service
    
    Raises:
        ValueError: If no input text is provided
    """
    # Input text retrieval
    input_text: str = ""
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise

    elif text:
        input_text = text
    else:
        raise ValueError("No input text provided. Use 'text' or 'file_path'.")

    # Validate API key
    if not api_key:
        raise ValueError("API key is required")

    # Create async runner wrapper
    async def async_runner():
        # Initialize and run TTS pipeline
        tts_manager = TTSPipelineManager(
            voice=voice, 
            api_key=api_key, 
            tts_server_url=URLMAIN + BASE
        )

        try:
            await tts_manager.run(input_text)
        except KeyboardInterrupt:
            tts_manager.quit()
            logger.info("Quitting gracefully...")

    # Run the async function
    asyncio.run(async_runner())

# Voice data dictionary
voice_data = [
    {"Name": "af-ZA-AdriNeural", "Gender": "Female"},
    {"Name": "af-ZA-WillemNeural", "Gender": "Male"},
    {"Name": "am-ET-AmehaNeural", "Gender": "Male"},
    {"Name": "am-ET-MekdesNeural", "Gender": "Female"},
    {"Name": "ar-AE-FatimaNeural", "Gender": "Female"},
    {"Name": "ar-AE-HamdanNeural", "Gender": "Male"},
    {"Name": "ar-BH-AliNeural", "Gender": "Male"},
    {"Name": "ar-BH-LailaNeural", "Gender": "Female"},
    {"Name": "ar-DZ-AminaNeural", "Gender": "Female"},
    {"Name": "ar-DZ-IsmaelNeural", "Gender": "Male"},
    {"Name": "ar-EG-SalmaNeural", "Gender": "Female"},
    {"Name": "ar-EG-ShakirNeural", "Gender": "Male"},
    {"Name": "ar-IQ-BasselNeural", "Gender": "Male"},
    {"Name": "ar-IQ-RanaNeural", "Gender": "Female"},
    {"Name": "ar-JO-SanaNeural", "Gender": "Female"},
    {"Name": "ar-JO-TaimNeural", "Gender": "Male"},
    {"Name": "ar-KW-FahedNeural", "Gender": "Male"},
    {"Name": "ar-KW-NouraNeural", "Gender": "Female"},
    {"Name": "ar-LB-LaylaNeural", "Gender": "Female"},
    {"Name": "ar-LB-RamiNeural", "Gender": "Male"},
    {"Name": "ar-LY-ImanNeural", "Gender": "Female"},
    {"Name": "ar-LY-OmarNeural", "Gender": "Male"},
    {"Name": "ar-MA-JamalNeural", "Gender": "Male"},
    {"Name": "ar-MA-MounaNeural", "Gender": "Female"},
    {"Name": "ar-OM-AbdullahNeural", "Gender": "Male"},
    {"Name": "ar-OM-AyshaNeural", "Gender": "Female"},
    {"Name": "ar-QA-AmalNeural", "Gender": "Female"},
    {"Name": "ar-QA-MoazNeural", "Gender": "Male"},
    {"Name": "ar-SA-HamedNeural", "Gender": "Male"},
    {"Name": "ar-SA-ZariyahNeural", "Gender": "Female"},
    {"Name": "ar-SY-AmanyNeural", "Gender": "Female"},
    {"Name": "ar-SY-LaithNeural", "Gender": "Male"},
    {"Name": "ar-TN-HediNeural", "Gender": "Male"},
    {"Name": "ar-TN-ReemNeural", "Gender": "Female"},
    {"Name": "ar-YE-MaryamNeural", "Gender": "Female"},
    {"Name": "ar-YE-SalehNeural", "Gender": "Male"},
    {"Name": "az-AZ-BabekNeural", "Gender": "Male"},
    {"Name": "az-AZ-BanuNeural", "Gender": "Female"},
    {"Name": "bg-BG-BorislavNeural", "Gender": "Male"},
    {"Name": "bg-BG-KalinaNeural", "Gender": "Female"},
    {"Name": "bn-BD-NabanitaNeural", "Gender": "Female"},
    {"Name": "bn-BD-PradeepNeural", "Gender": "Male"},
    {"Name": "bn-IN-BashkarNeural", "Gender": "Male"},
    {"Name": "bn-IN-TanishaaNeural", "Gender": "Female"},
    {"Name": "bs-BA-GoranNeural", "Gender": "Male"},
    {"Name": "bs-BA-VesnaNeural", "Gender": "Female"},
    {"Name": "ca-ES-EnricNeural", "Gender": "Male"},
    {"Name": "ca-ES-JoanaNeural", "Gender": "Female"},
    {"Name": "cs-CZ-AntoninNeural", "Gender": "Male"},
    {"Name": "cs-CZ-VlastaNeural", "Gender": "Female"},
    {"Name": "cy-GB-AledNeural", "Gender": "Male"},
    {"Name": "cy-GB-NiaNeural", "Gender": "Female"},
    {"Name": "da-DK-ChristelNeural", "Gender": "Female"},
    {"Name": "da-DK-JeppeNeural", "Gender": "Male"},
    {"Name": "de-AT-IngridNeural", "Gender": "Female"},
    {"Name": "de-AT-JonasNeural", "Gender": "Male"},
    {"Name": "de-CH-JanNeural", "Gender": "Male"},
    {"Name": "de-CH-LeniNeural", "Gender": "Female"},
    {"Name": "de-DE-AmalaNeural", "Gender": "Female"},
    {"Name": "de-DE-ConradNeural", "Gender": "Male"},
    {"Name": "de-DE-FlorianMultilingualNeural", "Gender": "Male"},
    {"Name": "de-DE-KatjaNeural", "Gender": "Female"},
    {"Name": "de-DE-KillianNeural", "Gender": "Male"},
    {"Name": "de-DE-SeraphinaMultilingualNeural", "Gender": "Female"},
    {"Name": "el-GR-AthinaNeural", "Gender": "Female"},
    {"Name": "el-GR-NestorasNeural", "Gender": "Male"},
    {"Name": "en-AU-NatashaNeural", "Gender": "Female"},
    {"Name": "en-AU-WilliamNeural", "Gender": "Male"},
    {"Name": "en-CA-ClaraNeural", "Gender": "Female"},
    {"Name": "en-CA-LiamNeural", "Gender": "Male"},
    {"Name": "en-GB-LibbyNeural", "Gender": "Female"},
    {"Name": "en-GB-MaisieNeural", "Gender": "Female"},
    {"Name": "en-GB-RyanNeural", "Gender": "Male"},
    {"Name": "en-GB-SoniaNeural", "Gender": "Female"},
    {"Name": "en-GB-ThomasNeural", "Gender": "Male"},
    {"Name": "en-HK-SamNeural", "Gender": "Male"},
    {"Name": "en-HK-YanNeural", "Gender": "Female"},
    {"Name": "en-IE-ConnorNeural", "Gender": "Male"},
    {"Name": "en-IE-EmilyNeural", "Gender": "Female"},
    {"Name": "en-IN-NeerjaExpressiveNeural", "Gender": "Female"},
    {"Name": "en-IN-NeerjaNeural", "Gender": "Female"},
    {"Name": "en-IN-PrabhatNeural", "Gender": "Male"},
    {"Name": "en-KE-AsiliaNeural", "Gender": "Female"},
    {"Name": "en-KE-ChilembaNeural", "Gender": "Male"},
    {"Name": "en-NG-AbeoNeural", "Gender": "Male"},
    {"Name": "en-NG-EzinneNeural", "Gender": "Female"},
    {"Name": "en-NZ-MitchellNeural", "Gender": "Male"},
    {"Name": "en-NZ-MollyNeural", "Gender": "Female"},
    {"Name": "en-PH-JamesNeural", "Gender": "Male"},
    {"Name": "en-PH-RosaNeural", "Gender": "Female"},
    {"Name": "en-SG-LunaNeural", "Gender": "Female"},
    {"Name": "en-SG-WayneNeural", "Gender": "Male"},
    {"Name": "en-TZ-ElimuNeural", "Gender": "Male"},
    {"Name": "en-TZ-ImaniNeural", "Gender": "Female"},
    {"Name": "en-US-AnaNeural", "Gender": "Female"},
    {"Name": "en-US-AndrewMultilingualNeural", "Gender": "Male"},
    {"Name": "en-US-AndrewNeural", "Gender": "Male"},
    {"Name": "en-US-AriaNeural", "Gender": "Female"},
    {"Name": "en-US-AvaMultilingualNeural", "Gender": "Female"},
    {"Name": "en-US-AvaNeural", "Gender": "Female"},
    {"Name": "en-US-BrianMultilingualNeural", "Gender": "Male"},
    {"Name": "en-US-BrianNeural", "Gender": "Male"},
    {"Name": "en-US-ChristopherNeural", "Gender": "Male"},
    {"Name": "en-US-EmmaMultilingualNeural", "Gender": "Female"},
    {"Name": "en-US-EmmaNeural", "Gender": "Female"},
    {"Name": "en-US-EricMultilingualNeural", "Gender": "Male"},
    {"Name": "en-US-EricNeural", "Gender": "Male"},
    {"Name": "en-US-JacobNeural", "Gender": "Male"},
    {"Name": "en-US-JennyMultilingualNeural", "Gender": "Female"},
    {"Name": "en-US-JennyNeural", "Gender": "Female"},
    {"Name": "en-US-MichelleNeural", "Gender": "Female"},
    {"Name": "es-AR-JoaquinNeural", "Gender": "Male"},
]


def get_voice_package(name_or_gender=None, locale=None):
    """
    Retrieve voice package name(s) based on pet name, gender, or locale.
    Args:
        name_or_gender (str): Part of the name, pet name, or gender to search for.
        locale (str): Locale to filter the results (e.g., "ar-AE").
    Returns:
        list: Matching voice package names with their genders.
    """
    matches = []
    for entry in voice_data:
        if (
            (name_or_gender and (name_or_gender.lower() in entry["Name"].lower() or name_or_gender.lower() == entry["Gender"].lower())) and
            (locale is None or locale in entry["Name"])
        ):
            matches.append({"Name": entry["Name"], "Gender": entry["Gender"]})
    return matches

def voices(name, locale=None):
    voicedata = []
    results = get_voice_package(name.strip(), locale or None)
    for s in results:
        voicedata.append(s)
    return voicedata
def get_voices(voice, locale=None):
    """
    Retrieve and display available voice models with a colorful, formatted output.
    
    Args:
        voice (str): Voice name, language code, or country code to search
        locale (str, optional): Specific locale to filter voices (e.g., 'en-US')
    
    Usage Examples:
    - get_voices('neerja')           # Search for voices related to 'neerja'
    - get_voices('en')               # Get all English voices
    - get_voices('neerja', 'en-US')  # Get 'neerja' voices in US English locale
    """
    # Print introductory help text
    print(colored("\n🔊 Voice Model Lookup Utility 🔊", "cyan", attrs=['bold']))
    print(colored("----------------------------------", "cyan"))
    
    # Retrieve voice models
    try:
        if locale is not None:
            voice_models = voices(voice, locale)
        else:
            voice_models = voices(voice)
        
        # Check if any voices were found
        if not voice_models:
            print(colored("❌ No voice models found for the given query.", "red"))
            return
        
        # Print header
        print(colored("\nAvailable Voice Models:", "green", attrs=['underline']))
        
        # Print voices with colored numbering
        for i, voice_model in enumerate(voice_models, 1):
            # Use different colors for alternating rows
            color = 'blue' if i % 2 == 0 else 'magenta'
            print(colored(f"{i:2d}. ", color) + colored(f"{voice_model}", color))
        
        # Print total count
        print(colored(f"\nTotal Voices Found: {len(voice_models)}", "yellow"))
    
    except Exception as e:
        print(colored(f"❌ Error retrieving voices: {e}", "red"))

# Examples and usage instructions
def get_voices_help():
    """Print detailed usage instructions for voice lookup"""
    help_text = colored("\n📘 Voice Lookup Helper 📘", "cyan", attrs=['bold'])
    help_text += colored("\n----------------------------", "cyan")
    help_text += colored("\n\nQuick Guide to Finding Voice Models:", "green")
    help_text += colored("\n1. Basic Search:", "yellow")
    help_text += colored("\n   get_voices('neerja')  # Search by name", "white")
    help_text += colored("\n2. Language Search:", "yellow")
    help_text += colored("\n   get_voices('en')      # All English voices", "white")
    help_text += colored("\n3. Locale-Specific Search:", "yellow")
    help_text += colored("\n   get_voices('neerja', 'en-IN')  # indian   English Neerja voices", "white")
    
    print(help_text)
async def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced Text-to-Speech Pipeline")
    parser.add_argument('--text', type=str, help="Input text to convert to speech")
    parser.add_argument('--file', type=str, help="Path to a text file containing input")
    parser.add_argument('--voice', type=str, default='en-US-EmmaNeural', help="Voice for TTS")
    parser.add_argument('--api-key', type=str, help="API key for additional services")
    parser.add_argument('--voices', type=str, help="To get preffered voice names.. by --voices 'your voice '")
    parser.add_argument('--locale', type=str, help="For a specific voice locale eg en-IN")
    
    
    args = parser.parse_args()
    # Validate arguments
    if args.voices:
        print("available voices")
        df = (args.locale if args.locale else None)
        if not df == None:
          print(voices(args.voices[-1], df))
        else:
            print(voices(args.voices[-1]))

    # Input text retrieval
    input_text: str = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            sys.exit(1)
    elif args.text:
        input_text = args.text
    else:
        logger.error("No input text provided. Use --text or --file.")
        sys.exit(1)

    # Interactive API key input if not provided
    api_key: Optional[str] = args.api_key
    if not api_key:
        logger.error("No api key provided please give a api key by --api-key 'api key'")
        sys.exit(1)

    # Initialize and run TTS pipeline
    tts_manager = TTSPipelineManager(
        voice=args.voice, 
        api_key=api_key, 
        tts_server_url=URLMAIN + BASE
    )

    try:
        await tts_manager.run(input_text)
    except KeyboardInterrupt:
        tts_manager.quit()
        logger.info("Quitting gracefully...")

if __name__ == "__main__":
    asyncio.run(main())