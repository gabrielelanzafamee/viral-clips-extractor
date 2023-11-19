import torch
import librosa

import moviepy.editor as mpe
import whisper_timestamped as whisper

from core.utils.common import generate_random_string

class STT:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.duration = 0 # save the duration for keep the timing during the merge

    def get_transcript(self, video_path: str) -> dict:
        result = []
        transcript = ""

        for chunk in self.chunks_audio(mpe.VideoFileClip(video_path).audio):
            data = self.clean_transcript(
                chunk.get('path'),
                self.__call_whisper__(chunk.get('path')),
                result
            )

            for i in range(0, len(data)-1):
                path = data[i].get('path')
                content = f"{data[i].get('text')} {data[i+1].get('text')}"
                start = data[i].get('start')
                end = data[i+1].get('end')

                result.append({
                    'path': path,
                    'content': content,
                    'start': start,
                    'end': end
                })
                transcript += f"Text: {content} Timestamp: {start[0]} - {end[-1]}\n"
        
        self.__clean_global__()
        return {
            'data': result,
            'transcript': transcript
        }

    def clean_transcript(self, audio_path, transcript, prev_transcript) -> list[dict]:
        if transcript == []:
            return []
        
        print(f"Cleaning the STT...")

        result = []

        if len(prev_transcript) > 1:
            audio, sample_rate = librosa.load(prev_transcript[-1]['path'])
            self.duration += librosa.get_duration(y=audio, sr=sample_rate)

        for i in range(0, len(transcript['segments']), 5):
            segments = transcript['segments'][i:i+5]
            for segment in segments:
                    words = ' '.join([x['text'] for x in segment['words']])
                    words_start_times = [x['start'] + self.duration for x in segment['words']]
                    words_end_times = [x['end'] + self.duration for x in segment['words']]
                    result.append({
                        'path': audio_path,
                        'text': words,
                        'start': words_start_times,
                        'end': words_end_times
                    })

        print(f"Process completed.")
        return result
    
    def chunks_audio(self, audio: mpe.AudioClip) -> list[dict]:
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
            chunks.append({
                'path': tmp_audio,
                'start': start,
                'end': start + chunk_duration
            })
            start += chunk_duration

        return chunks
    
    @staticmethod
    def calc_chunks_size(duration):
        return max(1, int((duration / 60) / 15))

    def __call_whisper__(self, audio_path):
        try:
            print(f'\nLoading audio {audio_path}...')
            audio = whisper.load_audio(audio_path)
            model = whisper.load_model("small.en", device=self.device)
            transcript = whisper.transcribe(model, audio, language="en", verbose=False)
        except:
            return []
        
        return transcript

    def __clean_global__(self):
        self.duration = 0