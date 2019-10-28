#!/usr/local/bin/python3
# Accsyn example Python 2/3 script for sending out a outsource file package to a subcontractor/remote employee. See README.md for more information.

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

def create_get_user(user_email):
    ''' Call this function when a user is created, could be triggered by a change in your production database on which your script is listening for events. '''
    session = accsyn_api.Session()
    u = session.find_one("user WHERE code={0}".format(user_email))
    if u is None:
        u = session.create("user",{"code":user_email,"clearance":"user"})
        generic_print("Created Accsyn user '{0}'".format(user_email))
    return u

def create_get_project_share(project_name):
    ''' Call this function when a project is created, could be triggered by a change in your production database on which your script is listening for events. '''
    u = create_get_user()
    share = session.find_one("share WHERE code={0}-outsourcing".format(project_name))
    if share is None:
        share_code = "{0}-outsourcing".format(project_name)
        share = session.create("share", {"code":share_code,"parent":"production","path":project_name})
        generic_print("Created Accsyn share '{0}'".format(share_code))
    return share

def task_assigned(project_name, user_email, p_dataset):
    ''' Call this function when a user is assigned to a task to work on, could be triggered by a change in your production database on which your script is listening for events. p_dataset is the path to task files.'''
    u = create_get_user()
    share = create_get_project_share(project_name)

    acl_source = session.find_one("acl WHERE (ident=user:{0} AND target=share:{1} AND path={2})".format(u['id'], share['id'], p_dataset))
    if acl_source is None:
        acl_source = session.create("acl",{"ident":"user:{0}".format(u['id']),"target":"share:{0}".format(share['id']),"path":p_dataset,"read":True,"write":False})
        generic_print("Granted user '{0}' read access to directory: {1}/{2}".format(user_email, project_name, p_dataset))

    p_taskref="TO_VENDORS"
    acl_ref = session.find_one("acl WHERE (ident=user:{0} AND target=share:{1} AND path={2})".format(u['id'], share['id'], p_taskref))
    if acl_ref is None: 
        acl_ref = session.create("acl",{"ident":"user:{0}".format(u['id']),"target":"share:{0}".format(share['id']),"path":p_taskref,"read":True,"write":False})
        generic_print("Granted user '{0}' read access to directory: {1}/{2}".format(user_email, project_name, p_taskref))

    p_work="FROM_VENDORS/{0}".format(user_email)
    acl_work = session.find_one("acl WHERE (ident=user:{0} AND target=share:{1} AND path={2})".format(u['id'], share['id'], p_work))
    if acl_work is None:
        acl_work = session.create("acl",{"ident":"user:{0}".format(u['id']),"target":"share:{0}".format(share['id']),"path":p_work,"read":True,"write":True})
        generic_print("Granted user '{0}' write access to directory: {1}/{2}".format(user_email, project_name, p_work))

    # Create a accsyn Send transfer job
    job = session.create("job",{
        "code":"{0}_{1}_outsource_{1}"%(project_name, p_dataset, user_email),
        "tasks":{
            "0":{
                "source":"share={0}/{1}".format(share['code'], p_dataset),
                "dest":"{0}:{0}/{1}"%(user_email, project_name, p_dataset)
            },
            "1":{
                "source":"share={0}/TO_VENDORS".format(share['code']),
                "dest":"{0}:TO_VENDORS".format(user_email)
            },
        }
    })
    generic_print("Sent outsource package '{0}'(id:{1}) to user '{2}'".format(job['code'], job['id'], user_email))

    # User will receive an E-mail when package has arrived, signaling task is available to start work on.