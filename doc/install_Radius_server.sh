#!/bin/bash

yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E '%{rhel}').noarch.rpm
yum -y update
yum -y install mlocate
yum -y install openssh-server
yum -y install nano
yum -y install less
yum -y install libtalloc-devel
yum -y install openldap-devel
yum -y install perl 
yum -y install gcc 
yum -y install make 
yum -y install zlib-devel
yum -y install wget
yum -y install automake
yum -y install autoconf
yum -y install libtool
yum -y install openssl
yum -y install openssl-devel
yum -y install openssl-libs
yum -y install openssl-static
yum -y install libmemcached-devel
yum -y install libmemcached
yum -y install rpm-build
yum -y install libpcap-devel
yum -y install collectd
yum -y install libcap-devel
yum -y install gdbm-devel
yum -y install pam-devel
yum -y install perl-devel
yum -y install perl-Glib-devel
yum -y install perl-ExtUtils-Embed
yum -y install json-devel
yum -y install json-c-devel
yum -y install libcurl-devel
yum -y install mysql-devel
yum -y install sqlite-devel
yum -y install postgresql-devel
yum -y install python
yum -y install python-devel
yum -y install python-pip
yum -y install redis
yum -y install freeradius
systemctl enable redis
systemctl start redis

cd install_radius_server
cp radiusd.service /usr/lib/systemd/system/
cp logrotate_freeradius /etc/logrotate.d/
cp logrotate_freeradius_log /etc/logrotate.d/

tar zxf freeradius-server-3.0.15.tar.gz
cd freeradius-server-3.0.15/

./configure --build x86_64-linux-gnu \
	--prefix=/usr \
	--exec-prefix=/usr \
	--mandir=/usr/share/man \
	--sysconfdir=/etc \
	--libdir=/usr/lib/freeradius \
	--datadir=/usr/share \
	--localstatedir=/var \
	--with-raddbdir=/etc/freeradius \
	--with-logdir=/var/log/freeradius \
	--enable-ltdl-install=no --enable-strict-dependencies \
	--with-large-files --with-udpfromto --with-edir \
	--enable-developer \
	--config-cache \
	--without-rlm_eap_tnc \
	--with-rlm_sql_postgresql_lib_dir=`pg_config --libdir` \
	--with-rlm_sql_postgresql_include_dir=`pg_config --includedir` \
	--without-rlm_eap_ikev2 \
	--without-rlm_sql_oracle \
	--without-rlm_sql_unixodbc \
	--with-system-libtool \
	--without-rlm_couchbase \
	--without-rlm_idn \
	--without-rlm_opendirectory \
	--without-rlm_redis \
	--without-rlm_rediswho \
	--without-rlm_ruby \
	--without-rlm_securid \
	--without-rlm_sql_firebird \
	--without-rlm_sql_db2 \
	--without-rlm_sql_iodbc \
	--without-rlm_sql_freetds \
	--without-rlm_unbound \
	--without-rlm_yubikey

make && make install

cd ..

systemctl daemon-reload
systemctl enable radiusd
systemctl start radiusd

whiptail --title "For LDAP : Don't forget" --msgbox ". In /etc/freeradius/mods-available/ldap edit your configuration to correctly join your LDAP\n. Create a symbolic link between mods-available/ldap mods-enable/ldap\n. Use or uncomment ldap line in /etc/freeradius/sites-enabled/default" 15 78

###
# Just incase for Freeradius >= 4.* or 3.1 compile problem
###
# On CentOS, install package centos-release-scl available in CentOS repository:
# yum install centos-release-scl

# On RHEL, enable RHSCL repository for you system:
# yum-config-manager --enable rhel-server-rhscl-7-rpms

#yum -y install devtoolset-3-gcc
#yum -y install devtoolset-3-gcc-c++
#scl enable devtoolset-3 bash

#VERSION=2.1.0
#wget https://github.com/mheily/libkqueue/archive/v${VERSION}.tar.gz
#tar -xvzf v${VERSION}.tar.gz
#cd ./libkqueue-${VERSION}
#sed -ie "s/Version:.*/Version:    ${VERSION}/" ./libkqueue.spec
#sed -ie "s/%{_mandir}\/man2\/kevent.2.*//" ./libkqueue.spec
#sed -ie "s/^%{make_install}.*/%{make_install} \&\& rm -rf %{_libdir}\/*.a \&\& rm -rf %{_libdir}\/*.la/" ./libkqueue.spec
#autoreconf -i
#cd ..
#tar -czf ./libkqueue-${VERSION}.tar.gz ./libkqueue-${VERSION}

# Only required if you don't already have a build environment setup
#mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
#cp ./libkqueue-${VERSION}.tar.gz ~/rpmbuild/SOURCES/libkqueue-${VERSION}.tar.gz
#rpmbuild -ba ./libkqueue-${VERSION}/libkqueue.spec