#
# (C) Copyright 2012 Vector Guo <vectorguo@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License Version
# 2.1 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

"""fetch a web page.

"""
import sys
import httplib
import re

def fetch_webpage(url) :
    try:
        host = url.replace("http://", "", 1)
        url_parts = host.split('/');
        path = host.replace(url_parts[0], "", 1)
        host = url_parts[0];

        conn = httplib.HTTPConnection(host)
        req = conn.request("GET", path)
        res = conn.getresponse()
    except:
        return fetch_webpage(url)
    return res.read()
