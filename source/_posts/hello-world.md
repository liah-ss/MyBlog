---
title: 你好，世界
date: 2026-10-20 19:20:00
updated: 2026-10-20 19:20:00
tags:
  - 随笔
categories:
  - 生活
keywords: 开始
description: 第一篇占位文章，顺便记录这套博客是怎么搭起来的。
top_img: /img/default_cover.jpg
cover: /img/default_cover.jpg
---

这是博客的第一篇文章，你可以直接改写它，也可以删掉后重新写。

## 写一篇新文章

```bash
npx hexo new "文章标题"
```

命令会在 `source/_posts/` 下生成一个 Markdown 文件，以及一个同名资源文件夹，图片放进文件夹后即可在文章里直接引用。

## 本地预览

```bash
npx hexo clean && npx hexo server
```

浏览器打开 <http://localhost:4000> 查看效果。

## 生成静态文件

```bash
npx hexo generate
```

产物在 `public/` 目录，可以直接部署到任意静态托管平台。
