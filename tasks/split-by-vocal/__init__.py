from oocana import Context
import demucs.separate
import os
from pathlib import Path

#region generated meta
import typing
class Inputs(typing.TypedDict):
    input: str
    outputDir: str
    outputBaseName: str | None
class Outputs(typing.TypedDict):
    vocals: typing.NotRequired[str]
    no_vocals: typing.NotRequired[str]
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    """
    将音频分离为人声和非人声部分
    """
    input_path = Path(params["input"])
    
    # 验证输入文件
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"输入文件不存在: {params['input']}")
    
    # 获取输入文件基础名称
    input_basename = input_path.stem
    
    # 确定输出文件名称
    output_name = params["outputBaseName"] or input_basename
    
    # 执行音频分离
    model = 'htdemucs'
    try:
        demucs.separate.main([
            "--mp3", 
            "--two-stems", "vocals", 
            "-v", 
            "-n", model, 
            "-o", params["outputDir"], 
            "--filename", f"{{track}}/{output_name}_{{stem}}.{{ext}}", 
            str(input_path)
        ])
    except Exception as e:
        raise RuntimeError(f"音频分离失败: {str(e)}")
    
    # 构建输出目录路径
    output_model_dir = Path(params["outputDir"]) / model / input_basename
    
    if not output_model_dir.exists():
        raise RuntimeError(f"输出目录不存在: {output_model_dir}")
    
    # 查找输出文件
    vocals_file = output_model_dir / f"{output_name}_vocals.mp3"
    no_vocals_file = output_model_dir / f"{output_name}_no_vocals.mp3"
    
    if not vocals_file.exists():
        raise FileNotFoundError(f"人声文件未找到: {vocals_file}")
    if not no_vocals_file.exists():
        raise FileNotFoundError(f"非人声文件未找到: {no_vocals_file}")
    
    vocals_path = str(vocals_file)
    no_vocals_path = str(no_vocals_file)
    
    # 设置输出
    context.output("vocals", vocals_path)
    context.output("no_vocals", no_vocals_path)
    
    return {
        "vocals": vocals_path,
        "no_vocals": no_vocals_path
    }

