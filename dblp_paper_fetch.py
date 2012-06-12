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

"""fetch dblp papers of a proceeding in batches.

"""
import sys
import httplib
import re


url = "http://dblp.uni-trier.de/db/conf/acl/acl2011.html"

if (len(sys.argv) > 1):
    url = sys.argv[1]

host = "dblp.uni-trier.de"

conn = httplib.HTTPConnection(host)

req = conn.request("GET", url.replace("http://"+host, "", 1))
res = conn.getresponse()
#print res.read()
contents = res.read()
paper_links = re.findall('<br><a href="(.*?)"><img alt="Electronic Edition"', contents)
paper_names = re.findall('<b>(.*?)\.', contents)
#print paper_links
#print paper_names
index = 0
for paper_link in paper_links :
    host_d = paper_link.replace("http://", "", 1)
    url_parts = host_d.split('/');
    path = host_d.replace(url_parts[0], "", 1)
    host_d = url_parts[0];
    #print host_d
    #print path
    conn_d = httplib.HTTPConnection(host_d)
    req_d = conn_d.request("GET", path)
    res_d = conn_d.getresponse()

    contents_d = res_d.read()
    real_path = re.findall('<a href="(.*?)"', contents_d)
    host_f = real_path[0].replace("http://", "", 1)
    url_parts = host_f.split('/');
    path = host_f.replace(url_parts[0], "", 1)
    host_f = url_parts[0];

    req_f = conn_d.request("GET", path)
    res_f = conn_d.getresponse()

    paper_file = open(paper_names[index]+'.pdf', 'w')
    paper_file.write(res_f.read())
    paper_file.close()
    index = index + 1
