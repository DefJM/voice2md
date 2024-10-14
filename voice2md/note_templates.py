from datetime import datetime
from pathlib import Path


def md_note_builder(datetime_created, transcript, transcript_tldr, file_path_voice_memo_processed):
    note = f"""
[[{datetime_created.strftime("%Y-%m-%d")}]]

## TLDR

{transcript_tldr}


## Voice memo transcript

{transcript["text"]}


## Voice memo

![](../../assets/voice_memos_audio_files/{file_path_voice_memo_processed.name})

    """
    return note


def md_note_builder_obsidian(datetime_created, transcript, transcript_tldr, file_path_voice_memo_processed):
    note = f"""---
date-created: {datetime_created.strftime("%Y-%m-%d")}
type: note
tags: [note, voice_memo]
---

[[{datetime_created.strftime("%Y-%m-%d")}]]

## TLDR

{transcript_tldr}


## Voice memo transcript

{transcript["text"]}


## Voice memo

![](../../assets/voice_memos_audio_files/{file_path_voice_memo_processed.name})

    """
    return note
