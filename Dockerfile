FROM eavatar/basebox
MAINTAINER sampot <sam@eavatar.com>

ADD dist/ava /ava
ADD ava-run.sh /etc/service/ava/run
RUN chown -R ava:ava /ava && chmod a+x /etc/service/ava/run

EXPOSE 5000 5443
VOLUME /ava/home
