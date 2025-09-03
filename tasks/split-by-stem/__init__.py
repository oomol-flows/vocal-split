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
    vocals: str
    drums: str
    guitar: str
    piano: str
    bass: str
    other: str
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    """
    将音频分离为不同音轨（人声、鼓、吉他、钢琴、贝斯、其他）
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
    model = 'htdemucs_6s'
    try:
        demucs.separate.main([
            "--mp3", 
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
    
    # 定义音轨文件映射
    stem_outputs = {
        "vocals": f"{output_name}_vocals.mp3",
        "drums": f"{output_name}_drums.mp3", 
        "guitar": f"{output_name}_guitar.mp3",
        "piano": f"{output_name}_piano.mp3",
        "bass": f"{output_name}_bass.mp3",
        "other": f"{output_name}_other.mp3"
    }
    
    # 构建结果字典
    results = {}
    
    for stem_name, filename in stem_outputs.items():
        file_path = output_model_dir / filename
        if file_path.exists():
            path_str = str(file_path)
            results[stem_name] = path_str
            context.output(stem_name, path_str)
        else:
            # 如果文件不存在，返回空字符串
            results[stem_name] = ""
            context.output(stem_name, "")
    
    return results

