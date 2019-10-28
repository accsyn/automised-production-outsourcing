#!/usr/local/bin/python3
# Accsyn Hook example Python 2/3 script for post-processing a subcontractor upload 

import json,sys,os

import accsyn_api

def generic_print(s):
    try:
        if ((3, 0) < sys.version_info):
            # Python 3 code in this block
            expr = """print(s)"""
        else:
            # Python 2 code in this block
            expr = """print s"""
        eval(expr)
    except:
        pass


def publish(user=None, comment=None, filename=None):
    ''' Do something with data uploaded by user. '''
    generic_print("User {0} published '{1}' ,comment: {2}".format(user, filename, comment))

if __name__ == '__main__':

    p_input = sys.argv[1]
    data = json.load(open(p_input, "r"))
    generic_print("Publish hook incoming data from user %s: %s"%(data['user_hr'], json.dumps(data, indent=3)))

    # Find the output amongst files
    for p in [d["source"]["path_abs"] for d in data["tasks"].values()]:
        if p.lower().endswith("_exported.dat"):
            publish(user=data["source_hr"].split(":")[1], comment="Subcontractor publish", filename=p)
    