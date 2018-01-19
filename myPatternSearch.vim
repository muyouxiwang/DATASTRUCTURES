


function! PatternSearch(pat)


python << EOF

import vim
import re
import os
import traceback

exts = set(["py", "js", "html", "htm", "css"])

p = vim.eval("a:pat").strip()
#print "your search pattern is : %s\n" % p

search_result = []
try:
    p = re.compile(p)
    for curdir, _, files in os.walk("."):
        for filename in files:
            if filename.rfind(".") != -1:
                ext = filename.split(".")[-1].lower()
                if ext in exts:
                    filepath = os.path.join(curdir, filename)
                    linenum = 0
                    with open(filepath) as rf:
                        for line in rf:
                            linenum += 1
                            line = line.strip()
                            if line:
                                data = p.search(line)
                                if data is not None:
                                    search_result.append("%s:%d:%s" % (filepath, linenum, line))
                                    #print "find in %s: %s" % (filepath, line)


    vim.command("set errorformat=%f:%l:%m")

    vim.command("let b:ret_lst = []")
    for item in search_result:
        item = item.replace("\\", r"\\").replace("\"", r"\"")
        vim.command("call add(b:ret_lst, \"%s\")" % item)
    vim.command("cex b:ret_lst")

    vim.command("cw")

    #vim.command("cex \"%s\"" % search_result[0].replace("\\", r"\\"))
    #for item in search_result[1:]:
    #    item = item.replace("\\", r"\\").replace("\"", r"\"")
    #    vim.command("cadde \"%s\"" % item)


except:
    print "search ERROR: %s" % traceback.format_exc()


EOF
endfunction



