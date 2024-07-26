style_prompt = """
The following are the full lyrics of a song, a set of parameters to provide context for the music background image style. 

Lyrics:
{full_lyrics}

Parameters:
{parameters_json}

Analyze these lyrics and parameters to generate a new JSON object that sets the base style of the background image throughout the song. 
There are no need to include all the parameters in the output, only the ones that are relevant to the song.
The base style should include relevant art styles, mediums, and any other attributes that fit the overall tone and mood of the song.

{customization_prompt}

Only return the output as a JSON object with the base style settings for this song in a proper Python recognizable format, without any other information or lyrics itself.
Structure the output starting directly with the elements, without any outer key.
Enclose the output in triple backticks for easy parsing, without any other information.
"""
