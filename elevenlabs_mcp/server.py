import os
from typing import Literal
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import (
    TextContent,
    EmbeddedResource,
)
from elevenlabs.client import ElevenLabs
from elevenlabs_mcp.model import McpVoice
from elevenlabs_mcp.utils import (
    make_error,
    make_output_path,
    make_output_file,
    handle_input_file,
)

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
base_path = os.getenv("ELEVENLABS_MCP_BASE_PATH")

if not api_key:
    raise ValueError("ELEVENLABS_API_KEY environment variable is required")

client = ElevenLabs(api_key=api_key)
mcp = FastMCP("ElevenLabs")


@mcp.tool(
    description="""Convert text to speech with a given voice and save the output audio file to a given directory.
    Directory is optional, if not provided, the output file will be saved to $HOME/Desktop of a user."""
)
def text_to_speech(
    text: str,
    voice_name: str | None = None,
    output_directory: str = "",
):
    """Convert text to speech with a given voice and save the output audio file to a given directory.

    Args:
        text (str): The text to convert to speech
        voice_name (str, optional): The name of the voice to use, if not provided uses first available voice
        output_path (str, optional): Directory where files should be saved.
            Defaults to $HOME/Desktop if not provided.

    Returns:
        List containing text content and audio data as embedded resource
    """
    voices = client.voices.search(search=voice_name)

    if len(voices.voices) == 0:
        make_error("No voices found with that name.")

    if voice_name is None:
        voice = voices.voices[0]
    else:
        voice = next((v for v in voices.voices if v.name == voice_name), None)

    if voice is None:
        make_error(f"Voice with name: {voice_name} does not exist.")

    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("tts", text, output_path, "mp3")

    audio_data = client.text_to_speech.convert(
        text=text,
        voice_id=voice.voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path / output_file_name, "wb") as f:
        f.write(audio_bytes)

    return TextContent(
        type="text",
        text=f"Success. File saved as: {output_path / output_file_name}. Voice used: {voice.name}",
    )


@mcp.tool(
    description="Transcribe speech from an audio file and either save the output text file to a given directory or return the text to the client directly."
)
def speech_to_text(
    input_file_path: str,
    language_code: str = "eng",
    diarize=False,
    save_transcript_to_file=True,
    return_transcript_to_client_directly=False,
    output_directory: str = "",
) -> TextContent:
    """Transcribe speech from an audio file using ElevenLabs API.

    Args:
        file_path: Path to the audio file to transcribe
        language_code: Language code for transcription (default: "eng" for English)

    Returns:
        TextContent containing the transcription
    """
    if not save_transcript_to_file and not return_transcript_to_client_directly:
        make_error("Must save transcript to file or return it to the client directly.")
    file_path = handle_input_file(input_file_path)
    if save_transcript_to_file:
        output_path = make_output_path(output_directory, base_path)
        output_file_name = make_output_file("stt", file_path.name, output_path, "txt")
    with file_path.open("rb") as f:
        audio_bytes = f.read()
    transcription = client.speech_to_text.convert(
        model_id="scribe_v1",
        file=audio_bytes,
        language_code=language_code,
        enable_logging=True,
        diarize=diarize,
        tag_audio_events=True,
    )

    if save_transcript_to_file:
        with open(output_path / output_file_name, "w") as f:
            f.write(transcription.text)

    if return_transcript_to_client_directly:
        return TextContent(type="text", text=transcription.text)
    else:
        return TextContent(
            type="text", text=f"Transcription saved to {output_path / output_file_name}"
        )


@mcp.tool(
    description="""Convert text description of a sound effect to sound effect with a given duration and save the output audio file to a given directory.
    Directory is optional, if not provided, the output file will be saved to $HOME/Desktop of a user.
    Duration must be between 0.5 and 5 seconds."""
)
def text_to_sound_effects(
    text: str, duration_seconds: float = 2.0, output_directory: str = ""
) -> list[TextContent | EmbeddedResource]:
    if duration_seconds < 0.5 or duration_seconds > 5:
        make_error("Duration must be between 0.5 and 5 seconds")
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("sfx", text, output_path, "mp3")

    audio_data = client.text_to_sound_effects.convert(
        text=text,
        output_format="mp3_44100_128",
        duration_seconds=duration_seconds,
    )
    audio_bytes = b"".join(audio_data)

    with open(output_path / output_file_name, "wb") as f:
        f.write(audio_bytes)

    return TextContent(
        type="text",
        text=f"Success. File saved as: {output_path / output_file_name}",
    )


@mcp.tool(description="List all available voices")
def list_voices() -> list[McpVoice]:
    """List all available voices.

    Returns:
        A formatted list of available voices with their IDs and names
    """
    response = client.voices.get_all()
    return [
        McpVoice(id=voice.voice_id, name=voice.name, category=voice.category)
        for voice in response.voices
    ]


@mcp.resource("voices://list")
def get_voices() -> list[McpVoice]:
    """Get a list of all available voices."""
    response = client.voices.get_all()
    return [
        McpVoice(id=voice.voice_id, name=voice.name, category=voice.category)
        for voice in response.voices
    ]


@mcp.tool(description="Search for voices by search term. Returns all voices if no search term is provided. Searches in name, description, labels and category.")
def search_voices(
    search: str | None = None,
    sort: Literal["created_at_unix", "name"] = "name",
    sort_direction: Literal["asc", "desc"] = "desc",
) -> list[McpVoice]:
    """Search for voices.

    Args:
        search: Search term to filter voices by. Searches in name, description, labels and category.
        sort: Which field to sort by. `created_at_unix` might not be available for older voices.
        sort_direction: Sort order, either ascending or descending.

    Returns:
        List of voices that match the search criteria.
    """
    response = client.voices.search(search=search, sort=sort, sort_direction=sort_direction)
    return [
        McpVoice(id=voice.voice_id, name=voice.name, category=voice.category)
        for voice in response.voices
    ]


@mcp.resource("voice://{voice_id}")
def get_voice(voice_id: str) -> McpVoice:
    """Get details of a specific voice."""
    response = client.voices.get_all()
    for voice in response.voices:
        if voice.voice_id == voice_id:
            return McpVoice(id=voice.voice_id, name=voice.name, category=voice.category)
    raise f"Voice with id: {voice_id} not found"


@mcp.tool(description="Clone a voice using provided audio files")
def voice_clone(
    name: str, files: list[str], description: str | None = None
) -> TextContent:
    voice = client.clone(name=name, description=description, files=files)

    return TextContent(
        type="text",
        text=f"""Voice cloned successfully:
        Name: {voice.name}
        ID: {voice.voice_id}
        Category: {voice.category}
        Description: {voice.description or "N/A"}
        Labels: {", ".join(voice.labels) if voice.labels else "None"}
        Preview URL: {voice.preview_url or "N/A"}
        Available for Cloning: {voice.fine_tuning.available_for_cloning}
            Fine Tuning Status: {voice.fine_tuning.status}""",
    )


@mcp.tool(
    description="Isolate audio from a file and save the output audio file to a given directory. Directory is optional, if not provided, the output file will be saved to $HOME/Desktop of a user."
)
def isolate_audio(
    input_file_path: str, output_directory: str = ""
) -> list[TextContent | EmbeddedResource]:
    file_path = handle_input_file(input_file_path)
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("iso", file_path.name, output_path, "mp3")
    with file_path.open("rb") as f:
        audio_bytes = f.read()
    audio_data = client.audio_isolation.audio_isolation(
        audio=audio_bytes,
    )
    audio_bytes = b"".join(audio_data)

    with open(output_path / output_file_name, "wb") as f:
        f.write(audio_bytes)

    return TextContent(
        type="text",
        text=f"Success. File saved as: {output_path / output_file_name}",
    )


@mcp.tool(
    description="Check the current subscription status. Could be used to measure the usage of the API."
)
def check_subscription() -> TextContent:
    subscription = client.user.get_subscription()
    return TextContent(type="text", text=f"{subscription.model_dump_json(indent=2)}")


if __name__ == "__main__":
    mcp.run()
