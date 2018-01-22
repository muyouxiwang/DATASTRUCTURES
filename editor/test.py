# -*- coding=utf-8 -*-







#print len(u"为人民")
#print len(u"a为人民")
#print len("a为人民dd")


import re

p = re.compile("(abc)")


t = "lsfabcsdeabclsdfabclsdl"


print t.index("abc")
print t.find("abc")
