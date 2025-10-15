from oocana import Context
import demucs.separate
import os
from pathlib import Path

#region generated meta
import typing
class Inputs(typing.TypedDict):
    audio_file: str
    output_dir: str | None
    output_base_name: str | None
class Outputs(typing.TypedDict):
    vocals: typing.NotRequired[str]
    no_vocals: typing.NotRequired[str]
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    """
    Separate audio into vocals and instrumental parts
    """
    input_path = Path(params["audio_file"])

    # Validate input file
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {params['audio_file']}")

    # Get input file base name
    input_basename = input_path.stem

    # Determine output file name
    output_name = params["output_base_name"] or input_basename

    # Determine output directory
    output_dir = params["output_dir"] or context.session_dir

    # Execute audio separation
    model = 'htdemucs'
    try:
        demucs.separate.main([
            "--mp3",
            "--two-stems", "vocals",
            "-v",
            "-n", model,
            "-o", output_dir,
            "--filename", f"{{track}}/{output_name}_{{stem}}.{{ext}}",
            str(input_path)
        ])
    except Exception as e:
        raise RuntimeError(f"Audio separation failed: {str(e)}")

    # Build output directory path
    output_model_dir = Path(output_dir) / model / input_basename

    if not output_model_dir.exists():
        raise RuntimeError(f"Output directory does not exist: {output_model_dir}")

    # Find output files
    vocals_file = output_model_dir / f"{output_name}_vocals.mp3"
    no_vocals_file = output_model_dir / f"{output_name}_no_vocals.mp3"

    if not vocals_file.exists():
        raise FileNotFoundError(f"Vocals file not found: {vocals_file}")
    if not no_vocals_file.exists():
        raise FileNotFoundError(f"Instrumental file not found: {no_vocals_file}")

    vocals_path = str(vocals_file)
    no_vocals_path = str(no_vocals_file)

    # Set outputs
    context.output("vocals", vocals_path)
    context.output("no_vocals", no_vocals_path)
    
    return {
        "vocals": vocals_path,
        "no_vocals": no_vocals_path
    }

