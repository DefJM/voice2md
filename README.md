# voice2md: Transcribe Apple voice memos to markdown



## Getting started

### Prequequisite: Ollama is installed on your machine

You can install Ollama directly from their homepage: https://ollama.com. 
Make sure it is running, by testing it by running it the usual way through the command line.


### Step 1: Install dependencies

From the root folder of the project, run:

```bash
poetry install
```

### Step 2: Copy voice memos from Apple Voice Memos app to desktop

Due to privacy restrictions, in order to process Apple's voice memos you have to manually copy the voice memos from the Apple Voice Memos app to the folder of your choice. Unfortunately, there is no easy way to do this yet. 

1. Provide input and output paths (input and output directories) in `.env` file. See `.env.template` for reference.

2. Provide `Full Disk Access` to the Terminal app, so it can access your file system. You can do this by going to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Full Disk Access` and then adding the Terminal app.

3. Using the Terminal app, navigate to the root folder of the project. Run `python copy_voice_memos.py`. Currently, the script will copy voice memos < 0.5 MB in size. You can change this in the script. Once this is done, you should see the copied files in the output paths you've specified in the `.env` file.

4. ⚠️ Remove `Full Disk Access` from the Terminal app (you can do this by going to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Full Disk Access` and then removing the Terminal app from the list).


