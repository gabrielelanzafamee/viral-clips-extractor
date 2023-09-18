# Viral Clips Extractor

This is a clips extractor tool that allows you to extract the most viral, funny, or interesting parts of a YouTube video based on the transcript, create subtitles, and crop the video around detected faces using OpenCV. It leverages the power of Whisper Timestamped for transcript extraction and ChatGPT 3.5 for content analysis.

## Overview

This tool provides a convenient way to:

1. Extract the transcript of a YouTube video using whisper_timestamped.
2. Analyze the transcript with ChatGPT 3.5 to identify the most engaging parts.
3. Cut the video at the identified times to create shorter clips.
4. Generate subtitles for the clips.
5. Automatically crop the video to focus on the detected faces using OpenCV.

## Requirements

To run the YouTube Clips Extractor, you'll need the following:
- FFMPEG
- ImageMagick
- Check the `requirements.txt` file.

## Installation

1. Clone this repository:

   ```shell
   git clone https://github.com/xjabr/viral-clips-extractor.git
   ```

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Sign up for ChatGPT 3.5 and obtain your API credentials.

4. Configure the API credentials for ChatGPT 3.5 by update the variable `openai.api_key` in `contents/chatgpt.py` file in the project directory.

   ```python
   openai.api_key = '<your-token>'
   ```

5. Run the application:

   ```shell
   python clips_extractor.py --url <url>
   ```

## Contributors

This project was developed by:

- Gabriele Lanzafame (@xjabr) - [GitHub Profile](https://github.com/xjabr)

If you'd like to contribute or report issues, please feel free to open an [issue](https://github.com/xjabr/viral-clips-extractor/issues) or submit a [pull request](https://github.com/xjabr/viral-clips-extractor/pulls).

## Acknowledgments

We would like to thank the following libraries and services for making this project possible:

- [moviepy](https://github.com/Zulko/moviepy) by Zulko
- [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) by linto-ai
- [ChatGPT 3.5](https://beta.openai.com/signup/) by OpenAI
- [OpenCV](https://opencv.org/) for face detection and video manipulation

Your contributions and feedback are highly appreciated!