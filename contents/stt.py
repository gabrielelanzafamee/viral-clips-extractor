import librosa

import moviepy.editor as mpe
import whisper_timestamped as whisper

from utils.common import generate_random_string

class STT:
    def __init__(self):
        self.duration = 0 # save the duration for keep the timing during the merge

    def get_transcript(self, video_path: str) -> list[tuple[str, float, float]]:
        result = []
        result_string = ""

        for chunk in self.chunks_audio(mpe.VideoFileClip(video_path).audio):
            transcript = self.__call_whisper__(chunk[0])
            for (path, text, start, end) in self.clean_transcript(chunk[0], transcript, result):
                result.append((path, text, start, end))
                result_string += f"{text}: {start[0]} - {end[-1]}\n"
        
        self.__clean_global__()
        return result, result_string, mpe.VideoFileClip(video_path).audio.duration

    def clean_transcript(self, audio_path, transcript, prev_transcript) -> list[tuple[str, str, list, list]]:
        print(f"Cleaning the STT...")

        result = []
        
        if len(prev_transcript) > 1:
            audio, sample_rate = librosa.load(prev_transcript[-1][0])
            self.duration += librosa.get_duration(y=audio, sr=sample_rate)

        for i in range(0, len(transcript['segments']), 5):
            segments = transcript['segments'][i:i+5]
            for segment in segments:
                    words = ' '.join([x['text'] for x in segment['words']])
                    words_start_times = [x['start'] + self.duration for x in segment['words']]
                    words_end_times = [x['end'] + self.duration for x in segment['words']]
                    result.append((audio_path, words, words_start_times, words_end_times))

        print(f"Process completed.")
        return result
            
    
    def chunks_audio(self, audio: mpe.AudioClip):
        start = 0
        size = 10
        chunk_duration = audio.duration / size
        chunks = []

        print(f"\nChunking the audio...")
        print(f"Duration: {audio.duration}")
        print(f"Single Chunk Duration: {chunk_duration}")
        print(f"Size: {size}\n")

        for _ in range(0, size):
            tmp_audio = f"tmp/{generate_random_string(16)}.mp3"
            audio_chunk = audio.subclip(start, start + chunk_duration)
            audio_chunk.write_audiofile(tmp_audio)
            chunks.append((tmp_audio, start, start + chunk_duration))
            start += chunk_duration

        return chunks
    
    @staticmethod
    def calc_chunks_size(duration):
        return max(1, int((duration / 60) / 15))

    def __call_whisper__(self, audio_path):
        print(f'\nLoading audio {audio_path}...')
        audio = whisper.load_audio(audio_path)
        model = whisper.load_model("base.en", device="cpu") # replace with small
        transcript = whisper.transcribe(model, audio, language="en", verbose=False)
        return transcript

    def __clean_global__(self):
        self.duration = 0
