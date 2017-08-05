#!/usr/bin/python3
# -*- coding=utf-8 -*-

from ldap3 import Server, Connection, AUTO_BIND_NO_TLS

server = Server('ldap://172.16.66.6') 


def qytldap(username, password):
    try:
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=True,check_names=True, user="qytang\\"+username, password=password)
        c.search(search_base = 'dc=qytang,dc=com', search_filter = '(&(samAccountName=' + username + '))',attributes = ['memberOf','Sn'],paged_size = 5)
        return (c.response[0]['attributes']['memberOf'],c.response[0]['attributes']['Sn'])
    except Exception:
        return None


if __name__ == "__main__":
    print(qytldap('rsec-zhumin','Cisc0123'))
