FROM 10.12.36.155:8020/cds/daohang/python39a:latest

ADD common /data/ui/common
ADD config /data/ui/config
ADD daohang /data/ui/daohang
ADD conftest.py /data/ui/
ADD run_ui_test.py /data/ui/

WORKDIR /data/ui

# 设置为上海时区
RUN echo "Asia/Shanghai" > /etc/timezone

CMD python3 run_ui_test.py