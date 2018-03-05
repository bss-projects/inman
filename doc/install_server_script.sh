#!/bin/bash

SERVER_DEST="srv.inman.lan"
INMAN_SOURCE_PATH="/root/inman/git"
INMAN_DEST_SOURCE_PATH="/tmp/inman_source"

INMAN_DEST_MAIN_PATH="/opt/inman"
INMAN_DEST_SERVER_PATH="$INMAN_DEST_MAIN_PATH/master/im_server"
INMAN_DEST_WEB_PATH="$INMAN_DEST_MAIN_PATH/master/web"
INMAN_DEST_CROSSBAR_PATH="$INMAN_DEST_MAIN_PATH/inman_crossbar/.crossbar"

OLD_VERSION="v0.9.4-RC2"

pg_dump -U dbu_inman -s inman > $INMAN_SOURCE_PATH/for_release/inman_dump_struct_$OLD_VERSION.sql
sed -i 's/CREATE FUNCTION/CREATE OR REPLACE FUNCTION/g' $INMAN_SOURCE_PATH/for_release/inman_dump_struct_$OLD_VERSION.sql
sed -i 's/[# ]fd[ .].*//g' $INMAN_SOURCE_PATH/for_release/inman_dump_struct_$OLD_VERSION.sql
sed -i 's/^fd[ .].*//g' $INMAN_SOURCE_PATH/for_release/inman_dump_struct_$OLD_VERSION.sql

ssh root@$SERVER_DEST "mkdir -p $INMAN_DEST_SOURCE_PATH"
scp -r $INMAN_SOURCE_PATH/* root@$SERVER_DEST:$INMAN_DEST_SOURCE_PATH

ssh root@$SERVER_DEST "cd $INMAN_DEST_SOURCE_PATH/im_server && nuitka --recurse-to=im_dbclass --recurse-to=im_agentdialogclass --recurse-to=im_user_trace_action_class im_masterside.py"

ssh root@$SERVER_DEST "mkdir -p $INMAN_DEST_SERVER_PATH ; mkdir -p $INMAN_DEST_WEB_PATH ; mkdir -p $INMAN_DEST_CROSSBAR_PATH"


ssh root@$SERVER_DEST "cp -r $INMAN_DEST_MAIN_PATH $INMAN_DEST_MAIN_PATH/../inman.$OLD_VERSION"
ssh root@$SERVER_DEST "pg_dump -U dbu_inman -s inman > $INMAN_DEST_MAIN_PATH/../inman.$OLD_VERSION/inman_dump_struct.sql"
ssh root@$SERVER_DEST "pg_dump -U dbu_inman inman > $INMAN_DEST_MAIN_PATH/../inman.$OLD_VERSION/inman_dump_db.sql"
ssh root@$SERVER_DEST "cd $INMAN_DEST_SOURCE_PATH/im_server && cp -r crossbar im_cron im_freeradius im_masterside.exe init.d_im_master templates translation web_session $INMAN_DEST_SERVER_PATH"
ssh root@$SERVER_DEST "cd $INMAN_DEST_SOURCE_PATH/web && cp -r * $INMAN_DEST_WEB_PATH"

ssh root@$SERVER_DEST "su -l postgres -c \"psql -d inman < $INMAN_DEST_SOURCE_PATH/for_release/inman_dump_struct_$OLD_VERSION.sql\""

ssh root@$SERVER_DEST "cp $INMAN_DEST_SOURCE_PATH/im_server/crossbar/config.json $INMAN_DEST_CROSSBAR_PATH"
