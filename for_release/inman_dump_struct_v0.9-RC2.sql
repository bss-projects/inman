--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: plpythonu; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpythonu;


ALTER PROCEDURAL LANGUAGE plpythonu OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: delete_agent_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION delete_agent_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_agent = []

agent_info = json.loads(TD['old']['agent_info'])

if agent_info['plugin'] == 'freeradius':
 agent_name = agent_info['agent_name']

 res = plpy.execute("SELECT * FROM matview WHERE name = 'list_agent_freeradius'")

 if res:
  for row in res:
   l_agent = json.loads(row['view_data'])
   uid = row['id']
  if agent_name in l_agent:
   l_agent.remove(agent_name)
   l_agent = json.dumps(l_agent)
   res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_agent +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.delete_agent_freeradius() OWNER TO postgres;

--
-- Name: delete_client_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION delete_client_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_client = []
ip = json.loads(TD['old']['client_info'])['ip']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_client_freeradius'")
if res:
 for row in res:
  l_client = json.loads(row['view_data'])
  uid = row['id']
 if ip in l_client:
  l_client.remove(ip)
  l_client = json.dumps(l_client)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_client +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.delete_client_freeradius() OWNER TO postgres;

--
-- Name: delete_flag_vendor_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION delete_flag_vendor_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

d_flag_vendor = {}
l_flag_vendor_tmp = []
flag_update = False
l_flag = []
l_flag_vendor = []
uid = 0

l_block = json.loads(TD['old']['vendor_info'])['l_flag_level'][0]['l_block']
vendorname = json.loads(TD['old']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

for block in l_block:
 l_flag += block['list']

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_flag_vendor_freeradius'")

if res:
 for row in res:
  l_flag_vendor = json.loads(row['view_data'])
  uid = row['id']
 
# fd.write("Previous REC" + "\n")
 for d_flag_vendor in l_flag_vendor:
  if d_flag_vendor['vendorname'] != vendorname:
   l_flag_vendor_tmp.append(d_flag_vendor.copy())
#   fd.write("Known vendor" + "\n")

 l_flag_vendor = json.dumps(l_flag_vendor_tmp)
# fd.write(l_flag_vendor + "\n")
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_flag_vendor +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.delete_flag_vendor_freeradius() OWNER TO postgres;

--
-- Name: delete_network_perimeter_for_user_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION delete_network_perimeter_for_user_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_perim = []
l_net_perim_for_user = []

#fd = open('/tmp/test_trigger', 'a')

d_user_info = json.loads(TD['old']['user_info'])
d_user_id = TD['old']['id']

if 'network_perimeter' in d_user_info :

 res = plpy.execute("SELECT id, view_data FROM matview WHERE name = 'list_network_perimeter_for_user_freeradius'")

 if res :
  for row in res:
   uid = row['id']
   l_net_perim_for_user = json.loads(row['view_data'])

  for network_perimeter in d_user_info['network_perimeter']:
   l_perim.append(network_perimeter['uid'])

  i = 0
  for net_perim_for_user in l_net_perim_for_user :
   if net_perim_for_user['id'] in l_perim:
    j = 0
    for user in net_perim_for_user['list_user']:
     if user['id'] == d_user_id :
#      fd.write('User to del detected : {0}'.format(d_user_id))
      del net_perim_for_user['list_user'][j]
     j += 1
    l_net_perim_for_user[i]['list_user'] = net_perim_for_user['list_user']
   i += 1

  l_net_perim_for_user = json.dumps(l_net_perim_for_user)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_net_perim_for_user +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.delete_network_perimeter_for_user_freeradius() OWNER TO postgres;

--
-- Name: delete_right_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION delete_right_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_right = []
l_label = []

fd = open('/tmp/test_trigger', 'a')
fd.write("\n\n")
fd.write("delete_right_freeradius\n")

l_flag_level = json.loads(TD['old']['vendor_info'])['l_flag_level']
vendorname = json.loads(TD['old']['vendor_info'])['vendorname']
uid = TD['old']['id']

OLDl_flag_level = json.loads(TD['old']['vendor_info'])['l_flag_level']
OLDvendorname = json.loads(TD['old']['vendor_info'])['vendorname']

res = plpy.execute("SELECT json_build_object('radiusname', vendor_info->'radiusname', 'vendorname', vendor_info->'vendorname', 'label', vendor_info->'l_flag_level') FROM vendor_freeradius")

if res:
 for row in res:
  fd.write(json.dumps(row) + "\n")
  l_flag = json.loads(row['json_build_object'])['label']
  for d_flag in l_flag :
   if d_flag['label'] != 'list_flag' and d_flag['label'] not in l_label:
    l_label.append(d_flag['label'])

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_right_freeradius'")

if res:
 for row in res:
  uid = row['id']

 l_right = json.dumps(l_label)
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_right +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.delete_right_freeradius() OWNER TO postgres;

--
-- Name: delete_vendor_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION delete_vendor_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_vendor = []
vendorname = json.loads(TD['old']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_vendor_freeradius'")
if res:
 for row in res:
  l_vendor = json.loads(row['view_data'])
  uid = row['id']
 if vendorname in l_vendor:
  l_vendor.remove(vendorname)
  l_vendor = json.dumps(l_vendor)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_vendor +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.delete_vendor_freeradius() OWNER TO postgres;

--
-- Name: list_agent_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_agent_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_agent = []

agent_info = json.loads(TD['new']['agent_info'])

if agent_info['plugin'] == 'freeradius':
 agent_name = agent_info['agent_name']

 res = plpy.execute("SELECT * FROM matview WHERE name = 'list_agent_freeradius'")

 if res:
  for row in res:
   l_agent = json.loads(row['view_data'])
   uid = row['id']
  if agent_name not in l_agent:
   l_agent.append(agent_name)
   l_agent = json.dumps(l_agent)
   res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_agent +"') WHERE id = "+ str(uid) +"")
 else:
  l_agent.append(agent_name)
  l_agent = json.dumps(l_agent)
  res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_agent_freeradius', '"+l_agent+"')")

$$;


ALTER FUNCTION public.list_agent_freeradius() OWNER TO postgres;

--
-- Name: list_client_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_client_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_client = []
ip = json.loads(TD['new']['client_info'])['ip']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_client_freeradius'")
if res:
 for row in res:
  l_client = json.loads(row['view_data'])
  uid = row['id']
 if ip not in l_client:
  l_client.append(ip)
  l_client = json.dumps(l_client)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_client +"') WHERE id = "+ str(uid) +"")
else:
 l_client.append(ip)
 l_client = json.dumps(l_client)
 res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_client_freeradius', '"+l_client+"')")

$$;


ALTER FUNCTION public.list_client_freeradius() OWNER TO postgres;

--
-- Name: list_flag_vendor(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_flag_vendor() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

d_flag_vendor = {}
d_flag_vendor_tmp = {}
flag_update = False
l_flag = []
l_flag_vendor = []
uid = 0

l_block = json.loads(TD['new']['vendor_info'])['l_flag_level'][0]['l_block']
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

for block in l_block:
 l_flag += block['list']

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_flag_vendor'")

if res:
 for row in res:
  l_flag_vendor = json.loads(row['view_data'])
  uid = row['id']
 
# fd.write("Previous REC" + "\n")
 i = 0
 for d_flag_vendor in l_flag_vendor:
  if d_flag_vendor['vendorname'] == vendorname:
   d_flag_vendor['l_flag'] = l_flag
   l_flag_vendor[i] = d_flag_vendor
   flag_update = True
#   fd.write("Known vendor" + "\n")
   break
  i += 1

 if not flag_update :
#  fd.write("Unknown vendor" + "\n")
#  fd.write(json.dumps(l_flag_vendor) + "\n")
  d_flag_vendor_tmp['vendorname'] = vendorname
  d_flag_vendor_tmp['l_flag'] = l_flag
#  fd.write(json.dumps(d_flag_vendor_tmp) + "\n")
  l_flag_vendor.append(d_flag_vendor_tmp)

 l_flag_vendor = json.dumps(l_flag_vendor)
# fd.write(l_flag_vendor + "\n")
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_flag_vendor +"') WHERE id = "+ str(uid) +"")

else:
 d_flag_vendor['vendorname'] = vendorname
 d_flag_vendor['l_flag'] = l_flag
 l_flag_vendor.append(d_flag_vendor)

 l_flag_vendor = json.dumps(l_flag_vendor)
 res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_flag_vendor', '"+ l_flag_vendor +"')")

$$;


ALTER FUNCTION public.list_flag_vendor() OWNER TO postgres;

--
-- Name: list_flag_vendor_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_flag_vendor_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

d_flag_vendor = {}
d_flag_vendor_tmp = {}
flag_update = False
l_flag = []
l_flag_vendor = []
uid = 0

l_block = json.loads(TD['new']['vendor_info'])['l_flag_level'][0]['l_block']
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

for block in l_block:
 l_flag += block['list']

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_flag_vendor_freeradius'")

if res:
 for row in res:
  l_flag_vendor = json.loads(row['view_data'])
  uid = row['id']
 
# fd.write("Previous REC" + "\n")
 i = 0
 for d_flag_vendor in l_flag_vendor:
  if d_flag_vendor['vendorname'] == vendorname:
   d_flag_vendor['l_flag'] = l_flag
   l_flag_vendor[i] = d_flag_vendor
   flag_update = True
#   fd.write("Known vendor" + "\n")
   break
  i += 1

 if not flag_update :
#  fd.write("Unknown vendor" + "\n")
#  fd.write(json.dumps(l_flag_vendor) + "\n")
  d_flag_vendor_tmp['vendorname'] = vendorname
  d_flag_vendor_tmp['l_flag'] = l_flag
#  fd.write(json.dumps(d_flag_vendor_tmp) + "\n")
  l_flag_vendor.append(d_flag_vendor_tmp)

 l_flag_vendor = json.dumps(l_flag_vendor)
# fd.write(l_flag_vendor + "\n")
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_flag_vendor +"') WHERE id = "+ str(uid) +"")

else:
 d_flag_vendor['vendorname'] = vendorname
 d_flag_vendor['l_flag'] = l_flag
 l_flag_vendor.append(d_flag_vendor)

 l_flag_vendor = json.dumps(l_flag_vendor)
 res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_flag_vendor_freeradius', '"+ l_flag_vendor +"')")

$$;


ALTER FUNCTION public.list_flag_vendor_freeradius() OWNER TO postgres;

--
-- Name: list_network_perimeter_for_user_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_network_perimeter_for_user_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

d_user_info = {}
l_net_perim_for_user = []
flag_add_user = True
l_id_perim = []
uid = 0

d_user_info = json.loads(TD['new']['user_info'])
d_user_id = TD['new']['id']

if 'network_perimeter' in d_user_info :
 res = plpy.execute("SELECT id, view_data FROM matview WHERE name = 'list_network_perimeter_for_user_freeradius'")

 if res :
  for row in res:
   uid = row['id']
   l_net_perim_for_user = json.loads(row['view_data'])

  i = 0
  for net_perim_for_user in l_net_perim_for_user :
   for network_perimeter in d_user_info['network_perimeter'] :
    if net_perim_for_user['id'] == network_perimeter['uid'] :
     l_id_perim.append(network_perimeter['uid'])
     for user in net_perim_for_user['list_user'] :
      flag_add_user = True
      if user['id'] == d_user_id :
       flag_add_user = False

     if flag_add_user:
      l_net_perim_for_user[i]['list_user'].append({'id': d_user_id, 'username': d_user_info['username']})

   i += 1

  for network_perimeter in d_user_info['network_perimeter'] :
   if network_perimeter['uid'] not in l_id_perim :
    l_net_perim_for_user.append({'id': network_perimeter['uid'], 'network_perimeter_name': network_perimeter['perimeter_name'], 'list_user': [{'id': d_user_id, 'username': d_user_info['username']}]})

  l_net_perim_for_user = json.dumps(l_net_perim_for_user)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_net_perim_for_user +"') WHERE id = "+ str(uid) +"")

 else :
  for network_perimeter in d_user_info['network_perimeter']:
   l_net_perim_for_user.append({'id': network_perimeter['uid'], 'network_perimeter_name': network_perimeter['perimeter_name'], 'list_user': [{'id': d_user_id, 'username': d_user_info['username']}]})

  l_net_perim_for_user = json.dumps(l_net_perim_for_user)
  res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_network_perimeter_for_user_freeradius', '"+ l_net_perim_for_user +"')")

$$;


ALTER FUNCTION public.list_network_perimeter_for_user_freeradius() OWNER TO postgres;

--
-- Name: list_right_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_right_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_right = []
l_label = []

fd = open('/tmp/test_trigger', 'a')
fd.write('list_right_freeradius' + "\n")

l_flag_level = json.loads(TD['new']['vendor_info'])['l_flag_level']
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']

for d_level in l_flag_level :
 if d_level['label'] != 'list_flag' :
  l_label.append(d_level['label'])

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_right_freeradius'")

if res:
 for row in res:
  l_right = json.loads(row['view_data'])
  uid = row['id']

 for label in l_label:
  if label not in l_right:
   l_right.append(label)

 l_right = json.dumps(l_right)
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_right +"') WHERE id = "+ str(uid) +"")

else :
 l_right += l_label
 l_right = json.dumps(l_right)
 res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_right_freeradius', '"+ l_right +"')")

$$;


ALTER FUNCTION public.list_right_freeradius() OWNER TO postgres;

--
-- Name: list_user(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_user() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_user = []

username = json.loads(TD['new']['user_info'])['username']

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_user'")

if res:
 for row in res:
  l_user = json.loads(row['view_data'])
  uid = row['id']
 if username not in l_user:
  l_user.append(username)
  l_user = json.dumps(l_user)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_user +"') WHERE id = "+ str(uid) +"")
else:
 l_user.append(username)
 l_user = json.dumps(l_user)
 res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_user', '"+l_user+"')")

$$;


ALTER FUNCTION public.list_user() OWNER TO postgres;

--
-- Name: list_vendor_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION list_vendor_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_vendor = []
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_vendor_freeradius'")
if res:
 for row in res:
  l_vendor = json.loads(row['view_data'])
  uid = row['id']
 if vendorname not in l_vendor:
  l_vendor.append(vendorname)
  l_vendor = json.dumps(l_vendor)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_vendor +"') WHERE id = "+ str(uid) +"")
else:
 l_vendor.append(vendorname)
 l_vendor = json.dumps(l_vendor)
 res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_vendor_freeradius', '"+l_vendor+"')")

$$;


ALTER FUNCTION public.list_vendor_freeradius() OWNER TO postgres;

--
-- Name: update_client_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_client_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_client = []
ip = json.loads(TD['new']['client_info'])['ip']
OLDip = json.loads(TD['old']['client_info'])['ip']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_client_freeradius'")
if res:
 for row in res:
  l_client = json.loads(row['view_data'])
  uid = row['id']
 if OLDip in l_client:
  l_client.remove(OLDip)
  l_client.append(ip)
  l_client = json.dumps(l_client)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_client +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.update_client_freeradius() OWNER TO postgres;

--
-- Name: update_flag_vendor_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_flag_vendor_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

d_flag_vendor = {}
d_flag_vendor_tmp = {}
flag_update = False
l_flag = []
l_flag_vendor = []
l_flag_vendor_tmp = []
uid = 0

l_block = json.loads(TD['new']['vendor_info'])['l_flag_level'][0]['l_block']
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']
OLDl_block = json.loads(TD['old']['vendor_info'])['l_flag_level'][0]['l_block']
OLDvendorname = json.loads(TD['old']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

for block in l_block:
 l_flag += block['list']

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_flag_vendor_freeradius'")

if res:
 for row in res:
  l_flag_vendor = json.loads(row['view_data'])
  uid = row['id']
 
# fd.write("Previous REC" + "\n")
 i = 0
 for d_flag_vendor in l_flag_vendor:
  if d_flag_vendor['vendorname'] == vendorname:
   d_flag_vendor['l_flag'] = l_flag
   l_flag_vendor[i] = d_flag_vendor
   flag_update = True
#   fd.write("Known vendor" + "\n")
   break
  i += 1

 if not flag_update :
#  fd.write("Unknown vendor" + "\n")
  for d_flag_vendor in l_flag_vendor:
   if d_flag_vendor['vendorname'] != OLDvendorname:
    l_flag_vendor_tmp.append(d_flag_vendor.copy())
   elif d_flag_vendor['vendorname'] == OLDvendorname:
    d_flag_vendor_tmp['vendorname'] = vendorname
    d_flag_vendor_tmp['l_flag'] = l_flag
    l_flag_vendor_tmp.append(d_flag_vendor_tmp)

 if l_flag_vendor_tmp:
  l_flag_vendor = json.dumps(l_flag_vendor_tmp)
 else :
  l_flag_vendor = json.dumps(l_flag_vendor)
# fd.write(l_flag_vendor + "\n")
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_flag_vendor +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.update_flag_vendor_freeradius() OWNER TO postgres;

--
-- Name: update_network_perimeter_for_user_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_network_perimeter_for_user_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

fd = open('/tmp/test_trigger', 'a')

d_user_info_new = json.loads(TD['new']['user_info'])
d_user_info_old = json.loads(TD['old']['user_info'])
d_user_id = TD['new']['id']
l_net_perim_for_user = []
flag_new_perimeter = True
flag_new_perimeter_list_id = []
rest_in_list = []
d_id_perim_name = {}

fd.write('{0} {1} {2}'.format(d_user_id, d_user_info_new, d_user_info_old))


res = plpy.execute("SELECT id, view_data FROM matview WHERE name = 'list_network_perimeter_for_user_freeradius'")

if res :
 for row in res:
  uid = row['id']
  l_net_perim_for_user = json.loads(row['view_data'])

 l_perim_old = []
 l_perim_new = []

 if 'network_perimeter' in d_user_info_new :
  for network_perimeter in d_user_info_new['network_perimeter']:
   l_perim_new.append(network_perimeter['uid'])
   d_id_perim_name[network_perimeter['uid']] = network_perimeter['perimeter_name']

 if 'network_perimeter' in d_user_info_old :
  for network_perimeter in d_user_info_old['network_perimeter']:
   l_perim_old.append(network_perimeter['uid'])

 l_perim_del_after_update = list(set(l_perim_old) - set(l_perim_new))
 l_perim_add_after_update = list(set(l_perim_new) - set(l_perim_old))

 fd.write('To add -> {0} \n To delete -> {1} \n'.format(l_perim_add_after_update, l_perim_del_after_update))

 i = 0
 for net_perim_for_user in l_net_perim_for_user :
  if net_perim_for_user['id'] in l_perim_del_after_update:
   j = 0
   for user in net_perim_for_user['list_user']:
    if user['id'] == d_user_id :
     fd.write('User to del detected : {0}'.format(d_user_id))
     del net_perim_for_user['list_user'][j]
    j += 1
   if net_perim_for_user['list_user'] != [] :
    l_net_perim_for_user[i]['list_user'] = net_perim_for_user['list_user']
   else :
    del l_net_perim_for_user[i]
  i += 1

 i = 0
 for net_perim_for_user in l_net_perim_for_user :
  if net_perim_for_user['id'] in l_perim_add_after_update:
   flag_new_perimeter_list_id.append(net_perim_for_user['id'])
   l_net_perim_for_user[i]['list_user'].append({'id': d_user_id, 'username': d_user_info_new['username']})
  if l_perim_add_after_update == [] and l_perim_del_after_update == [] and net_perim_for_user['id'] in d_id_perim_name :
   l_net_perim_for_user[i]['network_perimeter_name'] = d_id_perim_name[net_perim_for_user['id']]
  i += 1

 rest_in_list = list(set(l_perim_add_after_update) - set(flag_new_perimeter_list_id))

 if rest_in_list:
  for id in rest_in_list :
   l_net_perim_for_user.append({'id': id, 'network_perimeter_name': d_id_perim_name[id], 'list_user': [{'id': d_user_id, 'username': d_user_info_new['username']}]})

 l_net_perim_for_user = json.dumps(l_net_perim_for_user)
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_net_perim_for_user +"') WHERE id = "+ str(uid) +"")

else :
 if 'network_perimeter' in d_user_info_new :
  for network_perimeter in d_user_info_new['network_perimeter']:
   l_net_perim_for_user.append({'id': network_perimeter['uid'], 'network_perimeter_name': network_perimeter['perimeter_name'], 'list_user': [{'id': d_user_id, 'username': d_user_info_new['username']}]})

  l_net_perim_for_user = json.dumps(l_net_perim_for_user)
  res = plpy.execute("INSERT INTO matview (name, view_data) VALUES ('list_network_perimeter_for_user_freeradius', '"+ l_net_perim_for_user +"')")

$$;


ALTER FUNCTION public.update_network_perimeter_for_user_freeradius() OWNER TO postgres;

--
-- Name: update_right_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_right_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_right = []
l_label = []

fd = open('/tmp/test_trigger', 'a')
fd.write("\n\n")
fd.write("update_right_freeradius\n")

l_flag_level = json.loads(TD['new']['vendor_info'])['l_flag_level']
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']
uid = TD['new']['id']

OLDl_flag_level = json.loads(TD['old']['vendor_info'])['l_flag_level']
OLDvendorname = json.loads(TD['old']['vendor_info'])['vendorname']

res = plpy.execute("SELECT json_build_object('radiusname', vendor_info->'radiusname', 'vendorname', vendor_info->'vendorname', 'label', vendor_info->'l_flag_level') FROM vendor_freeradius")

if res:
 for row in res:
  fd.write(json.dumps(row) + "\n")
  l_flag = json.loads(row['json_build_object'])['label']
  for d_flag in l_flag :
   if d_flag['label'] != 'list_flag' and d_flag['label'] not in l_label:
    l_label.append(d_flag['label'])

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_right_freeradius'")

if res:
 for row in res:
  uid = row['id']

 l_right = json.dumps(l_label)
 res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_right +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.update_right_freeradius() OWNER TO postgres;

--
-- Name: update_vendor_freeradius(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_vendor_freeradius() RETURNS trigger
    LANGUAGE plpythonu
    AS $$

import json
import sys

l_vendor = []
vendorname = json.loads(TD['new']['vendor_info'])['vendorname']
OLDvendorname = json.loads(TD['old']['vendor_info'])['vendorname']

#fd = open('/tmp/test_trigger', 'a')
#fd.write(row['view_data'] + "\n")

res = plpy.execute("SELECT * FROM matview WHERE name = 'list_vendor_freeradius'")
if res:
 for row in res:
  l_vendor = json.loads(row['view_data'])
  uid = row['id']
 if OLDvendorname in l_vendor:
  l_vendor.remove(OLDvendorname)
  l_vendor.append(vendorname)
  l_vendor = json.dumps(l_vendor)
  res = plpy.execute("UPDATE matview SET (view_data) = ('"+ l_vendor +"') WHERE id = "+ str(uid) +"")

$$;


ALTER FUNCTION public.update_vendor_freeradius() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: agent; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE agent (
    id integer NOT NULL,
    agent_info json
);


ALTER TABLE agent OWNER TO dbu_inman;

--
-- Name: agent_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE agent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE agent_id_seq OWNER TO dbu_inman;

--
-- Name: agent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE agent_id_seq OWNED BY agent.id;


--
-- Name: client_freeradius; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE client_freeradius (
    id integer NOT NULL,
    client_info json
);


ALTER TABLE client_freeradius OWNER TO dbu_inman;

--
-- Name: client_freeradius_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE client_freeradius_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE client_freeradius_id_seq OWNER TO dbu_inman;

--
-- Name: client_freeradius_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE client_freeradius_id_seq OWNED BY client_freeradius.id;


--
-- Name: matview; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE matview (
    id integer NOT NULL,
    name character varying(140),
    view_data json
);


ALTER TABLE matview OWNER TO dbu_inman;

--
-- Name: matview_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE matview_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE matview_id_seq OWNER TO dbu_inman;

--
-- Name: matview_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE matview_id_seq OWNED BY matview.id;


--
-- Name: network_perimeter_freeradius; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE network_perimeter_freeradius (
    id integer NOT NULL,
    network_perimeter_info json
);


ALTER TABLE network_perimeter_freeradius OWNER TO dbu_inman;

--
-- Name: network_perimeter_freeradius_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE network_perimeter_freeradius_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE network_perimeter_freeradius_id_seq OWNER TO dbu_inman;

--
-- Name: network_perimeter_freeradius_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE network_perimeter_freeradius_id_seq OWNED BY network_perimeter_freeradius.id;


--
-- Name: plugin; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE plugin (
    id integer NOT NULL,
    plugin_info json
);


ALTER TABLE plugin OWNER TO dbu_inman;

--
-- Name: plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE plugin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE plugin_id_seq OWNER TO dbu_inman;

--
-- Name: plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE plugin_id_seq OWNED BY plugin.id;


--
-- Name: range_freeradius; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE range_freeradius (
    id integer NOT NULL,
    range_info json
);


ALTER TABLE range_freeradius OWNER TO dbu_inman;

--
-- Name: range_freeradius_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE range_freeradius_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE range_freeradius_id_seq OWNER TO dbu_inman;

--
-- Name: range_freeradius_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE range_freeradius_id_seq OWNED BY range_freeradius.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    user_info json
);


ALTER TABLE users OWNER TO dbu_inman;

--
-- Name: users_freeradius; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE users_freeradius (
    id integer NOT NULL,
    user_info json
);


ALTER TABLE users_freeradius OWNER TO dbu_inman;

--
-- Name: users_freeradius_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE users_freeradius_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_freeradius_id_seq OWNER TO dbu_inman;

--
-- Name: users_freeradius_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE users_freeradius_id_seq OWNED BY users_freeradius.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO dbu_inman;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: vendor_freeradius; Type: TABLE; Schema: public; Owner: dbu_inman; Tablespace: 
--

CREATE TABLE vendor_freeradius (
    id integer NOT NULL,
    vendor_info json
);


ALTER TABLE vendor_freeradius OWNER TO dbu_inman;

--
-- Name: vendor_freeradius_id_seq; Type: SEQUENCE; Schema: public; Owner: dbu_inman
--

CREATE SEQUENCE vendor_freeradius_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE vendor_freeradius_id_seq OWNER TO dbu_inman;

--
-- Name: vendor_freeradius_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbu_inman
--

ALTER SEQUENCE vendor_freeradius_id_seq OWNED BY vendor_freeradius.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY agent ALTER COLUMN id SET DEFAULT nextval('agent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY client_freeradius ALTER COLUMN id SET DEFAULT nextval('client_freeradius_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY matview ALTER COLUMN id SET DEFAULT nextval('matview_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY network_perimeter_freeradius ALTER COLUMN id SET DEFAULT nextval('network_perimeter_freeradius_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY plugin ALTER COLUMN id SET DEFAULT nextval('plugin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY range_freeradius ALTER COLUMN id SET DEFAULT nextval('range_freeradius_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY users_freeradius ALTER COLUMN id SET DEFAULT nextval('users_freeradius_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbu_inman
--

ALTER TABLE ONLY vendor_freeradius ALTER COLUMN id SET DEFAULT nextval('vendor_freeradius_id_seq'::regclass);


--
-- Name: agent_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY agent
    ADD CONSTRAINT agent_id_key UNIQUE (id);


--
-- Name: client_freeradius_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY client_freeradius
    ADD CONSTRAINT client_freeradius_id_key UNIQUE (id);


--
-- Name: matview_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY matview
    ADD CONSTRAINT matview_id_key UNIQUE (id);


--
-- Name: network_perimeter_freeradius_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY network_perimeter_freeradius
    ADD CONSTRAINT network_perimeter_freeradius_id_key UNIQUE (id);


--
-- Name: plugin_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY plugin
    ADD CONSTRAINT plugin_id_key UNIQUE (id);


--
-- Name: range_freeradius_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY range_freeradius
    ADD CONSTRAINT range_freeradius_id_key UNIQUE (id);


--
-- Name: users_freeradius_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY users_freeradius
    ADD CONSTRAINT users_freeradius_id_key UNIQUE (id);


--
-- Name: users_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_id_key UNIQUE (id);


--
-- Name: vendor_freeradius_id_key; Type: CONSTRAINT; Schema: public; Owner: dbu_inman; Tablespace: 
--

ALTER TABLE ONLY vendor_freeradius
    ADD CONSTRAINT vendor_freeradius_id_key UNIQUE (id);


--
-- Name: delete_agent_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER delete_agent_freeradius AFTER DELETE ON agent FOR EACH ROW EXECUTE PROCEDURE delete_agent_freeradius();


--
-- Name: delete_client_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER delete_client_freeradius AFTER DELETE ON client_freeradius FOR EACH ROW EXECUTE PROCEDURE delete_client_freeradius();


--
-- Name: delete_flag_vendor_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER delete_flag_vendor_freeradius AFTER DELETE ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE delete_flag_vendor_freeradius();


--
-- Name: delete_network_perimeter_for_user_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER delete_network_perimeter_for_user_freeradius AFTER DELETE ON users_freeradius FOR EACH ROW EXECUTE PROCEDURE delete_network_perimeter_for_user_freeradius();


--
-- Name: delete_right_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER delete_right_freeradius AFTER DELETE ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE delete_right_freeradius();


--
-- Name: delete_vendor_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER delete_vendor_freeradius AFTER DELETE ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE delete_vendor_freeradius();


--
-- Name: list_agent_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER list_agent_freeradius AFTER INSERT ON agent FOR EACH ROW EXECUTE PROCEDURE list_agent_freeradius();


--
-- Name: list_client_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER list_client_freeradius AFTER INSERT ON client_freeradius FOR EACH ROW EXECUTE PROCEDURE list_client_freeradius();


--
-- Name: list_flag_vendor_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER list_flag_vendor_freeradius AFTER INSERT ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE list_flag_vendor_freeradius();


--
-- Name: list_network_perimeter_for_user_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER list_network_perimeter_for_user_freeradius AFTER INSERT ON users_freeradius FOR EACH ROW EXECUTE PROCEDURE list_network_perimeter_for_user_freeradius();


--
-- Name: list_right_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER list_right_freeradius AFTER INSERT ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE list_right_freeradius();


--
-- Name: list_vendor_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER list_vendor_freeradius AFTER INSERT ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE list_vendor_freeradius();


--
-- Name: update_client_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER update_client_freeradius AFTER UPDATE ON client_freeradius FOR EACH ROW EXECUTE PROCEDURE update_client_freeradius();


--
-- Name: update_flag_vendor_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER update_flag_vendor_freeradius AFTER UPDATE ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE update_flag_vendor_freeradius();


--
-- Name: update_network_perimeter_for_user_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER update_network_perimeter_for_user_freeradius AFTER UPDATE ON users_freeradius FOR EACH ROW EXECUTE PROCEDURE update_network_perimeter_for_user_freeradius();


--
-- Name: update_right_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER update_right_freeradius AFTER UPDATE ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE update_right_freeradius();


--
-- Name: update_vendor_freeradius; Type: TRIGGER; Schema: public; Owner: dbu_inman
--

CREATE TRIGGER update_vendor_freeradius AFTER UPDATE ON vendor_freeradius FOR EACH ROW EXECUTE PROCEDURE update_vendor_freeradius();


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

