import os
import threading
import sys
import subprocess
from bryan_agent.utils.tool import log_with_loading, log_completion, is_file_valid
from bryan_agent.utils.io import extract_number

class CreateVideo:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.stop_loading = [False]

    def write_input(self, lrc, dic, output_file = "input.txt") :
        folder_path = os.path.join(os.path.dirname(lrc), "background_images")
        output = os.path.join(folder_path, output_file)

        if is_file_valid(output):
            print(f"✅ {output_file} already exists and is valid. Skipping.....")
            return output 

        image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
        image_files.sort(key=extract_number) 

        with open(output, 'w') as file:
            for i, image_file in enumerate(image_files):
                duration = dic.get(i, {}).get('duration', 1.0)  
                
                file_path = os.path.join(folder_path, image_file)
                
                file.write(f"file '{file_path}'\n")
                file.write(f"duration {duration}\n")
            
        return output

    def create_video(self, input_txt, lrc, settings, final_video="background.mp4"):
        logo_path = os.path.join(os.path.dirname(lrc), "logo.png")
        watermark_path = os.path.join(os.path.dirname(__file__), "../../", settings["default_watermark_path"])
        final_video_path = os.path.join(os.path.dirname(lrc), final_video)

        background_resolution = settings["background_resolution"]
        logo_y_position = settings["logo_y_position"]
        watermark_y_position = settings["watermark_y_position"]

        if is_file_valid(final_video_path):
            print(f"✅ {final_video} already exists and is valid. Skipping.....")
            return final_video_path

        with open(input_txt, 'r') as file:
            lines = file.readlines()

        file_paths = []
        durations = []
        for i in range(0, len(lines), 2):
            if lines[i].startswith('file'):
                file_path = lines[i].split(' ')[1].strip().strip("'")
                duration = float(lines[i+1].split(' ')[1].strip())
                file_paths.append(file_path)
                durations.append(duration)

        ffmpeg_command = ["ffmpeg"]
        filter_complex_parts = []
        for idx, (file_path, duration) in enumerate(zip(file_paths, durations)):
            ffmpeg_command.extend(["-loop", "1", "-t", str(duration), "-i", file_path])
            filter_complex_parts.append(f"[{idx}:v]scale={background_resolution},setpts=N/(FRAME_RATE*TB)[v{idx}]")

        ffmpeg_command.extend(["-i", logo_path])
        ffmpeg_command.extend(["-i", watermark_path])

        filter_complex = "; ".join(filter_complex_parts)
        concat_filter = f"[v0]{''.join([f'[v{i}]' for i in range(1, len(file_paths))])}concat=n={len(file_paths)}:v=1:a=0,format=yuv420p[v]"
        
        logo_x = "(main_w/2)-(overlay_w/2)"
        watermark_x = "(main_w/2)-(overlay_w/2)"
        overlay_filter = f"[v][{len(file_paths)}:v]overlay={logo_x}:{logo_y_position}[v_tmp];[v_tmp][{len(file_paths) + 1}:v]overlay={watermark_x}:{watermark_y_position}[v_out]"

        filter_complex = f"{filter_complex}; {concat_filter}; {overlay_filter}"

        ffmpeg_command.extend([
            "-y",
            "-filter_complex", filter_complex,
            "-map", "[v_out]",
            "-vcodec", "libx264",
            "-crf", "25",
            "-pix_fmt", "yuv420p",
            final_video_path
        ])

        try:
            loading_thread = log_with_loading(self.agent_name, "generating videos", self.stop_loading)
            
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            log_completion(self.agent_name, self.stop_loading, loading_thread)
            print(f"✅ The final video is saved as '{final_video}'")

        except subprocess.CalledProcessError as e:
            self.stop_loading[0] = True
            loading_thread.join()
            print(f"Error occurred while creating background video. Details: {e}")

