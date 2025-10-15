from oocana import Context
import demucs.separate
import os
from pathlib import Path

#region generated meta
import typing
class Inputs(typing.TypedDict):
    audio_file: str
    output_dir: str
    outputBaseName: str | None
class Outputs(typing.TypedDict):
    vocals: typing.NotRequired[str]
    drums: typing.NotRequired[str]
    guitar: typing.NotRequired[str]
    piano: typing.NotRequired[str]
    bass: typing.NotRequired[str]
    other: typing.NotRequired[str]
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    """
    Separate audio into different tracks (vocals, drums, guitar, piano, bass, other)
    """
    input_path = Path(params["audio_file"])

    # Validate input file
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {params['audio_file']}")

    # Get input file base name
    input_basename = input_path.stem

    # Determine output file name
    output_name = params["outputBaseName"] or input_basename

    # Execute audio separation
    model = 'htdemucs_6s'
    try:
        demucs.separate.main([
            "--mp3",
            "-v",
            "-n", model,
            "-o", params["output_dir"],
            "--filename", f"{{track}}/{output_name}_{{stem}}.{{ext}}",
            str(input_path)
        ])
    except Exception as e:
        raise RuntimeError(f"Audio separation failed: {str(e)}")

    # Build output directory path
    output_model_dir = Path(params["output_dir"]) / model / input_basename

    if not output_model_dir.exists():
        raise RuntimeError(f"Output directory does not exist: {output_model_dir}")

    # Define stem file mapping
    stem_outputs = {
        "vocals": f"{output_name}_vocals.mp3",
        "drums": f"{output_name}_drums.mp3", 
        "guitar": f"{output_name}_guitar.mp3",
        "piano": f"{output_name}_piano.mp3",
        "bass": f"{output_name}_bass.mp3",
        "other": f"{output_name}_other.mp3"
    }

    # Build results dictionary
    results = {}

    for stem_name, filename in stem_outputs.items():
        file_path = output_model_dir / filename
        if file_path.exists():
            path_str = str(file_path)
            results[stem_name] = path_str
            context.output(stem_name, path_str)
        else:
            # If file does not exist, return empty string
            results[stem_name] = ""
            context.output(stem_name, "")
    
    return results

