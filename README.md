# SinaMicro

### Python爬取新浪微博

#### 主要思路：
1. 模拟登陆得到cookie：因为新浪微博网页版诸多限制，故爬取新浪微博手机版，技术上使用selenium模拟浏览器
2. 代理IP：新浪对访问有限制，故采用代理IP的方式，目前主要爬取www.kuaidaili.com上的高匿IP
3. 从测试帐号开始爬取微博
