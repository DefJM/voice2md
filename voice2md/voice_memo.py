import shutil
import re
from datetime import datetime

from voice2md.llm import llm_generate_note_title, llm_summarize_transcript
from voice2md.note_templates import md_note_builder


class VoiceMemo:
    """
    Class for processing voice memos. Handles parsing dates, transcription,
    summarization, and file operations.
    """

    def __init__(self, file_path_original, path_voice_memos_processed, path_markdown):
        """
        Initialize the voice_memo object.

        Args:
            file_path_original (Path): Path to the original voice memo file.
            path_voice_memos_processed (Path): Directory path for processed voice memos.
            path_markdown (Path): Directory path for markdown files.
        """
        self.file_path_original = file_path_original
        self.path_voice_memos_processed = path_voice_memos_processed
        self.path_markdown = path_markdown
        self.datetime_created = None
        self.file_size_mb = None
        self.transcript = None
        self.transcript_tldr = None
        self.transcript_title = None
        self.file_name_datetime = None
        self.file_path_voice_memo_processed = None
        self.file_path_markdown = None
        self.md_note = None

    def parse_datetime_created(self):
        """Parse the creation datetime from the original file name."""
        datetime_str = str(self.file_path_original).split("/")[-1].split("-")[0]
        self.datetime_created = datetime.strptime(datetime_str, "%Y%m%d %H%M%S")

    def get_file_size_mb(self):
        """Calculate and store the file size in megabytes."""
        self.file_size_mb = round(
            self.file_path_original.stat().st_size / (1024 * 1024), 2
        )

    def create_file_path_voice_memo_processed(self):
        """Create the file path for the processed voice memo."""
        self.file_name_datetime = f"{self.datetime_created.strftime('%Y-%m-%d_%H%M%S')}_{str(self.file_path_original).split('.')[0].split('-')[-1]}"
        self.file_path_voice_memo_processed = (
            self.path_voice_memos_processed / f"{self.file_name_datetime}.m4a"
        )

    def create_file_path_markdown(self):
        """Create the file path for the markdown file."""
        self.file_name_note = f"{self.datetime_created.strftime('%Y-%m-%d_%H%M%S')}_{str(self.file_path_original).split('.')[0].split('-')[-1]}"
        self.file_path_markdown = (
            self.path_markdown / f"{self.file_name_datetime}_{self.transcript_title}.md"
        )

    def save_voice_memo_processed(self):
        """Save a copy of the processed voice memo file."""
        shutil.copy2(self.file_path_original, self.file_path_voice_memo_processed)

    def transcribe(self, asr_model):
        """
        Transcribe the voice memo using the provided ASR model.

        Args:
            asr_model: ASR model for transcription.
        """
        transcript = asr_model.transcribe(str(self.file_path_voice_memo_processed))
        transcript["text"] = transcript["text"].strip()
        self.transcript = transcript

    def summarize(self, llm_client, model):
        """
        Generate a summary of the transcript.

        Args:
            llm_client: LLM client for summarization.
            model (str): Model for summarization.
        """
        if len(self.transcript["text"]) <= 20:
            self.transcript_tldr = self.transcript["text"]
        else:
            res = llm_summarize_transcript(llm_client, self.transcript, model=model)
            res_text = res.choices[0].message.content.strip()
            self.transcript_tldr = res_text

    def generate_title(self, llm_client, model):
        """
        Generate a title for the transcript.

        Args:
            llm_client: LLM client for title generation.
            model (str): Model for title generation.
        """
        res = llm_generate_note_title(llm_client, self.transcript, model=model)
        res_text = res.choices[0].message.content.strip()[:80]
        self.transcript_title = self.clean_title(res_text)

    def clean_title(self, transcript_title):
        """
        Clean the generated title by removing non-alphanumeric characters and replacing spaces with hyphens.

        Args:
            transcript_title (str): Raw generated title.

        Returns:
            str: Cleaned title.
        """
        cleaned_title = re.sub(r"[^a-zA-Z0-9\s]", "", transcript_title)
        cleaned_title = re.sub(r"\s+", "-", cleaned_title)
        return cleaned_title.strip("-")

    def save_transcription(self):
        """Generate and save the markdown note with the transcription and summary."""
        self.md_note = md_note_builder(
            datetime_created=self.datetime_created,
            transcript=self.transcript,
            transcript_tldr=self.transcript_tldr,
            file_path_voice_memo_processed=self.file_path_voice_memo_processed,
        )
        with open(str(self.file_path_markdown), "w") as file:
            file.write(self.md_note)
