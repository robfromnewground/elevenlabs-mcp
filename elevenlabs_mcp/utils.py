import os
import tempfile
from pathlib import Path
from datetime import datetime
from fuzzywuzzy import fuzz
import urllib.parse


class ElevenLabsMcpError(Exception):
    pass


def make_error(error_text: str):
    raise ElevenLabsMcpError(error_text)


def is_file_writeable(path: Path) -> bool:
    if path.exists():
        return os.access(path, os.W_OK)
    parent_dir = path.parent
    return os.access(parent_dir, os.W_OK)


def make_output_file(
    tool: str, text: str, output_path: Path, extension: str, full_id: bool = False
) -> str:
    """Generate output filename (returns just the filename, not full path)"""
    id = text if full_id else text[:5]
    output_file_name = f"{tool}_{id.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    return output_file_name


def make_output_path(
    output_directory: str | None, base_path: str | None = None
) -> Path:
    output_path = None
    if output_directory is None:
        output_path = Path.home() / "Desktop"
    elif not os.path.isabs(output_directory) and base_path:
        output_path = Path(os.path.expanduser(base_path)) / Path(output_directory)
    else:
        output_path = Path(os.path.expanduser(output_directory))
    if not is_file_writeable(output_path):
        make_error(f"Directory ({output_path}) is not writeable")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def find_similar_filenames(
    target_file: str, directory: Path, threshold: int = 70
) -> list[tuple[str, int]]:
    """
    Find files with names similar to the target file using fuzzy matching.

    Args:
        target_file (str): The reference filename to compare against
        directory (str): Directory to search in (defaults to current directory)
        threshold (int): Similarity threshold (0 to 100, where 100 is identical)

    Returns:
        list: List of similar filenames with their similarity scores
    """
    target_filename = os.path.basename(target_file)
    similar_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if (
                filename == target_filename
                and os.path.join(root, filename) == target_file
            ):
                continue
            similarity = fuzz.token_sort_ratio(target_filename, filename)

            if similarity >= threshold:
                file_path = Path(root) / filename
                similar_files.append((file_path, similarity))

    similar_files.sort(key=lambda x: x[1], reverse=True)

    return similar_files


def try_find_similar_files(
    filename: str, directory: Path, take_n: int = 5
) -> list[Path]:
    similar_files = find_similar_filenames(filename, directory)
    if not similar_files:
        return []

    filtered_files = []

    for path, _ in similar_files[:take_n]:
        if check_audio_file(path):
            filtered_files.append(path)

    return filtered_files


def check_audio_file(path: Path) -> bool:
    audio_extensions = {
        ".wav",
        ".mp3",
        ".m4a",
        ".aac",
        ".ogg",
        ".flac",
        ".mp4",
        ".avi",
        ".mov",
        ".wmv",
    }
    return path.suffix.lower() in audio_extensions


def handle_input_file(file_path: str, audio_content_check: bool = True) -> Path:
    if not os.path.isabs(file_path) and not os.environ.get("ELEVENLABS_MCP_BASE_PATH"):
        make_error(
            "File path must be an absolute path if ELEVENLABS_MCP_BASE_PATH is not set"
        )
    path = Path(file_path)
    if not path.exists() and path.parent.exists():
        parent_directory = path.parent
        similar_files = try_find_similar_files(path.name, parent_directory)
        similar_files_formatted = ",".join([str(file) for file in similar_files])
        if similar_files:
            make_error(
                f"File ({path}) does not exist. Did you mean any of these files: {similar_files_formatted}?"
            )
        make_error(f"File ({path}) does not exist")
    elif not path.exists():
        make_error(f"File ({path}) does not exist")
    elif not path.is_file():
        make_error(f"File ({path}) is not a file")

    if audio_content_check and not check_audio_file(path):
        make_error(f"File ({path}) is not an audio or video file")
    return path


def handle_large_text(
    text: str, max_length: int = 10000, content_type: str = "content"
):
    """
    Handle large text content by saving to temporary file if it exceeds max_length.

    Args:
        text: The text content to handle
        max_length: Maximum character length before saving to temp file
        content_type: Description of the content type for user messages

    Returns:
        str: Either the original text or a message with temp file path
    """
    if len(text) > max_length:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as temp_file:
            temp_file.write(text)
            temp_path = temp_file.name

        return f"{content_type.capitalize()} saved to temporary file: {temp_path}\nUse the Read tool to access the full {content_type}."

    return text


def parse_conversation_transcript(transcript_entries, max_length: int = 50000):
    """
    Parse conversation transcript entries into a formatted string.
    If transcript is too long, save to temporary file and return file path.

    Args:
        transcript_entries: List of transcript entries from conversation response
        max_length: Maximum character length before saving to temp file

    Returns:
        tuple: (transcript_text_or_path, is_temp_file)
    """
    transcript_lines = []
    for entry in transcript_entries:
        speaker = getattr(entry, "role", "Unknown")
        text = getattr(entry, "message", getattr(entry, "text", ""))
        timestamp = getattr(entry, "timestamp", None)

        if timestamp:
            transcript_lines.append(f"[{timestamp}] {speaker}: {text}")
        else:
            transcript_lines.append(f"{speaker}: {text}")

    transcript = (
        "\n".join(transcript_lines) if transcript_lines else "No transcript available"
    )

    # Check if transcript is too long for LLM context window
    if len(transcript) > max_length:
        # Create temporary file
        temp_file = tempfile.SpooledTemporaryFile(
            mode="w+", max_size=0, encoding="utf-8"
        )
        temp_file.write(transcript)
        temp_file.seek(0)

        # Get a persistent temporary file path
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as persistent_temp:
            persistent_temp.write(transcript)
            temp_path = persistent_temp.name

        return (
            f"Transcript saved to temporary file: {temp_path}\nUse the Read tool to access the full transcript.",
            True,
        )

    return transcript, False


def generate_file_url(filename: str, base_url: str | None = None) -> str:
    """
    Generate HTTP URL for serving a file.
    
    Args:
        filename: The filename to serve
        base_url: Base URL of the server (defaults to environment variable)
    
    Returns:
        str: Complete HTTP URL for the file
    """
    if base_url is None:
        # Check for Railway public URL first
        railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if railway_url:
            base_url = f"https://{railway_url}"
        else:
            # Fallback to host/port
            host = os.getenv("HOST", "localhost")
            port = os.getenv("PORT", "3000")
            protocol = "https" if host != "localhost" and host != "127.0.0.1" else "http"
            base_url = f"{protocol}://{host}:{port}"
    
    # Ensure filename is URL-safe
    safe_filename = urllib.parse.quote(filename)
    return f"{base_url}/files/{safe_filename}"


def cleanup_old_files(directory: Path, max_age_hours: int = 24) -> int:
    """
    Clean up files older than max_age_hours from the specified directory.
    
    Args:
        directory: Directory to clean up
        max_age_hours: Maximum age in hours before files are deleted
    
    Returns:
        int: Number of files deleted
    """
    if not directory.exists():
        return 0
    
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    for file_path in directory.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except OSError:
                    pass  # Failed to delete, skip
    
    return deleted_count
