import os
import argparse
import ffmpeg
from transcribe_zh_en.audio_to_text import transcribe_audio


def has_subtitles(video_path):
    """
    Check if the video has subtitle streams using ffprobe.
    """
    try:
        probe = ffmpeg.probe(video_path)
        streams = probe.get('streams', [])
        for stream in streams:
            if stream.get('codec_type') == 'subtitle':
                return True
        return False
    except ffmpeg.Error as e:
        print(f"Error probing video {video_path}: {e}")
        return False

def detach_subtitles(input_video, output_subtitles):
    """
    Extract subtitles from the video if they exist and store them in the output file.
    """
    if has_subtitles(input_video):
        try:
            # Extract the first subtitle stream, make mapping optional
            stream = ffmpeg.input(input_video)
            stream = ffmpeg.output(stream, output_subtitles, map='0:s:0?', codec='text').overwrite_output()
            print(f"Running ffmpeg command: {' '.join(ffmpeg.compile(stream))}")
            ffmpeg.run(stream)
            
            # Check if subtitles were extracted
            if os.path.exists(output_subtitles) and os.path.getsize(output_subtitles) > 0:
                print(f"Subtitles extracted to {output_subtitles}")
            else:
                print(f"No subtitles found in {input_video}, skipping subtitle extraction.")
        except Exception as e:
            print(f"Error extracting subtitles from {input_video}: {e}")
    else:
        print(f"No subtitles found in {input_video}, skipping subtitle extraction.")

def detach_audio(input_video, output_audio, output_video_no_audio):
    """
    Extract audio and video separately:
    - Extract audio and save it to the output_audio file.
    - Create a new video file without audio and save it to the output_video_no_audio file.
    """
    try:
        # Extract audio from the video and save it to output_audio
        # Using libmp3lame to convert audio to MP3 format
        audio_stream = ffmpeg.input(input_video)
        audio_stream = ffmpeg.output(audio_stream, output_audio, codec='libmp3lame', map='0:a:0').overwrite_output()
        print(f"Running ffmpeg command: {' '.join(ffmpeg.compile(audio_stream))}")
        ffmpeg.run(audio_stream)
        
        # Create the video without audio and save it to output_video_no_audio
        video_stream = ffmpeg.input(input_video)
        video_stream = ffmpeg.output(video_stream, output_video_no_audio, codec='copy').overwrite_output()
        print(f"Running ffmpeg command: {' '.join(ffmpeg.compile(video_stream))}")
        ffmpeg.run(video_stream)
        
        print(f"Audio detached to {output_audio}")
        print(f"Video (without audio) saved to {output_video_no_audio}")
    except ffmpeg.Error as e:
        print(f"Error detaching audio for {input_video}: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error detaching audio for {input_video}: {e}")

def process_video(video_path, processed_dir, detach_subtitles_flag, detach_audio_flag, stt_zh_flag, stt_en_flag):
    """
    Process a single video: detach subtitles, audio, and optionally perform speech-to-text.
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_dir = os.path.join(processed_dir, video_name)

    os.makedirs(video_output_dir, exist_ok=True)

    output_subtitles = os.path.join(video_output_dir, f"{video_name}_zh_subtitles.txt")
    output_audio = os.path.join(video_output_dir, f"{video_name}_audio.mp3")
    output_video_no_audio = os.path.join(video_output_dir, f"{video_name}_NO_AUDIO.mp4")

    # Detach subtitles if flag is set
    if detach_subtitles_flag:
        if not detach_subtitles(video_path, output_subtitles):
            return False  # If subtitle extraction fails, stop further processing.

    # Detach audio if flag is set
    if detach_audio_flag:
        if not detach_audio(video_path, output_audio, output_video_no_audio):
            return False  # If audio extraction fails, stop further processing.

    # Perform Speech-to-Text (Chinese and/or English) if flags are set
    if stt_zh_flag:
        output_stt_zh = os.path.join(video_output_dir, f"{video_name}_stt_zh.txt")
        transcribe_audio(output_audio, output_stt_zh, model_size="small", language="zh")  # Chinese transcription
        
    if stt_en_flag:
        output_stt_en = os.path.join(video_output_dir, f"{video_name}_stt_en.txt")
        transcribe_audio(output_audio, output_stt_en, model_size="small", language="en")  # English transcription

    return True


def main():
    """
    Main function to parse arguments and process videos.
    """
    parser = argparse.ArgumentParser(description="Process videos with subtitles, audio detachment, and speech-to-text conversion.")
    
    parser.add_argument('--ori-vid-dir', required=True, help='Path to the directory containing original videos.')
    parser.add_argument('--processed-dir', help='Path to the directory where processed videos will be saved.')
    parser.add_argument('--detach-subtitles', action='store_true', help='Detach subtitles from videos.')
    parser.add_argument('--detach-audio', action='store_true', help='Detach audio from videos.')
    
    # Flags for speech-to-text conversion
    parser.add_argument('--speech-to-text-zh', action='store_true', help='Perform speech-to-text in Chinese.')
    parser.add_argument('--speech-to-text-en', action='store_true', help='Perform speech-to-text in English.')

    args = parser.parse_args()

    # Validate original video directory
    if not os.path.isdir(args.ori_vid_dir):
        print(f"The specified original video directory does not exist: {args.ori_vid_dir}")
        return

    # If processed-dir is not specified, set it to the parent directory of ori_vid_dir
    if not args.processed_dir:
        ori_vid_dir_parent = os.path.dirname(os.path.abspath(args.ori_vid_dir))
        args.processed_dir = ori_vid_dir_parent
        print(f"No --processed-dir specified. Using parent directory for processed videos: {args.processed_dir}")

    # Process each video in the original video directory
    for video_file in os.listdir(args.ori_vid_dir):
        video_path = os.path.join(args.ori_vid_dir, video_file)

        # Process only .mp4 videos
        if video_file.lower().endswith('.mp4'):
            print(f"Processing video: {video_path}")
            success = process_video(
                video_path, 
                args.processed_dir, 
                args.detach_subtitles, 
                args.detach_audio, 
                args.speech_to_text_zh, 
                args.speech_to_text_en
            )
            if not success:
                print(f"Skipping {video_file} due to processing failure.")
        else:
            print(f"Skipping non-mp4 file: {video_path}")

if __name__ == '__main__':
    main()