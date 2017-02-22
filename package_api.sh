#!/bin/bash
#cp template/conf/config.default.json template/conf/config.json
zip -r template_api.zip template \
    --exclude template/deploy/instantclient-* \
    --exclude template/conf/config.*.json \
    --exclude template/deploy/.vagrant/\* \
    --exclude template/migration_session/\* \
    --exclude template/prod_logs/\* \
    --exclude *.swp
