with open("result.json") as f:
    lines = f.readlines()


with_s = [x for x in lines if x.startswith('  "RPC"')]

for x in with_s:
    print(x[9:])


# print(this_list)
