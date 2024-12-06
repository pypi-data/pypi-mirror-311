import os
import argparse
import ffmpeg

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
        video_stream = ffmpeg.output(video_stream, output_video_no_audio, codec='copy', an=True).overwrite_output()
        print(f"Running ffmpeg command: {' '.join(ffmpeg.compile(video_stream))}")
        ffmpeg.run(video_stream)
        
        print(f"Audio detached to {output_audio}")
        print(f"Video (without audio) saved to {output_video_no_audio}")
    except ffmpeg.Error as e:
        print(f"Error detaching audio for {input_video}: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error detaching audio for {input_video}: {e}")

def process_video(video_path, processed_dir, detach_subtitles_flag, detach_audio_flag):
    """
    Process a single video: detach subtitles and/or detach audio based on flags.
    """
    # Get the base name of the video without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Determine the output directory for processed video files
    video_output_dir = os.path.join(processed_dir, video_name)

    # Create output directory for each video if it doesn't exist
    os.makedirs(video_output_dir, exist_ok=True)

    # Define output file names
    output_subtitles = os.path.join(video_output_dir, f"{video_name}_zh_subtitles.txt")
    output_audio = os.path.join(video_output_dir, f"{video_name}_audio.mp3")
    output_video_no_audio = os.path.join(video_output_dir, f"{video_name}_NO_AUDIO.mp4")

    # Detach subtitles if flag is set and subtitles exist
    if detach_subtitles_flag:
        detach_subtitles(video_path, output_subtitles)

    # Detach audio if flag is set
    if detach_audio_flag:
        detach_audio(video_path, output_audio, output_video_no_audio)


def main():
    """
    Main function to parse arguments and process videos.
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Process videos with Chinese subtitles and audio detachment. '
                    'This tool detaches subtitles if they are present and removes audio if requested.'
    )

    # Add arguments
    parser.add_argument(
        '--ori-vid-dir', 
        required=True, 
        help='Path to the directory containing the original video files (e.g., .mp4 files) that need to be processed. '
             'The tool will process all videos in this directory.' 
    )
    
    parser.add_argument(
        '--processed-dir', 
        help='Path to the directory where processed videos will be saved. If not specified, '
             'the processed videos will be saved outside the original video directory in a subdirectory '
             'named after each video. If --processed-dir is specified, each subdirectory will be named after the processed video.'
    )
    
    parser.add_argument(
        '--detach-subtitles', 
        action='store_true', 
        help='If set, the tool will attempt to detach Chinese subtitles from the videos, '
             'if subtitles are available.'
    )
    
    parser.add_argument(
        '--detach-audio', 
        action='store_true', 
        help='If set, the tool will remove audio from the video files and store it separately.'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Validate the original video directory
    if not os.path.isdir(args.ori_vid_dir):
        print(f"The specified original video directory does not exist: {args.ori_vid_dir}")
        return

    # If processed-dir is not specified, set it to the parent directory of ORI_Vid_dir
    if not args.processed_dir:
        # Define processed_dir as a sibling to ori_vid_dir
        ori_vid_dir_parent = os.path.dirname(os.path.abspath(args.ori_vid_dir))
        args.processed_dir = ori_vid_dir_parent
        print(f"No --processed-dir specified. Using parent directory for processed videos: {args.processed_dir}")

    # Validate the processed directory if specified
    else:
        if not os.path.exists(args.processed_dir):
            try:
                os.makedirs(args.processed_dir, exist_ok=True)
                print(f"Created processed directory: {args.processed_dir}")
            except Exception as e:
                print(f"Error creating processed directory {args.processed_dir}: {e}")
                return
        else:
            print(f"Using specified processed directory: {args.processed_dir}")

    # Process all videos in the given directory
    for video_file in os.listdir(args.ori_vid_dir):
        video_path = os.path.join(args.ori_vid_dir, video_file)
        
        # Process only .mp4 videos
        if video_file.lower().endswith('.mp4'):
            print(f"Processing video: {video_path}")
            process_video(video_path, args.processed_dir, args.detach_subtitles, args.detach_audio)
        else:
            print(f"Skipping non-mp4 file: {video_path}")

if __name__ == '__main__':
    main()