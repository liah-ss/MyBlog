# LIAH 的博客

基于 **Hexo 8.1.2 + 安知鱼主题（hexo-theme-anzhiyu 1.7.1）** 的个人博客，静态生成，可直接部署到任意静态托管平台。

## 常用命令

```bash
npx hexo new "文章标题"    # 新建文章（同时生成同名资源目录）
npx hexo new page "页面名" # 新建页面
npx hexo clean             # 清理缓存与 public
npx hexo server            # 本地预览 http://localhost:4000
npx hexo generate          # 生成静态文件到 public/
```

建议把 `npx hexo` 换成全局安装后的 `hexo`：`npm i -g hexo-cli`。

## 目录约定

```
├─ source/                # 内容
│  ├─ _posts/             # 文章（每篇可带同名资源目录放图片）
│  ├─ _data/              # 页面数据（about.yml 等）
│  ├─ about/ tags/ categories/ archives/  # 页面
│  └─ img/                # 站点静态图片（头像等）
├─ themes/anzhiyu/        # 主题源码：改模板/样式在这里
├─ scripts/               # 自研 Hexo 脚本，构建时自动加载（按需新建）
├─ scaffolds/             # 新建文章/页面的模板
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

## 二次开发入口

| 想改什么 | 改哪里 |
| --- | --- |
| 站点信息、导航、配色、开关 | `_config.anzhiyu.yml` |
| 首页/文章页/关于页结构 | `themes/anzhiyu/layout/*.pug` |
| 样式 | `themes/anzhiyu/source/css/`（覆盖变量优先，少直接改源码） |
| 由数据驱动的页面（关于、友链、相册） | `source/_data/*.yml` |
| 构建期逻辑（生成新页面、处理文章字段） | `scripts/*.js` |

主题是 GPL-3.0，可以自由修改，但保留 `themes/anzhiyu/LICENSE`。

## 主题升级

主题源码已内置在仓库里（不是 npm 依赖），升级时用官方仓库比对差异，不要整目录覆盖，否则会丢掉本地改动：

```bash
# 在临时目录拉取新版，按文件比对后手动合并
git clone --depth 1 https://github.com/anzhiyu-c/hexo-theme-anzhiyu.git /tmp/anzhiyu-new
```

同时比对 `themes/anzhiyu/_config.yml`，把新增项补充到根目录 `_config.anzhiyu.yml`。

## 部署

`npx hexo generate` 后把 `public/` 部署到静态托管（GitHub Pages / Vercel / Cloudflare Pages 等）。部署前记得把 `_config.yml` 里的 `url` 改成真实域名。
