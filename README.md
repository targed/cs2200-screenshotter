# Screenshotter Script Setup

This guide will help you set up and run the screenshotter script.

## Prerequisites

- Python 3.11 or later
- Google Chrome browser

## Installation Steps

1. Clone the repository or install the improved script:

```bash
git clone https://github.com/joshgollaher/cs2200-screenshotter.git
cd cs2200-screenshotter-main
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Download your game progress:

- Go to the right-hand corner of the game interface and download the .json files for your progress.
- Save the files as nng.json, stg.json, and logic.json in the same json-files directory.

4. Running the Script
   To run the script, cd into the scripts directory and use the following command:

```bash
python main.py
```

5. The script will automatically download and install chromedriver for you. It will then open a Chrome browser window and begin taking screenshots of the game interface.

6. Once you have the screenshots you desire, run the following command to automatically create a pdf of the screenshots:

```bash
python create_pdf.py
```
