

lyric_analyze_prompt = """
Analyze the following lyrics and group them into sections for best generating story-like background images:
{dic},
only return output with grouped id numbers in a proper Python recognizable list of lists format, without any other information or lyrics itself.
Each section must have at least two lines of lyrics. Enclose the output in triple backticks for easy parsing.
"""