#!/usr/bin/env python

from pprint import pprint

lstofdicts = [
    {'a':'a1', 'b':'b1', 'c':'c1'}
    , {'a':'a2', 'd':'d2', 'c':'c2'}
    ]

# print lstofdicts

# s = set()
# s.add('a')
# print s

# s = set([k for d in lstofdicts for k in d.keys()])
# print s

# for k in sorted(s):
#   print k

def lod2htmltable(lod):
    # Get list of keys, sorted
  ks = sorted(set([k for d in lod for k in d.keys()]))

    # Construct headers
  th = "".join(["<th>%s</th>" % k for k in ks])

    # Construct data rows
  dr = ["".join(["<td>%s</td>" % d.get(k, "-") for k in ks]) for d in lod]
  dr = "\n".join(["<tr>%s</tr>" % e for e in dr])

    # Construct final table
  rv = "\n".join([
          "<table>"
          , "<thead>"
          , th
          , "</thead>"
          , "<tdata>"
          , dr
          , "</tdata>"
          ,"</table>"
        ])
    
  return(rv)

print lod2htmltable(lstofdicts)

