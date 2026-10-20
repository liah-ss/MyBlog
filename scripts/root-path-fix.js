'use strict';

/**
 * 子路径兜底：主题里有些地方直接输出了 `/img/...`、`href="/about/"`，
 * 没有经过 url_for()。部署到 GitHub Pages 项目页（如 /MyBlog/）时，
 * 这些根路径会指向域名根目录，导致图片和链接 404。
 *
 * 这里在 HTML 渲染完成后，统一给「尚未带上 config.root 的根路径」补前缀。
 * root 为 '/' 时不做任何处理，因此本地根路径部署、自定义域名都不受影响。
 */

const ATTRS = ['src', 'href', 'data-lazy-src', 'data-src', 'poster'];

function escapeRe(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

hexo.extend.filter.register('after_render:html', function (html) {
  const root = (hexo.config.root || '/').trim();
  if (root === '/') return html;

  const prefix = root.replace(/\/+$/, ''); // '/MyBlog'
  const skip = escapeRe(prefix.replace(/^\/+/, '')); // 'MyBlog'

  // src="/img/x"、href="/about/" 等属性
  const attrRe = new RegExp(`(${ATTRS.join('|')})="/(?!/|${skip}(?:/|"))`, 'g');
  let out = html.replace(attrRe, (_, attr) => `${attr}="${prefix}/`);

  // 内联样式里的 url(/img/x)
  const cssRe = new RegExp(`url\\(\\s*/(?!/|${skip}/)`, 'g');
  out = out.replace(cssRe, `url(${prefix}/`);

  return out;
});
