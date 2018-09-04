FROM python:3.5
MAINTAINER WGS <wanggs_wkyx@163.com>
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
COPY ./scrapyd.conf /etc/scrapyd
EXPOSE 6800
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
CMD scrapyd
