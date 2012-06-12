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

"""fetch acmlib papers of a proceeding in batches.

"""
import sys
import httplib
import re

pNo = 0
size = 2

if (len(sys.argv) > 1):
    pNo = sys.argv[1]

if (len(sys.argv) > 2):
    size = int(sys.argv[2])

host_s = "acm.lib.tsinghua.edu.cn"
mpath_s = "/acm/Detail-List.nsp?&view=ACM&cid_PCODE=&cid_DOCTYPE=&cid_HASABSTRACT=&cid_HASFULLTEXT=&lastquery=(pNo):PROC_ID&sortfield=SECTION_SEQ_NO,SEQ_NO,PUBDATE&sortorder=ASCENDING,ASCENDING,ASCENDING&var_AUTHCODE=&var_PUBCODE=&var_BROWSECODE=&var_SOURCECODE=&recid=&reccode=&mailto=&docindex=iNo&var_SECTION=&numresults=25&fromrecord=&usertag="

host_d = "166.111.120.94"
mpath_d = "/acm/ContentLoader.nsp?view=path"
mpath_f = "/acm/path"

conn_s = httplib.HTTPConnection(host_s)
mpath_s = mpath_s.replace("pNo", pNo, 1)

conn_d = httplib.HTTPConnection(host_d)

for i in range(0, size) :
    #print mpath_s.replace("iNo", str(i), 1)
    req_s = conn_s.request("GET", mpath_s.replace("iNo", str(i), 1))
    res_s = conn_s.getresponse()
    #print res_s.read()
    #
    ## find paper name & link & save file
    contents_s = res_s.read()
    paper_name = re.findall('<b><img src="img/spacer.gif"><br>(.*?)</b>', contents_s);
    #print paper_name
    paper_path = re.findall('fl = "(.*?)"', contents_s)
    #print paper_path
    req_d = conn_d.request("GET", mpath_d.replace("path", paper_path[0], 1))
    res_d = conn_d.getresponse()
    contents_d = res_d.read()
    real_path = re.findall('top.location.replace\("(.*?)"', contents_d)
    #print real_path
    req_f = conn_d.request("GET", mpath_f.replace("path", real_path[0], 1))
    res_f = conn_d.getresponse()
    paper_file = open(paper_name[0]+'.pdf', 'w')
    paper_file.write(res_f.read())
    paper_file.close()
