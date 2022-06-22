#!/usr/local/bin/python3

# read all TF files in a directory and look for anything "bad"

import sys, re, glob

# Where are my terraform files stored
files = "terraform/*.tf"

# prefix - resources must start with this prefix
allowed_prefix = "team-a"

regexes = [
    r"topic_name\s*=\s*\"([^\"]+)\""
]

# Compile all regexes for moar performance
regexes = [re.compile(r) for r in regexes]

ret = 0 # Assume OK

try:
    for filename in glob.iglob(files):
        print(f">>> {filename} ")
        with open(filename) as f:
            data = f.read() # read in everything, rather than line-by-line
            for regex in regexes:
                for match in regex.finditer(data, re.M):
                    match_str = match.group(0)
                    match_grp = match.group(1)
                    if not match_grp.startswith(allowed_prefix):
                        print(f"Found new resource [{match_str}] that does not match allowed prefix, [{allowed_prefix}]")
                        ret = 1
except Exception as e:
    print("Exception analysing TF files, return with fail status code")
    print(e)
    sys.exit(1)

# All files analysed, return appropraite return code
sys.exit(ret)
