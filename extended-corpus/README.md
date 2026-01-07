# 数据集文件格式说明文档

## 1. 概述

该 JSON 文件由一个对象数组组成，数组中的每一个对象代表一个独立的重构样本案例。每个案例包含源代码位置、版本控制信息、重构前后的方法详情、标准答案（Oracle）以及 LLM 的实验数据。

## 2. 字段详细定义

### 2.1. 基础标识与版本信息 (Identity & Version Control)

这些字段用于在 Git 仓库中唯一定位代码片段。

| 属性名          | 类型    | 描述                                                             |
| :-------------- | :------ | :--------------------------------------------------------------- |
| `ID`            | Integer | 该重构样本在数据集中的唯一标识符。                               |
| `projectName`   | String  | 代码所属的 GitHub 项目名称（例如 `bennidi/mbassador`）。         |
| `filename`      | String  | 发生重构的源文件相对路径。                                       |
| `sha`           | String  | 当前数据点对应的 Git 提交哈希。                                  |
| `ParentSHA`     | String  | 当前提交的父提交哈希。                                           |
| `sha_ef`        | String  | 提取函数提交 (Extract Function SHA)：实际发生重构操作的提交 ID。 |
| `sha_before_ef` | String  | 重构前提交：重构操作发生之前的代码版本 ID。                      |
| `url`           | String  | 指向 GitHub 具体代码行的 URL 链接。                              |

### 2.2. 宿主方法信息 (Host Method Info)

描述重构前包含所有逻辑的原始大方法（即“宿主”）。

| 属性名               | 类型    | 描述                                      |
| :------------------- | :------ | :---------------------------------------- |
| `host_class_name`    | String  | 宿主方法所属的完整类名。                  |
| `host_functionName`  | String  | 宿主方法的名称。                          |
| `host_start_line`    | Integer | 宿主方法在源文件中的起始行号。            |
| `host_end_line`      | Integer | 宿主方法在源文件中的结束行号。            |
| `length_host`        | Integer | 宿主方法的代码行数（LOC）。               |
| `host_parameter`     | Array   | 宿主方法的参数列表（包含 name 和 type）。 |
| `host_start_off_set` | Integer | 宿主方法在文件中的起始字符偏移量。        |
| `host_end_off_set`   | Integer | 宿主方法在文件中的结束字符偏移量。        |

### 2.3. 被提取方法信息 (Extracted Method Info)

描述从宿主方法中被分离出来的新方法代码块。

| 属性名                          | 类型    | 描述                                             |
| :------------------------------ | :------ | :----------------------------------------------- |
| `extracted_method_functionName` | String  | 被提取出来的新方法的名称（或重构后的目标名称）。 |
| `extracted_method_start_line`   | Integer | 被提取代码块的起始行号。                         |
| `extracted_method_end_line`     | Integer | 被提取代码块的结束行号。                         |
| `length_extracted`              | Integer | 被提取代码块的长度（行数）。                     |
| `extracted_method_parameter`    | Array   | 提取出的新方法所需的参数列表。                   |
| `extracted_code_range_...`      | Object  | 包含文件路径、起止行列及偏移量的详细位置对象。   |
| `automatable`                   | Boolean | 标记该重构是否被判定为可完全自动化执行。         |

### 2.4. 标准答案 / 真值 (Oracle)

基于人类开发者实际提交的重构结果，作为评估 LLM 的基准。

| 属性名               | 类型    | 描述                                |
| :------------------- | :------ | :---------------------------------- |
| `oracle`             | Object  | 包含基准数据的对象。                |
| └ `loc`              | Integer | 人类开发者提取的代码行数。          |
| └ `line_start / end` | Integer | 人类开发者实际提取的起始/结束行号。 |
| └ `hf_body_loc`      | Integer | 重构前的宿主方法体行数。            |

### 2.5. LLM 实验数据 (LLM Multishot Data)

记录使用大语言模型进行重构建议的实验过程数据。

- **`llm_multishot_data`**: 这是一个对象，通常以温度参数为键（如 `"temperature_1.2"`），值为一个数组，数组中包含多次尝试（Shot）的数据。

**单次尝试（Shot）的数据结构：**

- `llm_raw_response`: (String) 完整的对话日志，包含系统提示词（System Prompt）、用户输入代码（User Prompt）以及 LLM 的原始回复。
- `response_extracted`: (String) 从 LLM 回复中解析出的 JSON 格式建议（只包含建议的函数名和起止行号）。
- `new-choices`: (String) 当前尝试中 LLM 提出的具体重构选择。
- `all-choices`: (String) 实验过程中累积的所有去重后的选择集合。
- `llm_processing_time`: (Float) 模型推理耗时（毫秒）。
- `response_parse_failed`: (Boolean) 标记 LLM 的回复是否无法被解析为有效的 JSON。

### 2.6. 排名与评估样本 (JetGPT Ranking Samples)

这部分是对 LLM 生成的多个候选项进行筛选和排序的结果。

- `jetgpt_ranking_samples`: 包含不同筛选策略（如 `IF_BODY`, `PREV_ASSIGNMENT` 等启发式规则）下的评估结果。
- `rank_by_size / popularity / heat`: 根据代码大小、出现频率或热度对候选重构方案进行排序的列表。
- `application_result`: 标记该建议是否能成功应用（如 `"OK"`）。
- `overlap`: 建议代码与 Oracle（标准答案）的重叠行数，用于衡量准确性。

### 2.7. 传统工具对比 (JExtract Result)

- `jextract_result`: 记录使用传统静态分析工具（JExtract）对同一代码段进行分析的结果，通常用于与 LLM 的结果进行对比（例如 result: `"UNMATCHED"` 表示传统工具未能识别出该重构机会）。




以`bennidi/mbassador`为例：
1. publish 方法重构
重构前：https://github.com/bennidi/mbassador/tree/d08470c339d317693d86b3efc356e16b1f16ad97
重构后：https://github.com/bennidi/mbassador/tree/fca9c6017cb8210a7dd216388bf66e7af3bfd45e

2. finalize 方法重构
重构前：https://github.com/bennidi/mbassador/tree/ffb5d01b70c5999379f53f150cf056423c30a089
重构后：https://github.com/bennidi/mbassador/tree/95c5d8e535d0dc0c36438defd45f9917f124f713