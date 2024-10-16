# import whisper
import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
from voice2md.logger_config import setup_logger
from voice2md.voice_memo import VoiceMemo
import whisper
from tinydb import TinyDB
from datetime import datetime

logger = setup_logger(__name__)


def load_environment():
    """
    Loads environment variables from .env file.

    Returns:
        dict: A dictionary containing paths for processed voice memos and markdown files.
    """
    load_dotenv()
    return {
        "path_voice_memos_original": Path(os.getenv("PATH_VOICE_MEMOS_ORIGINAL")),
        "path_voice_memos_processed": Path(os.getenv("PATH_VOICE_MEMOS_PROCESSED")),
        "path_markdown": Path(os.getenv("PATH_MARKDOWN")),
        "path_db": Path(os.getenv("PATH_DB")),
    }


def setup_directories(paths):
    """
    Creates necessary directories for storing processed voice memos and markdown files.

    Args:
        paths (dict): A dictionary containing paths for processed voice memos and markdown files.
    """
    paths["path_voice_memos_processed"].mkdir(parents=True, exist_ok=True)
    paths["path_markdown"].mkdir(parents=True, exist_ok=True)


def process_voice_memos(
    path_voice_memos_original: Path,
    path_voice_memos_processed: Path,
    path_markdown: Path,
    path_db: Path,
    asr_model,
    llm_client,
    llm_model: str = "llama3.2:3b",
    overwrite: bool = True,
    max_file_size_mb: float = 3.0,
    last_n_files: int = 4,
):
    """
    Process voice memos: transcribe, summarize, generate title, and store in database.

    Args:
        path_voice_memos_original (Path): Directory of original voice memos.
        path_voice_memos_processed (Path): Directory for processed voice memos.
        path_markdown (Path): Directory for markdown output.
        path_db (Path): Path to the database.
        asr_model: Automatic Speech Recognition model.
        llm_client: Language Model client.
        llm_model (str): Language Model name. Defaults to "llama3.2:3b".
        overwrite (bool): Whether to overwrite existing files. Defaults to True.
        max_file_size_mb (float): Maximum file size to process in MB. Defaults to 3.0.
        last_n_files (int): Number of recent files to process. Defaults to 4.

    Returns:
        None
    """
    db = TinyDB(path_db / "db.json")
    file_path_list_original = sorted(list(path_voice_memos_original.glob("*.m4a")))
    for file_path in file_path_list_original[-last_n_files:]:
        print(file_path)
        vm = VoiceMemo(file_path, path_voice_memos_processed, path_markdown)
        vm.parse_datetime_created()
        vm.create_file_path_voice_memo_processed()
        vm.get_file_size_mb()

        if vm.file_size_mb > max_file_size_mb:
            logger.info(
                f"Skipping {file_path} because it exceeds the maximum file size of {max_file_size_mb} MB"
            )
            continue

        # Get the processed file name without path and suffix
        processed_file_name = vm.file_path_voice_memo_processed.stem

        # Check if the processed file already exists
        if any(
            file.stem == processed_file_name
            for file in path_voice_memos_processed.iterdir()
        ):
            if not overwrite:
                logger.info(
                    f"Skipping {file_path} because {processed_file_name} already exists in processed directory and overwrite is False"
                )
                continue
            else:
                logger.info(
                    f"File {processed_file_name} exists in processed directory, but overwrite is True. Proceeding with transcription."
                )
        else:
            logger.info(f"Processing new file: {file_path}")

        vm.create_file_path_markdown()
        vm.save_voice_memo_processed()
        vm.transcribe(asr_model)
        logger.info(f"voice memo file: {vm.file_path_voice_memo_processed}.")
        vm.summarize(llm_client, llm_model)
        logger.info(f"summary: {vm.transcript_tldr}")
        vm.generate_title(llm_client, llm_model)
        logger.info(f"title: {vm.transcript_title}")
        vm.create_file_path_markdown()
        logger.info(vm.file_path_markdown)
        vm.save_transcription()

        db_item = {
            "file_name": processed_file_name,
            "file_path_original": str(vm.file_path_original),
            "file_path_voice_memo_processed": str(vm.file_path_voice_memo_processed),
            "file_path_markdown": str(vm.file_path_markdown),
            "datetime_created": vm.datetime_created.isoformat(),
            "file_size_mb": vm.file_size_mb,
            "transcript": vm.transcript,
            "transcript_tldr": vm.transcript_tldr,
            "transcript_title": vm.transcript_title,
            "datetime_recorded": datetime.now().isoformat(),
        }
        db.insert(db_item)
        logger.info(f"Persisted {processed_file_name} to database")


def main():
    paths = load_environment()
    setup_directories(paths)

    asr_model = whisper.load_model("medium")
    llm_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    llm_model = "llama3.2:3b"

    process_voice_memos(
        paths["path_voice_memos_original"],
        paths["path_voice_memos_processed"],
        paths["path_markdown"],
        paths["path_db"],
        asr_model,
        llm_client,
        llm_model,
        overwrite=True,
        max_file_size_mb=2.0,
        last_n_files=3,
    )


if __name__ == "__main__":
    main()
