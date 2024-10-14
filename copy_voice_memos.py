import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

from voice2md.logger_config import setup_logger

logger = setup_logger(__name__)


def main():
    load_dotenv()

    MAX_FILE_SIZE_MIRROR = (
        100.0  # in MB, this is roughly the size of a 3 hour audio file
    )

    path_voice_memos_apple = Path(os.getenv("PATH_VOICE_MEMOS_APPLE"))
    path_voice_memos_original = Path(os.getenv("PATH_VOICE_MEMOS_ORIGINAL"))
    path_voice_memos_original.mkdir(parents=True, exist_ok=True)

    get_voice_memos(
        path_voice_memos_apple, path_voice_memos_original, "m4a", MAX_FILE_SIZE_MIRROR
    )


def get_voice_memos(
    source_dir: Path,
    destination_dir: Path,
    suffix: str = "m4a",
    max_size_mb: float = 100.0,
) -> dict:
    """Copies voice memo files from source to destination directory, filtering by maximum size and avoiding duplicates.

    Args:
        source_dir: Source directory path.
        destination_dir: Destination directory path.
        suffix: File extension to copy. Defaults to "m4a".
        max_size_mb: Maximum file size in megabytes to copy. Defaults to 100.0.

    Returns:
        dict: Operation summary.
    """
    import hashlib

    destination_dir.mkdir(parents=True, exist_ok=True)
    files = list(source_dir.glob(f"*.{suffix}"))
    copied_files = []
    skipped_files = []
    unchanged_files = []

    logger.info(
        f"Copying files smaller than {max_size_mb} MB from {source_dir} to {destination_dir}"
    )
    for file_path in files:
        if file_path.is_file():
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb < max_size_mb:
                dest_file_path = destination_dir / file_path.name
                if dest_file_path.exists():
                    # Compare file hashes
                    with open(file_path, "rb") as f:
                        source_hash = hashlib.md5(f.read()).hexdigest()
                    with open(dest_file_path, "rb") as f:
                        dest_hash = hashlib.md5(f.read()).hexdigest()

                    if source_hash == dest_hash:
                        unchanged_files.append(file_path.name)
                        logger.info(
                            f"Skipped unchanged file {file_path} ({file_size_mb:.2f} MB)"
                        )
                        continue

                shutil.copy2(file_path, destination_dir)
                copied_files.append(file_path.name)
                logger.info(f"Copied file {file_path} ({file_size_mb:.2f} MB)")
            else:
                skipped_files.append(file_path.name)
                logger.info(
                    f"Skipped file {file_path} ({file_size_mb:.2f} MB) due to size"
                )

    return {
        "total_files": len(files),
        "copied_files": len(copied_files),
        "skipped_files": len(skipped_files),
        "unchanged_files": len(unchanged_files),
        "copied_file_names": copied_files,
        "skipped_file_names": skipped_files,
        "unchanged_file_names": unchanged_files,
    }


if __name__ == "__main__":
    main()
