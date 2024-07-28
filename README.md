# ai-mv-generator

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Bryan Agents is an advanced multi-agent system designed for generating music videos based on lyrics. This project analyzes the lyrics and creates story-like images to generate an image-to-image music video. The system leverages the OpenAI API, specifically the GPT-4o model for text processing and the DALL-E 3 model for image generation, to provide an end-to-end solution for video content creation.


## Features

- **Lyric Analyze Agent**: Analyzes lyrics and groups them for further processing.
- **Style Agent**: Analyzes and applies styles to the content.
- **Prompt Agent**: Generates detailed prompts for creating music video background images using GPT-4o model.
- **Image Agent**: Creates images based on the generated prompts using DALL-E 3 model.
- **Logo Agent**: Generates logos with various effects.
- **Video Agent**: Compiles the generated images, logos, and scorlling lyrics into a final video.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- `ffmpeg` installed and available in your system's PATH
- Required Python packages installed

### Installing `ffmpeg`

#### Windows:

1. Download `ffmpeg` from the [official website](https://ffmpeg.org/download.html).
2. Extract the downloaded archive to a folder of your choice.
3. Add the `bin` folder to your system's PATH:
    - Open the Start Search, type in "env", and select "Edit the system environment variables".
    - In the System Properties window, click on the "Environment Variables" button.
    - In the Environment Variables window, find the `Path` variable in the "System variables" section and select it. Click on "Edit".
    - Click "New" and add the path to the `bin` folder of the extracted `ffmpeg` archive. Click "OK" to apply the changes.

#### macOS:

1. Install `Homebrew` if you don't have it installed. Open the Terminal and run:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. Use `Homebrew` to install `ffmpeg`:

    ```bash
    brew install ffmpeg
    ```

#### Linux:

1. For Debian-based distributions (e.g., Ubuntu), open the Terminal and run:

    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

2. For Red Hat-based distributions (e.g., Fedora), open the Terminal and run:

    ```bash
    sudo dnf install ffmpeg
    ```

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/tanbryan/ai-mv-generator
    cd bryan-agent
    ```

2. **Create and activate a virtual environment (optional):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key:**

    Create a `.env` file in the project root and add your OpenAI API key:

    ```env
    OPENAI_API_KEY= "your_openai_api_key_here"
    ```

## Usage

1. **Run the main script:**

    Ensure that the lyrics file (.lrc) and music file (.mp3) are located within a dedicated directory. 
    ❗️Please make sure both files are named in the format of 'SongName-ArtistName.lrc or .mp3'
    Go into the main script `runner.py` and add your complete paths to both files:
    Then run: 

    ```bash
    python runner.py
    ```

2. **Agent Execution and Result Saving:**

    Each agent will work sequentially on the provided lyrics file:
    - **LyricAnalyzeAgent**: Analyzes the lyrics and groups them for further processing. The results will be saved in a JSON file within the lyrics directory.
    - **StyleAgent**: Analyzes and applies styles to the content. The base style settings will be saved in the same JSON file.
    - **PromptAgent**: Generates detailed prompts for creating music video background images. The script will pause after generating the prompts for you to review them in the generated JSON file. Once reviewed, press Enter to continue.
    - **ImageAgent**: Creates images based on the generated prompts and saves them in the specified directory.
    - **LogoAgent**: Generates logos with various effects.
    - **VideoAgent**: Compiles the generated images and logos into a final video.

    During the execution, an `agent_status.json` file will be created in the base_agent directory. This file keeps track of the status of each agent. If any agent completes, its status will be set to `true`. You can always set the status to `false` to rerun a specific agent if needed.

3. **Review the generated prompts:**

    The script will pause after generating the prompts. Review them in the generated JSON file within the lyrics directory. Once reviewed, press Enter to continue.

4. **Complete the image and video generation:**

    Follow the prompts to complete the image and video generation process.
    
## Test Directory

In the `test` directory, you will find sample outputs based on the "Love Story" by Taylor Swift lyrics file:

- `LoveStory-TaylorSwift.mp4`: The final generated video.
- `generated_prompts.json`: The JSON file containing the detailed prompts generated for the images.
- `logo.png`: The generated logo for the music video.
- `results.json`: The JSON file containing the results from each agent.
- `background_images/`: A folder containing the background images generated based on the prompts.

These samples provide an example of the output you can expect from the system.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
