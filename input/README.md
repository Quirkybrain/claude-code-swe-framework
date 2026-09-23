# Project Asset Pool (原始输入资产池)

`input/` 存放项目目前已有的所有原始资料。它不仅限于需求文档，还可以包含旧代码、设计图、架构草稿、API 规范及团队规则。

---

## 🚀 3 秒极速放置指南（我该把资料放哪？）

如果你第一次使用本框架，不必纠结深层子目录，按照你手头的资料类型快速放置即可：

| 你手头拥有的资料 | 推荐放置位置 | 说明与建议 |
|---|---|---|
| **只有一段想法 / 简要一句话需求** | 直接在 `input/` 根目录建 `requirements.md` | 或直接在启动 Claude 时通过自然语言输入，框架会自动摄取 |
| **完整的需求文档 / PRD / 用户故事** | 放入 [`input/requirements/`](requirements/) | 支持 Markdown、TXT、PDF、DOCX 等常见文档格式 |
| **成熟的存量业务代码** | **直接保留在项目根目录**，无需移动！ | 若希望以独立外部包形式引入，才放入 [`input/existing/`](existing/) |
| **API 接口文档 / Swagger / OpenAPI** | 放入 [`input/api/`](api/) | 支持 JSON、YAML、Markdown 等格式 |
| **架构草图 / 系统设计 / 拓扑图** | 放入 [`input/architecture/`](architecture/) | 支持图片、Mermaid 或文本描述 |
| **UI 原型 / 设计稿 / 页面流程图** | 放入 [`input/design/`](design/) | 支持线框图、截图或设计说明 |
| **数据字典 / 数据库表结构 / DDL** | 放入 [`input/data/`](data/) | 支持 SQL、Schema 定义或数据模型说明 |
| **团队统一工程/编码/测试规范** | 放入 [`input/standards/`](standards/README.md) | 统一规范源，详见 [standards/README.md](standards/README.md) |
| **💡 随便什么资料，不知道放哪个目录** | **直接丢在 `input/` 根目录**！ | **框架会自动解析内容语义进行归类，路径放错零惩罚！** |

---

## 推荐目录结构

```text
input/
├── requirements/      # 需求规格说明书、PRD、用户故事、功能清单
├── architecture/      # 现有架构方案、拓扑图、技术选型备忘
├── design/            # UI 界面原型、交互流程图、视觉参考
├── api/               # API 接口契约、OpenAPI/Swagger、Protobuf
├── data/              # 数据库 DDL、Schema 定义、数据字典、示例数据
├── standards/         # 团队级编码、测试、安全规范（见 standards/README.md）
├── existing/          # 存量代码快照或外部遗留系统依赖
├── tests/             # 已有测试用例、测试报告、缺陷日志
├── uml/               # UML 建模图（时序图、类图、用例图等）
├── project/           # 商业背景、立项报告、利益相关者诉求
├── competitors/       # 竞品分析、行业参考基准
├── references/        # 权威参考资料、第三方技术文档
└── other/             # 未分类的其他杂项资料
```

---

## 资产识别原则 (Recognition Principle)

1. **内容优先，路径仅作参考**：框架的 `project-intake` 技能会深度扫描文件内容，而非仅凭文件名或文件夹做出判断。
2. **原始资产只读保护**：框架不会擅自修改或删除 `input/` 中的原始资料。
3. **安全红线**：严禁在 `input/` 中放入真实数据库密码、生产环境 Token、私钥或敏感个人隐私数据。
