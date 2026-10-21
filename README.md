# LIAH 的博客

基于 **Hexo 8.1.2 + 安知鱼主题（hexo-theme-anzhiyu 1.7.1）** 的个人博客，静态生成，可直接部署到任意静态托管平台。

## 常用命令

```bash
npm run dev     # 本地预览 http://localhost:4000/MyBlog/
npm run build   # 生成静态文件到 public/
npm run check   # 清缓存后完整构建一遍，推代码前跑一次
```

也可以直接用 hexo（`npx hexo` 或全局安装后的 `hexo`）：

```bash
npx hexo new "文章标题"    # 新建文章（同时生成同名资源目录）
npx hexo new page "页面名" # 新建页面
npx hexo clean             # 清理缓存与 public
```

## 已包含的功能

| 功能 | 位置 | 说明 |
| --- | --- | --- |
| 站内搜索 | 导航栏放大镜 | `hexo-generator-searchdb` 生成 `search.xml` |
| RSS | `/atom.xml` | `hexo-generator-feed` |
| 站点地图 | `/sitemap.xml` | 便于搜索引擎收录 |
| 文章 | `/archives/` | Markdown + 封面 + 标签分类 |
| 相册 | `/album/` | 两套布局，照片走 `_data/album.yml` |
| 我的设备 | `/equipment/` | 分组卡片，图片走后台 |
| 友链 | `/link/` | `_data/link.yml`，支持三种卡片样式 |
| 即刻短文 | `/essay/` | 短内容流，`_data/essay.yml` |
| 留言板 | `/comments/` | 评论区留空，接后端后自动出现 |
| 自定义样式 | `source/css/custom.css` | 通过 `inject.head` 引入 |

## 目录约定

```
├─ source/                # 内容
│  ├─ _posts/             # 文章（每篇可带同名资源目录放图片）
│  ├─ _data/              # 页面数据（about.yml / album.yml）
│  ├─ about/ tags/ categories/ comments/ album/ equipment/  # 页面
│  ├─ link/ essay/        # 友链、即刻短文
│  ├─ dailyPhoto/ scenery/ # 相册详情页（与 album.yml 的 path_name 对应）
│  └─ img/                # 站点静态图片（头像、占位图、相册 album/）
├─ themes/anzhiyu/        # 主题源码：改模板/样式在这里
├─ scripts/               # 自研 Hexo 脚本，构建时自动加载（按需新建）
├─ tools/                 # 本地小工具（图片压缩等），不参与构建
├─ scaffolds/             # 新建文章/页面的模板
├─ .pages.yml             # 后台表单配置（Pages CMS）
├─ .github/workflows/     # 推送后自动构建并发布到 GitHub Pages
├─ _config.yml            # 站点配置
└─ _config.anzhiyu.yml    # 主题配置（优先级高于主题自带 _config.yml）
```

**约定**：任何自己写的代码放进 `scripts/` 或 `themes/anzhiyu/`，不要散落在根目录；临时脚本、草稿、导出文件用完即删。

## 配置约定

- `_config.yml` 管站点（标题、作者、URL、永久链接），`_config.anzhiyu.yml` 管主题外观与功能，改样式只动后者。
- 主题配置与主题内置的 `_config.yml` 是**逐项深度合并**的：对象按键合并，数组按索引合并、长度取两者的较大值。所以覆盖 `home_top.category`、`menu` 这类数组时，项数要和主题默认值对齐，否则会残留默认项。
- `themes/anzhiyu/` 里的 `.git` 已移除，主题代码作为普通文件随仓库提交（方便直接魔改）。
- 占位图 `source/img/avatar.png`、`source/img/placeholder.png` 是脚本生成的，替换同名文件即可全站生效。
- 首屏加载动画开关在 `_config.anzhiyu.yml` 的 `preloader.enable`，当前关闭；想还原参考站效果打开即可。

## 图片处理

后台传的图直接进仓库，体积大会拖慢克隆和构建。批量压缩：

```bash
python tools/compress-images.py source/img --max-edge 1600 --quality 82
```

- 长边超过 1600 的等比缩小，JPEG 重新编码，压缩后反而变大则保留原图；
- 照片不要存 PNG（一张 2.5MB 的照片压成 JPG 只要 70KB 左右）；
- 文章封面在 `source/img/covers/`，没设封面的文章会用主题 `cover.default_cover` 里的图随机挑一张。

## 评论系统

当前 `comments.use` 为空，页面只渲染留言板正文、不渲染评论区。接入只需两步：

1. 部署后端（任选其一）：
   - **Twikoo**：Vercel 新建项目 → 导入 [twikoojs/twikoo](https://github.com/twikoojs/twikoo) → 绑定 MongoDB（Atlas 免费版即可）→ 得到 `https://xxx.vercel.app`。
   - **giscus**：仓库开启 Discussions → 安装 [giscus app](https://github.com/apps/giscus) → 在 [giscus.app](https://giscus.app) 填写仓库，拿到 `repo` / `repo_id` / `category_id`。
2. 回到 `_config.anzhiyu.yml`：
   - Twikoo：`comments.use: ["Twikoo"]`，`twikoo.envId: https://xxx.vercel.app`
   - giscus：`comments.use: ["Giscus"]`，填 `giscus.repo` / `repo_id` / `category_id`

留言板页面在 `source/comments/index.md`，任何页面加 `comments: true` 就会显示评论区。

## 相册

相册由 `source/_data/album.yml` 驱动，一个相册一条数据：

- `type: 2`：justified 画廊（按行高铺满，适合多图），对应 `/dailyPhoto/`。
- `type: 1`：卡片瀑布流（每张图带描述、地点、日期），对应 `/scenery/`。
- 关键字段：`class_name`（相册名）、`path_name`（详情页路径）、`cover`（列表封面）、`album_list[].image`（图片路径数组）。

新增相册时：在 `album.yml` 加一条 → 用 `path_name` 新建同名页面，front-matter 写 `type: album_detail`。图片放 `source/img/album/`（当前 12 张是占位图，直接替换同名文件即可）。

## 二次开发入口

| 想改什么 | 改哪里 |
| --- | --- |
| 站点信息、导航、配色、开关 | `_config.anzhiyu.yml` |
| 首页/文章页/关于页结构 | `themes/anzhiyu/layout/*.pug` |
| 样式 | `themes/anzhiyu/source/css/`（覆盖变量优先，少直接改源码） |
| 由数据驱动的页面（关于、友链、相册、设备） | `source/_data/*.yml` |
| 评论后端与开关 | `_config.anzhiyu.yml` 的 `comments` / `twikoo` / `giscus` |
| 构建期逻辑（生成新页面、处理文章字段） | `scripts/*.js` |

主题是 GPL-3.0，可以自由修改，但保留 `themes/anzhiyu/LICENSE`。

## 主题升级

主题源码已内置在仓库里（不是 npm 依赖），升级时用官方仓库比对差异，不要整目录覆盖，否则会丢掉本地改动：

```bash
# 在临时目录拉取新版，按文件比对后手动合并
git clone --depth 1 https://github.com/anzhiyu-c/hexo-theme-anzhiyu.git /tmp/anzhiyu-new
```

同时比对 `themes/anzhiyu/_config.yml`，把新增项补充到根目录 `_config.anzhiyu.yml`。

## 后台（Pages CMS）

站点是静态的，没有服务器，所以后台用 Git 型 CMS：在网页上改内容 → 自动 commit 到仓库 → GitHub Actions 重新构建 → 网站更新，大约 1–2 分钟。配置在 [.pages.yml](.pages.yml)，目前可编辑：**文章、我的设备、相册、关于页、首页技能、友链、即刻短文**（支持加删条目、改文案、上传图片）。

### 一次性接入（约 10 分钟）

1. 把仓库推到 GitHub（公开或私有都可以）。
2. 打开 <https://app.pagescms.org>，用 GitHub 登录。
3. 安装 GitHub App，只授权这一个仓库。
4. 回到 Pages CMS 选择该仓库，会自动读取 `.pages.yml`。
5. 仓库 Settings → Pages → Source 选 **GitHub Actions**。
6. 推一次代码，Actions 自动构建并发布。

### 权限模型

只有对该仓库有写权限的 GitHub 账号能登录编辑；别人在 Pages CMS 里根本看不到这个仓库，访问网站只能看。不需要自己实现登录系统。

### 注意

- 后台传的图片会存到 `source/img/` 并作为 commit 进入仓库，照片多时建议先压缩，或以后换图床。
- 如果仓库名不是 `<用户名>.github.io`（项目页），要把 `_config.yml` 的 `url` 改成 `https://<用户名>.github.io/<仓库名>`，并加一行 `root: /<仓库名>/`。
- 文章（`source/_posts`）暂未配置表单，需要时按同样方式加一个 `type: collection` 即可。

## 部署

`npx hexo generate` 后把 `public/` 部署到静态托管（GitHub Pages / Vercel / Cloudflare Pages 等）。部署前记得把 `_config.yml` 里的 `url` 改成真实域名。
