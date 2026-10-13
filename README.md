# Chess Tactics Workbook Generator

一个面向国际象棋战术训练的旧版题册生成器。项目从 PGN 数据集中读取 4,462 道将杀题，使用 Python 2 生成 LaTeX，再通过 XeLaTeX 输出包含棋盘、答案页以及可选动画/着色走法的 PDF。

## 功能

- 从 `4462.pgn` 解析题目、FEN、答案和先行方信息。
- 每页生成 6 题或 8 题的练习册布局。
- 混合新题、随机旧题、错题和“半错题”，其中错题会获得更高抽样权重。
- 生成文本棋盘、逐步动画棋盘或带走法箭头和落点着色的棋盘。
- 在练习页之后附加答案页。

## 项目结构

| 路径 | 用途 |
| --- | --- |
| `4462.pgn` | 原始的 4,462 道战术题数据 |
| `4462.txt` | `pgn2pydict.py` 生成的 Python 字典快照 |
| `pgn2pydict.py` | 将 PGN 转换为供生成器读取的字典 |
| `TextChessExciv1.py` | 生成静态文字版题册 |
| `AnimateChessExciv2.py` | 生成带逐步动画的题册 |
| `ColorChessExciv3.py` | 生成带箭头和着色的动画题册，使用 `jBACKUPDIR` |
| `ColorChessExciv3.1.py` | 最新版本，使用 `jTMP` 作为输出目录 |
| `helpGen.txt` | 练习进度、页面设置及错题列表 |
| `TeX/` | LaTeX 布局与成功编译样例 |
| `xskak/` | 项目开发时参考的 xskak/chessboard 文档和示例 |

## 运行环境

该项目保留了原始实现，依赖旧版工具链：

- Python 2.7（代码使用 `print` 语句和 `dict.iteritems()`）
- XeLaTeX
- LaTeX 宏包：`geometry`、`multicol`、`babel`（含 Indonesian 支持）、`animate`、`chessboard`、`xskak` 和 `hyperref`
- 可执行 `mv`、`rm` 的类 Unix shell；Windows 上可使用 Git Bash、MSYS2 或 WSL

当前机器只有 Python 3，且未安装 XeLaTeX，因此本次归档没有重新构建项目。

## 使用方法

1. 如需从 PGN 重新生成字典，在项目根目录运行：

   ```sh
   python2 pgn2pydict.py
   ```

2. 编辑 `helpGen.txt`：

   - `lastquestion`：上次完成到的题号
   - `wrong`：错题编号，以逗号分隔
   - `halfwrong`：部分答错的题号，以逗号分隔
   - `randsel`：每页抽取的复习题数
   - `questperpage`：每页题数，原始代码支持 6 或 8
   - `page`：本次生成的页数

3. 设置输出环境变量。最新版 `ColorChessExciv3.1.py` 使用 `jTMP`：

   ```sh
   export jTMP=/path/to/output
   python2 ColorChessExciv3.1.py
   ```

   `ColorChessExciv3.py` 则使用 `jBACKUPDIR`，并期望其中存在 `tmp/` 和 `HW/` 子目录。

4. 脚本成功后会更新 `helpGen.txt` 中的进度，并在目标目录生成 PDF。

> [!CAUTION]
> `4462.txt` 通过 `eval()` 读取，只应使用本项目自身生成且可信的文件。不要用来源不明的文件替换它。

## 历史与归档状态

- `TeX/test.log` 记录了 `test.pdf` 成功生成，原文件时间为 2016-10-28 12:51:18。
- 当前主程序的最后修改时间为 2019-01-02 12:44:36（`ColorChessExciv3.1.py`）。
- 本仓库的首次提交日期采用后者，以表示当前归档快照形成的时间；它不是对 2019 年当天实际存在 Git 提交的声明。

这是一个历史项目归档。若要在现代环境继续维护，建议先迁移到 Python 3、用 `ast.literal_eval()` 或 JSON 取代 `eval()`，并将 shell 文件操作改为 Python 标准库实现。

## 许可证

仓库中的原创脚本和模板采用 MIT 许可证，见 `LICENSE`。`4462.pgn` 战术题数据及由其生成的 `4462.txt` 来自第三方题库，来源尚未记录，不在 MIT 许可范围内；重新分发或用于其他用途前请自行确认原始数据的授权条款。
