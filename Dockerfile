FROM ubuntu:16.04
MAINTAINER Internal Apps Team
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    nginx \
    libaio1 \
    unzip
RUN pip install --upgrade pip

# cx_Oracle install prep (installing instantclient)
RUN mkdir -p /opt/oracle
COPY template/deploy/*.zip /opt/oracle/
WORKDIR /opt/oracle
RUN unzip '*.zip'
WORKDIR /opt/oracle/instantclient_11_2
RUN ln -s libclntsh.so.11.1 libclntsh.so
ENV ORACLE_HOME=/opt/oracle/instantclient_11_2 \
    LD_LIBRARY_PATH=/opt/oracle/instantclient_11_2

# install the app
RUN mkdir -p /opt/sps
WORKDIR /opt/sps
COPY template_api.zip .
RUN unzip template_api.zip
WORKDIR /opt/sps/template
RUN pip install -r requirements.pip

# config the app
COPY template/conf/config.json conf/config.json

# nginx config
RUN rm /etc/nginx/sites-enabled/default && \
    cp deploy/template.nginx.conf /etc/nginx/sites-available && \
    ln -s /etc/nginx/sites-available/template.nginx.conf /etc/nginx/sites-enabled/template.nginx.conf

# user/permissions setup
RUN groupadd template && useradd -g template template && \
    chown -R template:template /opt/sps/template

EXPOSE 80
CMD service nginx start && \
    supervisord -c template.supervisor.conf && \
    sleep 1 && tail -f template.log
