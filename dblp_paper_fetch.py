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
import fetcher

#url -- proceeding page url
url = "http://dblp.uni-trier.de/db/conf/acl/acl2011.html"

if (len(sys.argv) > 1):
    url = sys.argv[1]

index = 0

contents = fetcher.fetch_webpage(url)
paper_links = re.findall('<br><a href="(.*?)"><img alt="Electronic Edition"', contents)
paper_names = re.findall('<b>(.*?)[\.|\?]', contents)

if len(paper_names) != len(paper_links):
    print "fetch paper names & links error!"
else:
    for paper_link in paper_links :
        real_path = re.findall('<a href="(.*?)"', fetcher.fetch_webpage(paper_link))
        if len(real_path) == 0 :
            index = index + 1
            continue
        paper_file = open(paper_names[index].replace("/", " ")+'.pdf', 'w')
        paper_file.write(fetcher.fetch_webpage(real_path[0]))
        paper_file.close()
        index = index + 1
