import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip

class VideoAgent:
    def create_video(self, image_files, audio_file, output_file="output.mp4"):
        audio_clip = AudioFileClip(audio_file)
        audio_duration = audio_clip.duration
        
        if len(image_files) == 1:
            # Single image case (generated image)
            image_clip = ImageClip(image_files[0]).set_duration(audio_duration)
            video = CompositeVideoClip([image_clip])
        else:
            # Multiple images case (user-provided images)
            image_duration = audio_duration / len(image_files)
            image_clips = [ImageClip(img).set_duration(image_duration) for img in image_files]
            video = concatenate_videoclips(image_clips, method="compose")
            
            # If video is shorter than audio, loop the video
            if video.duration < audio_duration:
                num_loops = int(audio_duration / video.duration) + 1
                video = video.loop(n=num_loops).subclip(0, audio_duration)
        
        # Set the audio to the video
        final_clip = video.set_audio(audio_clip)
        
        # Write the result to a file
        final_clip.write_videofile(output_file, fps=24)
        print(f"Video saved as {output_file}")
        return output_file
