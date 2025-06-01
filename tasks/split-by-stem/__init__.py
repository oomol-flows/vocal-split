#region generated meta
import typing
from oocana import Context
class Inputs(typing.TypedDict):
    input: str
    outputDir: str
    outputBaseName: str | None
class Outputs(typing.TypedDict):
    vocals: str
    drums: str
    guitar: str
    piano: str
    bass: str
    other: str
#endregion

from oocana import Context
import demucs.separate
import os

def main(params: Inputs, context: Context) -> None:
    print(params["input"], os.path.isfile(params["input"]))
    if not os.path.isfile(params["input"]):
        raise Exception(f"Input file does not exist: {params['input']}")
    f = os.path.basename(params["input"])
    inputBaseName= f.split('.')[0]

    outputName = inputBaseName
    if not params["outputBaseName"] == None:
        outputName = params["outputBaseName"]

    model = 'htdemucs_6s'
    demucs.separate.main(["--mp3", "-v", "-n", model, "-o", params["outputDir"], "--filename", "{track}/" + outputName + "_{stem}.{ext}", params["input"]])

    vocals: str = ""
    drums: str = ""
    guitar: str = ""
    piano: str = ""
    bass: str = ""
    other: str = ""
    for filename in os.listdir(params["outputDir"] + "/" + model + "/" + inputBaseName):
        print(filename)
        if filename == outputName + '_vocals.mp3':
            vocals = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("vocals", vocals)
        elif filename == outputName + '_drums.mp3':
            drums = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("drums", drums)
        elif filename == outputName + '_guitar.mp3':
            guitar = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("guitar", guitar)
        elif filename == outputName + '_piano.mp3':
            piano = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("piano", piano)
        elif filename == outputName + '_bass.mp3':
            bass = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("bass", bass)
        elif filename == outputName + '_other.mp3':
            other = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("other", other)

