# audio_to_text.py

import whisper

def transcribe_audio(audio_path, output_text_path, model_size='turbo', language='zh'):
    """
    Transcribe audio to text using the OpenAI Whisper model.
    - audio_path: Path to the audio file.
    - output_text_path: Path where the transcribed text will be saved.
    - model_size: Whisper model to use. Can be 'tiny', 'base', 'small', 'medium', 'large', or 'turbo'.
    - language: The language of the audio ('zh' for Chinese, 'en' for English).
    """
    try:
        # Load the Whisper model
        model = whisper.load_model(model_size)

        # Load audio file and pad/trim it
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # Make the Mel spectrogram and run inference
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Perform transcription with language setting
        result = model.transcribe(mel, language=language)

        # Save the transcription to a file
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"Transcription saved to {output_text_path}")

    except Exception as e:
        print(f"Error transcribing audio {audio_path}: {e}")