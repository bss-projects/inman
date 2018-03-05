#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import psycopg2
import sys

conn = psycopg2.connect(database='inman', user='dbu_inman', password='pass')
cur = conn.cursor()

#cur.execute("SELECT id, json_build_object('Name', vendor_info->'name', 'price', vendor_info->'price', 'tableau', vendor_info->'tableau', 'hash', vendor_info->'hash') FROM vendor")
#cur.execute("SELECT * FROM vendor")

#ver = cur.fetchall()
#print ver

#d_vendor_info = {}
#d_vendor_info['radiusname'] = 'RTHD'
#d_vendor_info['vendorname'] = 'Cisco'

#d_vendor_info['l_flag_level'] = [{'label' : 'list_flag', 'l_block' : [{'block_name' : 'default', 'list' : [{'Service-type' : ''}, {'AVPair' : ''}]}, {'block_name' : 'default2', 'list' : [{'Wana' : ''}, {'HSRP' : ''}]}]}, {'label' : 'read-only',  'l_flag' :[ {'Service-type' : '6'}, {'AVPair' : 'shell-level'}]}]

#to_insert = json.dumps(d_vendor_info).replace('\'', '\'\'')

#cur.execute("INSERT INTO vendor (vendor_info) VALUES ('"+ to_insert +"')")

#d_user_info = {}
#d_user_info['username'] = 'X2013360'
#d_user_info['isldap'] = True
#d_user_info['password'] = None
#d_user_info['right_level'] = 'read-only'

#to_insert = json.dumps(d_user_info).replace('\'', '\'\'')

#cur.execute("INSERT INTO users (user_info) VALUES ('"+ to_insert +"')")

d_agent_info = ['Radius RTHD', 'Radius BIV']

to_insert = json.dumps(d_agent_info).replace('\'', '\'\'')

cur.execute("INSERT INTO matview (name, view_data) VALUES ('list_agent_freeradius', '"+ to_insert +"')")

#tutu = 'cat\'s eyes'
#tutu = tutu.replace('\'', '\'\'')
#print tutu

#toto = "Super hyper\'\'marché&@àè"
#print type(toto)
#toto = toto.decode('utf-8')
#print type(toto)
#titi = 4242.4242

#print toto.encode('utf-8')

#print ver[3][1]['Name'].encode('utf-8')
#print ver[24][0]['price']
#print ver[20][0]['tableau'][2]
#print ver[20][0]['hash']['type']

#cur.execute("INSERT INTO vendor (vendor_info) VALUES ('{\"name\": \""+ toto +"\" , \"type\": \"phone\", \"brand\": \"ACME\", \"price\": "+ str(titi) +", \"available\": true, \"warranty_years\": 1, \"tableau\" : [1, \"deux\", \"je pense d''onc je suis\", 42], \"hash\" : {\"type\": \"firstname\", \"value\": \"John\"} } ')", (toto) )

#d_test_json = {}
#d_test_json[1] = 'tutu'
#d_test_json['Name'] = 'éàê super\'\'s insc'

#to_insert = ''
#to_insert = json.dumps(d_test_json)

#print to_insert

#cur.execute("INSERT INTO vendor (vendor_info) VALUES ('"+ to_insert +"')")

#cur.execute("SELECT * FROM vendor WHERE id = 1")
#ver = cur.fetchall()
#print ver[0][1]['brand']

#ver[0][1]['brand'] = 'Rien de rien'

#to_update = ''
#to_update = json.dumps(ver[0][1])
#to_update = to_update.replace('\'', '\'\'')

#print to_update

#cur.execute("UPDATE vendor SET (vendor_info) = ('"+ to_update +"') WHERE  vendor_info->>'brand' = 'CHOULI\"CHI\"PETTE'")

#cur.execute("DELETE FROM vendor WHERE  vendor_info->>'1' = 'tutu'")

conn.commit()
cur.close()
conn.close()