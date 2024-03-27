FROM python:3.12.1-alpine3.19
WORKDIR /app
ADD requirements.txt /app
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN rm -f /etc/localtime
RUN  ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
ADD . /app
CMD uvicorn main:app --host 0.0.0.0 --port 8000
EXPOSE 8000