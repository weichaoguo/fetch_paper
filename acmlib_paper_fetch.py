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
import fetcher

#pNo -- PROC_ID
#size -- PAPER_NUM
pNo = 0
size = 2

if (len(sys.argv) > 1):
    pNo = sys.argv[1]

if (len(sys.argv) > 2):
    size = int(sys.argv[2])

detail_list_url = "http://acm.lib.tsinghua.edu.cn/acm/Detail-List.nsp?&view=ACM&cid_PCODE=&cid_DOCTYPE=&cid_HASABSTRACT=&cid_HASFULLTEXT=&lastquery=(pNo):PROC_ID&sortfield=SECTION_SEQ_NO,SEQ_NO,PUBDATE&sortorder=ASCENDING,ASCENDING,ASCENDING&var_AUTHCODE=&var_PUBCODE=&var_BROWSECODE=&var_SOURCECODE=&recid=&reccode=&mailto=&docindex=iNo&var_SECTION=&numresults=25&fromrecord=&usertag="

content_url = "http://166.111.120.94/acm/ContentLoader.nsp?view=path"
file_url = "http://166.111.120.94/acm/path"

detail_list_url = detail_list_url.replace("pNo", pNo, 1)

for i in range(0, size) :
    contents = fetcher.fetch_webpage(detail_list_url.replace("iNo", str(i), 1))

    paper_name = re.findall('<b><img src="img/spacer.gif"><br>(.*?)</b>', contents);
    #print paper_name
    paper_path = re.findall('fl = "(.*?)"', contents)
    p_len = len(paper_path)
    index = 0
    while index < p_len:
        if not paper_path[index].endswith(".pdf") :
            del paper_path[index]
            p_len = p_len - 1
        else :
            index = index + 1
    if len(paper_path) == 0 :
        continue
    real_path = re.findall('top.location.replace\("(.*?)"', fetcher.fetch_webpage(content_url.replace("path", paper_path[0], 1)))
    if len(real_path) == 0 :
        continue
    paper_file = open(paper_name[0].replace("/", " ")+'.pdf', 'w')
    paper_file.write(fetcher.fetch_webpage(file_url.replace("path", real_path[0], 1)))
    paper_file.close()
