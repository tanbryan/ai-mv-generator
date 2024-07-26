# prompt_agent/prompt.py

base_prompt = """
The following are the full lyrics of a song to provide context:
{full_lyrics}
These lyrics will be used to generate detailed prompts for creating music video background images. 
Only return the detailed prompts without any other information.
Ensure that all the images generated have a consistent style and color scheme as per the base style settings provided.
"""

section_prompt = """
Group {idx} lyrics:
{group_lyrics}

The task is to create {num_images} detailed prompts for generating the best music video background images for this group of lyrics. 
Ensure the style and color scheme are consistent, and the images maintain logical continuity. 
"""

group_prompt = """
Follow the structure below for each prompt output:

- Image {idx}.{image_idx}: Generate an image that
    - Description: Detailed description of the scene based on the lyrics
    - Base Style Settings: {base_style_settings}
    - Elements: Key elements to include in the image, separated by commas
"""
