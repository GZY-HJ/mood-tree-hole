# 架构说明 · 情绪树洞

这个项目只有一个文件 `index.html`（73,778 字节 / 966 行），没有构建步骤、没有依赖、没有网络请求。本文件说明它内部是怎么组织的，方便后续维护和面试讲解。

## 1. 文件内部分区

```
index.html
├── <head>
│   └── 一个 <style>：全部样式（含 :root 设计变量与 :root.dark 深色主题）
├── <body>
│   ├── header            标题、座右铭、主题切换按钮
│   ├── .quote            顶部语录卡（6 秒轮播）
│   ├── .navtab           四个 tab 按钮（data-tab=home/advise/square/me）
│   ├── #pt-home          树洞：情绪选择、心声输入、字数计数、温柔回信
│   ├── #pt-advise        AI 劝导：话题输入与两段式回应
│   ├── #pt-square        广场：留言列表、匿名开关、发布
│   ├── #pt-me            我的：统计、正念呼吸、图表、记录列表、导出/清空
│   └── <dialog> × 4      登录 / 注册 / 删除确认 / 清空确认
└── 一个 <script>（IIFE）
    ├── 常量与存储键
    ├── 主题：initTheme / applyTheme
    ├── 面板切换：switchTab + hashchange
    ├── 树洞：提交、字数统计、AI 回信
    ├── 劝导：GUIDE 话术表 + 关键词匹配
    ├── 广场：渲染与发布
    ├── 我的：统计、呼吸训练、SVG 图表、导出
    └── 启动：initTheme → loadAll → render*
```

样式、逻辑、文案都在这一个文件里，拷贝走一份就能用，这是它「可离线、可分发」的前提。

## 2. 页面切换

用的是顶部四个 `data-tab` 按钮 + `class="on"` 显隐，而不是多文件路由：

- 点击 tab → `switchTab(name)`
- `switchTab` 里对 `tabs` 和 `panels` 逐个 `classList.toggle('on', ...)`
- 进到 `square` 会 `renderBoard()`，进到 `me` 会 `renderMe()`，保证数据是最新的
- 另外挂了一个 `hashchange` 监听：`location.hash` 去掉 `#` 后如果命中 `panels`，就走 `switchTab`，所以 `index.html#square` 这样的链接也能直接落到对应面板

## 3. 数据层

全部数据放在 `localStorage`，共 5 个键：

| 键名 | 存什么 |
|---|---|
| `coze-mood-tree-v1` | 当前用户的情绪记录数组 |
| `coze-mood-users-v1` | 注册用户表（昵称、密码散列后的字符串） |
| `coze-mood-board-v1` | 广场留言 |
| `coze-mood-current` | 当前登录用户 |
| `mood-theme` | 主题偏好（light / dark / 跟随系统） |

读写都是「取出来 → `JSON.parse` → 改 → `JSON.stringify` 写回」，没有任何异步上传。清空记录只删 `coze-mood-tree-v1`，不动用户表和广场；导出走 `Blob` + `URL.createObjectURL`，生成一个 JSON 文件下载。

## 4. AI 劝导的实现

不是接模型，是一张手写的 `GUIDE` 话术表 + 正则匹配：

```js
GUIDE.pressure = {
  label: '压力',
  re: [/压|加班|kpi|业绩|活多|累|忙|负荷|撑不住/],
  first: [ 4 句先接住情绪的话 ],
  deep:  [ 4 句具体做法 ]
};
```

- 命中某类 → 先用 `first` 回应，1.2 秒后再补 `deep`
- 全都没命中 → 落到「轻话题」，不会冷场
- 打字前有 700–1200ms 的停顿，模拟真人在写

好处是完全离线、可预期；代价是它只「接话」，不会真的理解内容——这一点在 README 的已知边界里写明了。

## 5. 图表

两张图都是手绘 SVG，没有引入任何图表库：

- 近七日柱状图：按最大值等比算 `<line>` 的高度，只标关键刻度、不画网格
- 情绪分布环形图：用 `stroke-dasharray` 把圆周按比例切段拼扇区

数据不足（比如只有 1 天记录）时留空或只画一根柱，不做平滑、不做预测。

## 6. 正念呼吸

4-4-4 节奏（吸 4 秒 — 屏 4 秒 — 呼 4 秒），走完 300 秒。计时用 `setInterval`，文案通过 `speechSynthesis` 用中文朗读（`lang='zh-CN'`、`rate=0.9`）；浏览器不支持语音时只走视觉节奏，不报错。

## 7. 零外链的自检

`scripts/verify_single_file.py` 会扫一遍 `index.html`，确认没有 `http(s)://` 外链、没有 `<script src>`、没有埋点域名，并核对 5 个存储键和文件大小。CI 里也跑同一份脚本（`.github/workflows/verify.yml`）。
