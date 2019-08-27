#对获得cookie的进程打包(有selenium动态代理)

FROM ubuntu
MAINTAINER yyqq188@foxmail.com
RUN apt-get update && apt-get install -y python3-pip && apt-get install -y libmysqlclient-dev \
&& apt-get install -y python3-dev \
&& pip3 install requests && pip3 install mysqlclient && pip3 install redis==3.2.0 \
&& pip3 install docker && pip3 install selenium


#修改默认python
RUN rm -rf /usr/bin/python &&  ln -s /usr/bin/python3  /usr/bin/python


COPY ./chromium-browser_75.0.3770.90-0ubuntu0.18.04.1_amd64.deb /chromium-browser_75.0.3770.90-0ubuntu0.18.04.1_amd64.deb
COPY ./chromium-chromedriver_74.0.3729.169-0ubuntu0.16.04.1_amd64.deb /chromium-chromedriver_74.0.3729.169-0ubuntu0.16.04.1_amd64.deb
RUN dpkg -i chromium-browser_75.0.3770.90-0ubuntu0.18.04.1_amd64.deb;apt-get -fy install
RUN dpkg -i chromium-chromedriver_74.0.3729.169-0ubuntu0.16.04.1_amd64.deb;apt-get -fy install
#用于在内部写exec_gen_cookie.sh
RUN apt install vim -y

#拷贝主要文件
COPY ./main_cookies.py  /qichacha_zhejiang/main_cookies.py
COPY ./settings.py /qichacha_zhejiang/settings.py
CMD python /qichacha_zhejiang/main_cookies.py

#docker run -d yyqq188/qcc_asiainfo_cookie:v1
#修改execute_cookie_cycle.sh 并启动


#---------------------------------------------------------------------------------------------------

#对pagelist爬虫进行打包

#FROM ubuntu
#MAINTAINER yyqq188@foxmail.com
#RUN apt-get update && apt-get install -y python3-pip && apt-get install -y libmysqlclient-dev \
#&& apt-get install -y python3-dev \
#&& pip3 install requests && pip3 install redis==3.2.0
#RUN apt install vim -y
#
##修改默认python
#RUN rm -rf /usr/bin/python &&  ln -s /usr/bin/python3  /usr/bin/python
#
#RUN pip3 install scrapy
##拷贝主要文件
#COPY ./main_pagelist.py  /qichacha_zhejiang/main_pagelist.py
#COPY ./settings.py /qichacha_zhejiang/settings.py
#CMD python /qichacha_zhejiang/main_pagelist.py

#
#docker run -e LANG=C.UTF-8 -d  yyqq188/qcc_asiainfo_pagelist_spider:v1
#注意启动时加LANG
#后期需要修改settings文件中的proxy服务器
#------------------------------------------------------------------------------------------------------
#对detail爬虫进行打包

#FROM ubuntu
#MAINTAINER yyqq188@foxmail.com
#RUN apt-get update && apt-get install -y python3-pip && apt-get install -y libmysqlclient-dev \
#&& apt-get install -y python3-dev \
#&& pip3 install requests && pip3 install mysqlclient && pip3 install redis==3.2.0 \
#&& apt install vim -y
#RUN pip3 install scrapy
#
#
##修改默认python
#RUN rm -rf /usr/bin/python &&  ln -s /usr/bin/python3  /usr/bin/python
#
#
##拷贝主要文件
#COPY ./main_detail.py /qichacha_zhejiang/main_detail.py
#COPY ./settings.py /qichacha_zhejiang/settings.py
#CMD python /qichacha_zhejiang/main_detail.py

#docker run -e LANG=C.UTF-8 -d  yyqq188/qcc_asiainfo_detail_spider:v1
#注意启动时加LANG
#后期需要修改settings文件中的proxy服务器


#-----------------------------------------------------------------------------
#将多个爬虫的redis数据统一写入mysql

#FROM ubuntu
#MAINTAINER yyqq188@foxmail.com
#RUN apt-get update && apt-get install -y python3-pip && apt-get install -y libmysqlclient-dev \
#&& apt-get install -y python3-dev \
#&& pip3 install requests && pip3 install mysqlclient && pip3 install redis==3.2.0 \
#&& apt install vim -y
#RUN pip3 install scrapy
#
#
##修改默认python
#RUN rm -rf /usr/bin/python &&  ln -s /usr/bin/python3  /usr/bin/python
#
#
##拷贝主要文件
#COPY ./main_write_to_mysql.py /qichacha_zhejiang/main_write_to_mysql.py
#COPY ./settings.py /qichacha_zhejiang/settings.py
#CMD python /qichacha_zhejiang/main_write_to_mysql.py


#docker run -e LANG=C.UTF-8 -d  yyqq188/qcc_asiainfo_write_to_mysql:v1
#注意启动时加LANG
#后期需要修改settings文件中的proxy服务器

