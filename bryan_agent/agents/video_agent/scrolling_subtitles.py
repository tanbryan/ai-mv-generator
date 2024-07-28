import subprocess
import os
import re
import numpy as np
import sys
from bryan_agent.utils.io import get_output_path, load_lrc, get_audio_duration, format_timestamp, cleanup_files
from bryan_agent.utils.tool import log_with_loading, log_completion, is_file_valid
from .settings import settings

class ScrollingSubtitlesGenerator:

    ###❗️❗️❗️ Please do not modify this class, this is the best I can do in ffmpeg syntax❗️❗️❗️

    def __init__(self):
        self.settings = settings

    def video_with_scrolling_subtitles(self, input_audio, input_lyrics):
        input_visual = get_output_path(input_audio, 'background.mp4')
        output = get_output_path(input_audio, "output_with_subtitles.mp4")
        if is_file_valid(output):
            print("✅ output_with_subtitles.mp4 already exists and is valid. Skipping.....")
            return output
        fontfile_path = self.settings['fontfile_path']
        font_size = highlight_fontsize = self.settings['font_size']
        font_color = self.settings['font_color']
        highlight_fontcolor = self.settings['highlight_fontcolor']
        resolution = self.settings['resolution']
        line_spacing = self.settings['subtitle_line_spacing']
        y_start_pos = self.settings['subtitle_starting_position']

        subs = load_lrc(input_lyrics)
        sub_filters = []

        def generate_y_expression(subs, depth=0, base_y=y_start_pos, fontsize=font_size, line_spacing=line_spacing):
            expression = ""
            for i, sub in enumerate(subs):
                adjustment = depth - i
                if i == 0:
                    expression += f"if(lt(t\\,{sub.time})\\,{base_y + (adjustment * (font_size + line_spacing))}\\"
                else:
                    expression += f", if(lt(t\\,{sub.time})\\,{base_y + (adjustment * (font_size + line_spacing))}\\"
            expression += f", {base_y + ((depth - len(subs)) * (font_size + line_spacing))}" 
            return expression + ")" * len(subs) 

        for i, sub in enumerate(subs):
            start_time = sub.time
            end_time = subs[i+1].time if i < len(subs) - 1 else start_time + 5
            y_expression = generate_y_expression(subs, depth=i)
            text = sub.text.replace("'", r"\'")

            drawtext_black_start= (
                    f"drawtext=text='{text}':fontfile='{fontfile_path}':fontsize={font_size}:"
                    f"fontcolor={font_color}:x=(w-text_w)/2:y={y_expression}"
                )
            sub_filters.append(drawtext_black_start)
        
            highlight_text = subs[i].text.replace("'", r"\'")

            drawtext_highlight = (
                f"drawtext=text='{highlight_text}':fontfile='{fontfile_path}':fontsize={highlight_fontsize}:"
                f"fontcolor={highlight_fontcolor}:x=(w-text_w)/2:y={y_start_pos - (font_size + line_spacing)}:enable='between(t,{start_time},{end_time})'"
            )
            sub_filters.append(drawtext_highlight)
            
        scale_filter = f"[1:v]scale={resolution}[scaled];"
        filter_complex = scale_filter  + "[scaled]"+ ",".join(sub_filters) + "[v]"

        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", input_audio,
            "-i", input_visual,
            "-filter_complex", f'"{filter_complex}"',
            "-map", "[v]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output
        ]

        ffmpeg_command = " ".join(ffmpeg_command)
        try:
            subprocess.run(ffmpeg_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while creating video with subtitles. Details: {e}")
            return None

    def crop_video(self, input_audio):
        input_subtitle_video = get_output_path(input_audio, "output_with_subtitles.mp4")
        output = get_output_path(input_subtitle_video, "cropped_subtitle.mp4")

        y_start_pos = self.settings['subtitle_starting_position']
        fontsize = self.settings['font_size']
        line_spacing = self.settings['subtitle_line_spacing']


        resolution = self.settings['resolution']
        match = re.match(r"(\d+)x(\d+)", resolution)
        if not match:
            raise ValueError(f"Invalid resolution format: {resolution}")
        crop_width = int(match.group(1))

        crop_height = (line_spacing + fontsize) * 7 + line_spacing
        crop_y = y_start_pos - (line_spacing + fontsize) * 4 - line_spacing
        crop_x = 0  
        if is_file_valid(output):
            print("✅ cropped_subtitle.mp4 already exists and is valid. Skipping.....")
            return (crop_x, crop_y, crop_width, crop_height)
        crop_command = f"crop=w={crop_width}:h={crop_height}:x={crop_x}:y={crop_y},format=yuv420p"
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", input_subtitle_video,
            "-vf", crop_command,
            "-c:v", "libx264", 
            "-crf", "18", 
            "-preset", "slow",  
            output
        ]
        try:
            result = subprocess.run(" ".join(ffmpeg_command), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return (crop_x, crop_y, crop_width, crop_height)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while cropping video. Details: {e.stderr.decode()}")
            raise

    def overlay_cropped_video(self, input_audio, crop_params):
        input_visual = get_output_path(input_audio, 'background.mp4')
        input_cropped = get_output_path(input_visual, "cropped_subtitle.mp4")
        output = get_output_path(input_visual, "final_output_with_subtitles.mp4")
        if is_file_valid(output):
            print("✅ final_output_with_subtitles.mp4 already exists and is valid. Skipping.....")
            return output
        x, y, _, _ = crop_params
        overlay_command = f"[0:v]format=yuv420p[base],[1:v]format=yuv420p[cropped],[base][cropped]overlay={x}:{y}"
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", input_visual,
            "-i", input_cropped,
            "-filter_complex", overlay_command,
            "-map", "1:a",  
            "-c:v", "libx264",  
            "-crf", "18", 
            "-preset", "slow", 
            output
        ]
        subprocess.run(" ".join(ffmpeg_command), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output

    def add_title(self, input_audio):
        input_video = get_output_path(input_audio, 'final_output_with_subtitles.mp4')
        output = get_output_path(input_audio, os.path.basename(input_video))

        fontfile_path = self.settings['fontfile_path']
        fontsize = self.settings['title_size']
        title_color = self.settings['title_color']
        line_spacing = self.settings['title_line_spacing']
        title_position = self.settings['title_position']
        author_fontsize = self.settings['author_fontsize']
        timestamp_fontsize = self.settings['timestamp_fontsize']
        author_color = self.settings['author_color']
        timestamp_color = self.settings['timestamp_color']

        base_name = os.path.basename(input_audio)
        video_name = base_name.split('.')[0]
        title, author = base_name.split('-')
        title = title.strip()
        author = author.split('.')[0].strip()

        output_dir = os.path.dirname(input_audio)
        output_video = os.path.join(output_dir, video_name + ".mp4")

        if is_file_valid(output_video):
            print(f"✅ {video_name}.mp4 already exists and is valid. Skipping.....")
            return output
        audio_duration = get_audio_duration(input_audio)
        total_timestamp = format_timestamp(audio_duration)

        filter_complex = [
            f"drawtext=text='{title}':fontfile='{fontfile_path}':fontsize={fontsize}:fontcolor={title_color}:x=(w-text_w)/2:y={title_position}",
            f"drawtext=text='{author}':fontfile='{fontfile_path}':fontsize={author_fontsize}:fontcolor={author_color}:x=(w-text_w)/2:y={title_position + fontsize + line_spacing}",
            f"drawtext=text='%{{pts\:gmtime\:0\:%M %S }}/{ total_timestamp}':fontfile='{fontfile_path}':fontsize={timestamp_fontsize}:fontcolor={timestamp_color}:x=(w-text_w)/2:y={title_position + 2 * (fontsize + line_spacing)}"
        ]
        filter_complex_string = ",".join(filter_complex)

        ffmpeg_command = f"ffmpeg -y -i {input_video} -filter_complex \"{filter_complex_string}\" -c:v libx264 -crf 23 -preset fast {output_video}"

        subprocess.run(ffmpeg_command, shell=True, check=True,  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        cleanup_files(output_dir)
        
        return output_video
