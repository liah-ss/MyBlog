---
title: 这个博客是怎么搭起来的
date: 2026-10-21 01:20:00
updated: 2026-10-21 01:20:00
tags:
  - Hexo
  - 建站
categories:
  - 技术
keywords: Hexo,安知鱼,GitHub Pages,Pages CMS
description: 从零到能访问：技术栈、内容怎么改、发布流程，以及踩过的坑。
top_img: /img/placeholder.png
cover: /img/placeholder.png
---

把建站过程记下来，一是方便以后重装，二是给同样想搭博客的人一个参照。

## 技术栈

| 层 | 选型 | 说明 |
| --- | --- | --- |
| 生成器 | Hexo 8 | 把 Markdown 生成静态 HTML |
| 主题 | 安知鱼 1.7.1 | 卡片式布局，自带相册、设备、友链、搜索 |
| 内容管理 | Pages CMS | 网页后台，改完自动提交到仓库 |
| 托管 | GitHub Pages | 免费，推送后自动构建发布 |

整套没有数据库、没有服务器，只有一堆静态文件。

## 日常怎么改内容

后台在 `app.pagescms.org`，用 GitHub 登录后能改：文章、相册、设备、友链、即刻短文、关于页。

保存的瞬间会生成一次 Git 提交，GitHub Actions 接到提交后重新构建，大约一两分钟站点更新。也就是说：

- 后台只负责「改文件」
- Actions 负责「把文件变成网站」

## 发布流程

```
Pages CMS 保存
   ↓ 提交到 GitHub
GitHub Actions 构建（npm ci → hexo generate）
   ↓ 产物上传
GitHub Pages 发布
```

构建配置在 `.github/workflows/deploy.yml`，只要推送到 `main` 分支就会触发。

## 踩过的坑

**1. 项目页有子路径**

仓库叫 `MyBlog`，站点地址就是 `https://用户名.github.io/MyBlog/`。主题里有不少地方直接写死了 `/img/...`，没走 Hexo 的 `url_for`，结果图片全 404。

解决办法是加了一个构建期脚本 `scripts/root-path-fix.js`：在 HTML 输出后统一给未带前缀的根路径补上 `root`。根路径部署（自定义域名）时这个脚本会自动跳过。

**2. 后台传图的文件名**

带空格或中文的路径（`/img/my product/xxx.png`、`微信图片_xxx.jpg`）在 URL 里会出问题。现在后台统一随机命名，图片按 `equipment/`、`album/`、`skills/` 分目录存放。

**3. 相册没封面**

相册列表用的是单独设置的封面，没设就会白底白字。已经改成回退到相册第一张照片。

## 后面还想加什么

评论后端、图床、访问统计，以及把文章写得再长一点。
