*整体分三个部分*
1. proxy server 是以容器的形式存在的
2. cookie的动态获得,也会以容器的形式存在
3. 爬虫部分,该部分分两个,一个是爬取列表页,一个是爬取详情页



---

cookie代理部分是     main_cookies.py
获得pagelist的部分是 main_pagelist.py
获得detail的部分是   main_detail.py
由于三个部分都是独立的进程，所以针对这三个分别进行docker打包

各个打包镜像的名称
docker run -d -p 8123:8123  yyqq188/tor_change_ip_proxy_with_more_vim:latest

docker run -d yyqq188/qcc_asiainfo_cookie:v1
docker run -e LANG=C.UTF-8 -d  yyqq188/qcc_asiainfo_pagelist_spider:v1
docker run -e LANG=C.UTF-8 -d  yyqq188/qcc_asiainfo_detail_spider:v1
docker run -e LANG=C.UTF-8 -d  yyqq188/qcc_asiainfo_write_to_mysql:v1
