#region generated meta
import typing
class Inputs(typing.TypedDict):
    input: str
    outputDir: str
    outputBaseName: str | None
class Outputs(typing.TypedDict):
    vocals: str
    no_vocals: str
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

    model = 'htdemucs'
    demucs.separate.main(["--mp3", "--two-stems", "vocals", "-v", "-n", model, "-o", params["outputDir"], "--filename", "{track}/" + outputName + "_{stem}.{ext}", params["input"]])

    vocals: str | None = None
    other: str | None = None
    for filename in os.listdir(params["outputDir"] + "/" + model + "/" + inputBaseName):
        print(filename)
        if filename == outputName + '_vocals.mp3':
            vocals = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("vocals", vocals)
        elif filename == outputName + '_no_vocals.mp3':
            other = params["outputDir"] + "/" + model + "/" + inputBaseName + "/" + filename
            context.output("no_vocals", other)

