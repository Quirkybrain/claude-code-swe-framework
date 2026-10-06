# 国际化与多语言工程规范 (Internationalization Policy)

本规范定义了本框架中针对多语言（i18n, Internationalization）与本地化（l10n, Localization）的默认工程准则。

## 适用范围与默认触发条件

当用户在需求或任务 Prompt 中**仅提出“支持多语言”或“支持 i18n”，而未提供具体的自定义国际化架构方案时**：
* 工作流各智能体**默认全面激活并执行本规范**；
* 无需在 Clarification Gate 中就“如何实现多语言”进行重复确认，直接遵循本标准中的单一代码库、外部化独立语言包与动态键值查找方案；
* 若用户明确指定了特定框架规范（如必须通过 `input/standards/i18n.md` 自定义），则以用户显式规范为准。

---

## 核心工程原则

### 1. 单代码库铁律 (Single Codebase Principle)
* **严禁编写多版本业务代码**：绝对禁止为了支持不同语言而维护两套或多套应用代码（如分别维护“中文版代码”与“英文版代码”）；
* 业务逻辑、控制流、数据流以及 UI 组件结构全局唯一，严禁出现因语言版本导致的逻辑分叉与功能漂移。

### 2. 文案与逻辑彻底解耦 (Decoupled Resource Bundles)
* 业务逻辑、控制层、组件模板中**严禁硬编码**任何面向用户的展示文本（包括 UI 标签、按钮文案、校验报错、提示弹窗、系统通知等）；
* 所有用户可见文本一律抽取为语义化键（Semantic Key）；
* 代码中通过统一的翻译查找函数或模块（如 `t("key")`、`i18n.translate("key")`、`ResourceBundle`）进行动态获取。

### 3. 分语言独立文件存储 (Per-Locale Independent Files)
* 语言资源包按语言/区域（Locale）采用独立文件隔离存储，**严禁将所有语言文案杂糅在同一个巨型文件内**；
* 推荐标准目录与命名：
  ```text
  locales/ (或 resources/i18n/, public/locales/)
  ├── zh-CN.json   # 简体中文（源语言/基准语言包）
  ├── en-US.json   # 英语（美式）
  └── ja-JP.json   # 日语（按需扩展）
  ```
* **工程收益**：
  * **按需加载 (Code Splitting)**：前端或客户端仅需加载用户当前选中的语言包，减少带宽与首屏解析开销；
  * **翻译协作无冲突**：外部翻译团队或多成员更新特定语言时互不干扰，彻底避免 Git 巨型文件合并冲突。

### 4. 语义化键命名与插值规范 (Key Naming & Interpolation)
* **分层命名空间**：采用点分隔（Dot notation）或嵌套 JSON 对象建立层级结构，反映文案归属：
  * 页面与功能：`auth.login.title`、`dashboard.metrics.active_users`
  * 通用交互：`common.actions.confirm`、`common.actions.cancel`、`common.status.loading`
  * 校验与异常：`errors.validation.required`、`errors.network.timeout`
* **参数插值而非字符串拼接**：动态内容统一使用参数化模板（如 `{username}` 或 `{{count}}`），**严禁直接用 `+` 拼接字符串**，以适应不同自然语言的主谓宾/主宾谓语序差异：
  ```json
  // 正确：
  "welcome_user": "欢迎回来，{username}！"
  // 错误：
  "welcome_prefix": "欢迎回来，" // 严禁在代码中写 "welcome_prefix" + user + "！"
  ```
* **安全回退机制 (Fallback Strategy)**：
  * 必须配置兜底默认语言（Fallback Locale，如源语言 `zh-CN` 或通用 `en-US`）；
  * 当某个 key 在目标语言中缺失时，平滑降级展示兜底语言文本，严禁直接抛出未捕获异常或展示空白界面。

---

## 多智能体工作流分工 (Agent Lifecycle)

在全流程开发中，各专业角色遵守以下协同契约：

| 阶段 / Agent 角色 | 核心职责与交付要求 |
| :--- | :--- |
| **需求分析**<br>`requirements-analyst` | - 识别用户多语言意图，若未指明具体语种，默认确立为 **基准源语言 + 英文（如 zh-CN 与 en-US）**；<br>- 在需求与验收标准（AC）中显式写入非功能需求：采用外部化 i18n 资源包，代码零硬编码字符串，支持动态切换。 |
| **架构设计**<br>`solution-architect` | - 在架构设计与详细设计中定义 i18n 模块架构与目录契约（如 `locales/{locale}.json`）；<br>- 确定适配当前技术栈的成熟轻量库（如 React `react-i18next`、Vue `vue-i18n`、Python `gettext`/`Babel`、Java `ResourceBundle`、Go `golang.org/x/text`）；<br>- 严禁批准任何创建多套代码分支的架构提案。 |
| **交互与体验**<br>`experience-designer` | - UI 容器必须具备弹性伸缩能力，预留 **20%~40% 文本长度膨胀空间**（应对德文/法文等长单词语言）；<br>- 避免使用固定像素宽度按钮，确保文本换行与省略样式优雅；按需预留 LTR / RTL 支持。 |
| **编码实现**<br>`implementation-engineer` | - 严格遵循架构契约，所有新建与修改的 UI/提示文本均抽取至语言文件；<br>- 同步补充所有目标语言文件中的对应 key，杜绝产生半成品或漏项；<br>- 业务代码中仅调用 `t(key)`，不包含具体展示字符。 |
| **质量审查**<br>`quality-reviewer` | - **静态审查**：检索业务代码与模板，严格拦截未抽取的硬编码字符串；<br>- **对称性审查 (Key Parity)**：比对所有语言文件，确保 key 集合 100% 对齐，无遗漏漏译；<br>- **分支审查**：核验是否存在多语言代码分叉副本。 |
| **系统测试**<br>`test-engineer` | - 验证语言切换上下文响应正常，语言包切换后无需重启即可实时重渲染（或平滑刷新）；<br>- 验证缺失 key 时的 Fallback 降级逻辑与参数插值正确性。 |

---

## 示例实现模式 (Reference Implementations)

### 模式 A：现代前端 (JavaScript / TypeScript)
```typescript
// 1. 语言资源文件 locales/zh-CN.json
{
  "common": { "submit": "提交", "cancel": "取消" },
  "user": { "greeting": "你好，{name}！" }
}

// 2. 语言资源文件 locales/en-US.json
{
  "common": { "submit": "Submit", "cancel": "Cancel" },
  "user": { "greeting": "Hello, {name}!" }
}

// 3. 业务组件使用（代码只有一套）
import { useTranslation } from 'react-i18next';

export function UserGreeting({ username }: { username: string }) {
  const { t } = useTranslation();
  return <h1>{t('user.greeting', { name: username })}</h1>;
}
```

### 模式 B：轻量级命令行工具 / 脚本 (Python)
```python
import json
import os
from pathlib import Path

class I18n:
    def __init__(self, locale_dir: str = "locales", default_lang: str = "en-US"):
        self.locale_dir = Path(locale_dir)
        self.default_lang = default_lang
        self.translations = {}
        self.load_all()

    def load_all(self):
        for file in self.locale_dir.glob("*.json"):
            lang = file.stem
            with open(file, "r", encoding="utf-8") as f:
                self.translations[lang] = json.load(f)

    def t(self, key: str, lang: str = None, **kwargs) -> str:
        lang = lang or self.default_lang
        bundle = self.translations.get(lang, self.translations.get(self.default_lang, {}))
        
        # 支持点分隔嵌套查找: auth.login.title
        val = bundle
        for part in key.split("."):
            if isinstance(val, dict):
                val = val.get(part)
            else:
                val = None
                break
        
        # 降级回退
        if val is None and lang != self.default_lang:
            return self.t(key, lang=self.default_lang, **kwargs)
        if val is None:
            return key
        return val.format(**kwargs) if kwargs else val
```
