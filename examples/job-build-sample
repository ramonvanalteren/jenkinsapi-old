from jenkinsapi import api

obj = api.Jenkins(url)
job = obj.get_job(jobname)

build = job.invoke(jobname, build_params={"param":"value"})

# then we can access this build via get_last_build method

build_obj = job.get_last_build()

# build_obj getting status , timestamp etc.
