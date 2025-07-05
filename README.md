# GUI 提取工具

用于从 3dmigoto 生成的帧转储中提取某些二次元游戏的模型数据。查看 [3DMigoto 寻模与转储教程](https://leotorrez.github.io/modding/guides/hunting) 获取快速上手指南。

## 环境要求
- **Python ≥ 3.9**
- texconv.exe（已包含在 modules 目录中）
- texdiag.exe（已包含在 modules 目录中）

> [!警告]
> texconv.exe 和 texdiag.exe 用于转换和检查 .dds 文件，这两个工具已包含在 modules 目录中。如果你担心未知的 .exe 文件被捆绑，这是非常合理的安全考虑，请随意删除它们，或自行从微软 DirectX 官方仓库获取：https://github.com/microsoft/DirectXTex/releases/tag/jun2024

## 运行方法

下载压缩包并解压。你可以双击 `launch.bat` 自动查找系统中的最新 Python 版本并运行程序，或者手动用 Python 运行 `collect.py`。

## 特别感谢以下开发者的直接或间接贡献：
- [**SilentNightSound**](https://github.com/SilentNightSound/)：如果没有 [最初的 collect 脚本](https://github.com/SilentNightSound/GI-Model-Importer/blob/main/Tools/genshin_3dmigoto_collect.py) 和 GIMI，所有这些都不可能实现。
- [**SinsOfSeven**](https://github.com/SinsOfSeven/)：目标转储与数据分析的先驱
- [**Gustav0**](https://github.com/Seris0/)：测试方面提供了巨大帮助
- [**Satan1c**](https://github.com/Satan1c)：[教程](https://leotorrez.github.io/modding/guides/hunting) 编写
- [**LeoMods**](https://github.com/leotorrez/)：XXMI 工具及[教程网站](https://leotorrez.github.io/modding/) 编写
- [**DarkStarSword**](https://github.com/DarkStarSword)、[**Bo3b**](https://github.com/bo3b) 和 Chiri：3DMigoto 作者

<div>
    <img src='resources/images/icons/Sucrose.png'/>
    <img src='resources/images/icons/Fofo.png'/>
    <img src='resources/images/icons/Corin.png'/>
    <img src='resources/images/icons/Mobius.png'/>
</div>
