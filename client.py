#!/usr/local/bin/python3
# Accsyn example Python 2/3 script enabling subcontractor/remote employee upload of file package back to servers. 


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


def upload_results(project_dir, share_name, task_name, files):
    ''' Triggered for example by a button within 3rd party application or command line/gui launcher 

    project_dir="E:\\WORK\\GEOSCAN\\Production\\proj002"
    share_name="proj002-outsourcing"
    task_name="DATASET_001_1203"
    files=[
        "FROM_VENDORS\\jennifer@gda.com\\cleaned_set.dat",                           # An asset
        "FROM_VENDORS\\jennifer@gda.com\\proj002_DATASET_001_1203.analyze",          # The project file
        "FROM_VENDORS\\jennifer@gda.com\\output\\proj002_DATASET_001_1203_exported.dat",      # The output
    ]
    '''

    import accsyn_api
    session = accsyn_api.Session()

    tasks = {}

    n = 0
    for p in files:
        tasks[str(n)] = {"source":"%s\\%s"%(project_dir,p),"destination":"acmefilme:share=%s:%s"%(share_name,p)}
        n += 1

    job = session.create("job",{
       "code":"%s_output"%(task_name),
       "tasks":tasks
    })

    generic_print("Submitted upload package '{0}'(id:{1})".format(job['code'], job['id']))

