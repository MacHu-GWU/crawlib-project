#!/bin/bash
# -*- coding: utf-8 -*-

docker run --rm --name crawlib-test-mongo-db \
    -d \
    -p 43346:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=username \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    mongo:3.6 \
sleep 1
