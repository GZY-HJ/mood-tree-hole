# 设计规范 · 情绪树洞

以下色值、字体栈都直接取自 `index.html` 里的 `:root` 与 `:root.dark` 两套 CSS 变量，改主题只需要改这两个块。

## 1. 浅色主题（默认）

| 变量 | 色值 | 用途 |
|---|---|---|
| `--canvas` | `#f5efe9` | 页面底色（暖米色） |
| `--surface` | `#ffffff` | 卡片、输入框底色 |
| `--surface-soft` | `#f6efe7` | 次级卡片、辅助分区 |
| `--surface-deep` | `#efe5da` | 分组底色、hover 状态 |
| `--ink` | `#3d333b` | 正文与标题（墨色） |
| `--ink-soft` | `#8a7f86` | 次要说明、时间戳 |
| `--ink-faint` | `#b7adb3` | 占位符、禁用态 |
| `--line` | `#e9ddd2` | 描边、分割线 |
| `--accent` | `#c85f74` | 主强调（豆沙玫瑰）：选中情绪、主按钮 |
| `--accent-deep` | `#ae4b61` | 按下态、深色强调 |
| `--accent-soft` | `#f9e6e6` | 强调色浅底（提示条、标签底） |
| `--accent-ink` | `#ffffff` | 强调色上的文字 |
| `--gold` | `#c79a4a` | 数据高亮（图表主色） |
| `--green` | `#4f8f6f` | 正向状态、成功提示 |
| `--blue` | `#5b7fb0` | 辅助信息 |
| `--focus` | `#a4455b` | 键盘焦点环 |

## 2. 深色主题（`prefers-color-scheme: dark` 或手动切换）

| 变量 | 色值 |
|---|---|
| `--canvas` | `#141019` |
| `--surface` | `#211a27` |
| `--surface-soft` | `#2b2231` |
| `--surface-deep` | `#332838` |
| `--ink` | `#ece4ea` |
| `--ink-soft` | `#a89dab` |
| `--ink-faint` | `#6f6572` |
| `--line` | `#3a303f` |
| `--accent` | `#e1788d` |
| `--accent-deep` | `#ea90a2` |
| `--accent-soft` | `#3d2a31` |
| `--accent-ink` | `#2a161b` |
| `--gold` | `#d9b76a` |
| `--green` | `#7fbf9b` |
| `--blue` | `#8aa9d8` |
| `--focus` | `#ee9aac` |

深色不是把浅色反转，而是重新配了一组：底色偏紫黑，强调色提亮两档保证在暗底上仍然可读。切换结果存在 `mood-theme`，下次打开沿用。

## 3. 字体

```css
--font-ui: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
           "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
```

只用系统字体，不引外部字体文件——这是「零外链」的一部分。中文优先落到苹方 / 冬青黑 / 微软雅黑，数字和代码片段用等宽栈。

## 4. 圆角与阴影

| 变量 | 值 | 用途 |
|---|---|---|
| `--radius` | `18px` | 卡片、弹窗 |
| `--radius-sm` | `12px` | 输入框、标签、按钮 |
| `--shadow-sm` | `0 1px 2px rgba(61,51,59,.05)` | 轻浮起 |
| `--shadow` | `0 2px 6px rgba(61,51,59,.05), 0 14px 34px rgba(61,51,59,.08)` | 常规卡片 |
| `--shadow-lg` | `0 6px 18px rgba(61,51,59,.08), 0 24px 60px rgba(61,51,59,.12)` | 弹窗、浮层 |

阴影统一用墨色（`#3d333b`）加低透明度，不用纯黑，避免在暖米色底上发灰。

## 5. 情绪标签

五种情绪是 emoji + 中文的组合，不加额外色块：

| 情绪 | 展示文案 |
|---|---|
| 平静安然 | `😌 平静安然` |
| 低落难过 | `😔 低落难过` |
| 焦虑紧绷 | `😰 焦虑紧绷` |
| 压抑愤怒 | `😡 压抑愤怒` |
| 温柔期待 | `✨ 温柔期待` |

未选中时是白底 + `--line` 描边；选中后底色换成 `--accent`、文字换成 `--accent-ink`、加粗。一屏内同权重按钮不超过 5 个，避免用户在选择上耗时间。

## 6. 版式取向

- 单列居中，最大宽度收在 720px 附近，窄屏自动收窄留白
- 卡片之间留 16–20px，视觉上用底色差（`--surface` / `--surface-soft`）分层，不靠粗描边
- 标题 20–24px，正文 15–16px，行高 1.6 左右；说明文字一律用 `--ink-soft`
- 只用一种强调色（豆沙玫瑰），数据高亮才用金色，不做多彩渐变
- 不用大圆角「气泡」堆叠，也不用投影堆层次，保持安静的观感

海报、幻灯片和这个页面共用同一套色值：暖米色底 + 豆沙玫瑰强调 + 墨色文字，是它们看起来像一套的原因。
