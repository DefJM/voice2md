# voice2md: Transcribe Apple voice memos to markdown

## Getting started

### Install Ollama
Install Ollama from https://ollama.com. Verify it's running by testing via command line. Pull the llm-model of your choice, e.g. `ollama pull llama3.2:3b`.

### Install dependencies
From the root folder of the project, run:

```bash
poetry install
```

(Note that for compatibility reasons for `llvmlite` with Apple's M-series chips the version for `numpy` was fixed in `pyproject.toml`.) 


### Copy voice memos from Apple Voice Memos app

#### Manually copy voice memos 
Apple restricts access to the voice memos folder by apps. Therefore, voice memos need to be copied manually from the Apple Voice Memos folder to your chosen folder (due to Apple's privacy restrictions).

#### Alternative: Use script instead of manually copying voice memos
Unfortunately, this requires switching on `Full Disk Access` for terminal. **For security reasons this should only be done temporarily!**

1. Set input and output paths in `.env` file (see `.env.template`).
2. Grant `Full Disk Access` to Terminal app (`System Preferences` -> `Security & Privacy` -> `Privacy` -> `Full Disk Access`).
3. Run `python copy_voice_memos.py` from the project root.
4. ⚠️ Remove `Full Disk Access` from Terminal app after copying. 

#### Intend: Automatically pull new voice memos from Apple Voice Memos folder
I tried to set up a cronjob using `crontab -e` / `LaunchAgent`. So far no success dealing with the access restrictions in a secure way. 

### Define paths in `.env`
Copy the `.env_template` file to `.env` and set paths.

### Run the app
From the root folder of the project, run:

```bash
poetry run python app.py
```

Processed notes are saved in `PATH_MARKDOWN` (see `.env`).