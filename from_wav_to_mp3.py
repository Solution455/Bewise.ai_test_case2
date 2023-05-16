import io
from typing import BinaryIO

from pydub import AudioSegment


def convert_to_mp3(wav_audio: BinaryIO):
    """
    converting a wav file to mp3
    :param wav_audio:
    :return mp3_audio io.BytesIO:
    """
    audio = AudioSegment.from_file(io.BytesIO(wav_audio.read()), format="wav")

    mp3_audio = io.BytesIO()
    audio.export(mp3_audio, format="mp3")

    return mp3_audio
