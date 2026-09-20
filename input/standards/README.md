# Project Standards

把组织、团队或项目长期遵守的工程规范放在本目录。文件名和格式不固定，Claude Code 会结合内容识别其含义。

常见示例：

```text
input/standards/
├── coding.md
├── testing.md
├── security.md
├── api.md
└── documentation.md
```

也可以使用其他名称、目录或文件格式，例如团队工程手册、合规要求、架构原则、UI 规范或发布流程。不要为了匹配示例而重命名已有标准。

建议每份标准明确：

- 适用范围和优先级；
- 必须、禁止和推荐事项；
- 版本、生效日期和维护者；
- 例外或豁免的授权方式；
- 与其他标准冲突时的处理原则。

Project Intake 会发现这些来源，分析/架构责任会将目标相关内容统一整理为带来源引用的 Project Constraints。其他 Agent 应使用这些已整理约束，而不是分别重新解释原始规范。

不要放入密码、Token、私钥、生产凭据、真实敏感数据或不应进入仓库的内部材料。无法共享的标准可以在 `config/project.md` 中记录其摘要、访问限制或外部引用。
