#!/usr/bin/env bash
docker run -d \
    -p 80:80 -p 443:443 -p 22:22 \
    --network=host \
    -e PHABRICATOR_HOST=192.168.34.84 \
    -e MYSQL_HOST=192.168.12.199 \
    -e MYSQL_USER=root \
    -e MYSQL_PASS=root \
    -e PHABRICATOR_REPOSITORY_PATH=/repos \
    -v /data:/repos \
    --name phabricator \
    registry.cn-shenzhen.aliyuncs.com/aios/phabricator
