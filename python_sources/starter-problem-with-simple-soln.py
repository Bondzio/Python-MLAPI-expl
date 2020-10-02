#!/usr/bin/env python
# coding: utf-8

# Notebook provides a toy example of how I think this problem should be solved. This is a very simple solution. I have read the job descriptions manually and selected only one job tree to start with. There is a lot of automation and extension to this possible. It currently doesn't handle certifications or education requirements at all. For a description of the problem I think we are solving see this kernel: https://www.kaggle.com/devinanzelmo/exploring-problem-statement which has a copy of the problem statement that I based the following soln on. 
# 
# 
# This is v1 first draft, lots of work to do. Meaning this is unfinished. 
# 
# Please see this pdf for diagram of this problem. 
# `../input/cityofla/CityofLA/Additional\ data/City\ Job\ Paths/Tree_Surgeon.pdf`
# 
# If anyone wants to fork, and make this prettier please feel free. I will of course use your work in the future. 

# In[12]:


# class for job, hold certification requirements, and 
# prerequisite jobs
class Job(object):
    def __init__(self, name, required_certs, prereq_jobs_list):
        self.name = name
        self.required_certs = required_certs
        self.prereq_jobs_list = prereq_jobs_list
        
    def __repr__(self):
        return '{}'.format(self.name)
        
class Worker(object):
    def __init__(self, name, current_job_name, years_at_job, certifications):
        self.name = name
        self.current_job_name = current_job_name
        self.years_at_job = years_at_job
        self.certifications = certifications 
        
    def __repr__(self):
        return 'name: {}\n job name: {}\n years worked: {}'.format(
            self.name, self.current_job_name, self.years_at_job)
    


# **Create some example jobs**

# In[13]:


tss_name = 'Tree Surgeon Supervisor'
tss_certs = ['pass high voltage line clearance multiple-choice written test',
             'have "Qualified Line Clearance Tree Trimmer" certification',
             'have Certified Commercial Applicators license']
tss_prereqs = [('Tree Sergeon', 3)]
tss = Job(tss_name,
          tss_certs,
          tss_prereqs)


# In[14]:


irg_spec_name = 'Irrigation Specialist'
irg_spec_certs = []
irg_spec_prereqs = [('Senior Gardener', 1), ('Gardener Caretaker', 2)]
irg_spec = Job(irg_spec_name,
               irg_spec_certs,
               irg_spec_prereqs)


# In[15]:


pms_name = 'Park Maintenance Supervisor'
pms_certs = []
pms_prereqs = [('Senior Gardener', 2), ('Irrigation Specialist', 2)]
pms = Job(pms_name,
          pms_certs,
          pms_prereqs)


# In[16]:


spms_name = 'Senior Park Maintenance Supervisor'
spms_certs = []
spms_prereqs = [('Tree Surgeon Supervisor', 2), ('Park Maintenance Supervisor', 2)]
spms = Job(spms_name,
           spms_certs,
           spms_prereqs)


# In[17]:


pgms_name = 'Principal Grounds Maintenance Supervisor'
pgms_certs = []
pgms_prereqs = [('Senior Park Maintenance Supervisor', 2), ('Park Maintenance Supervisor', 4)]
pgms = Job(pgms_name,
           pgms_certs,
           pgms_prereqs)


# **Create some example workers**

# In[18]:


worker_name = 'Worker1'
current_job_name = 'Tree Sergeon'
years_at_job = 2.5
certs = ['have "Qualified Line Clearance Tree Trimmer" certification',
         'have Certified Commercial Applicators license']

worker1 = Worker(worker_name,
                 current_job_name,
                 years_at_job,
                 certs)


# In[19]:


worker_name = 'Worker2'
current_job_name = 'Tree Sergeon'
years_at_job = 3.5
certs = ['have "Qualified Line Clearance Tree Trimmer" certification']

worker2 = Worker(worker_name,
                 current_job_name,
                 years_at_job,
                 certs)


# In[20]:


worker_name = 'Worker3'
current_job_name = 'Tree Sergeon Supervisor'
years_at_job = 4
certs = []

worker3 = Worker(worker_name,
                 current_job_name,
                 years_at_job,
                 certs)


# In[21]:


worker_name = 'Worker4'
current_job_name = 'Senior Gardener'
years_at_job = 2
certs = []

worker4 = Worker(worker_name,
                 current_job_name,
                 years_at_job,
                 certs)


# In[22]:


worker_name = 'Worker5'
current_job_name = 'Irrigation Specialist'
years_at_job = 2.5
certs = []

worker5 = Worker(worker_name,
                 current_job_name,
                 years_at_job,
                 certs)


# **Put all workers and jobs into a list**

# In[23]:


workers = [worker1, worker2, worker3, worker4, worker5]


# In[24]:


all_jobs = [tss, irg_spec, pms, spms, pgms]


# In[25]:


# the two core functions we need to write 
def workers_for_job(job, worker_list):
    """Returns all workers who hold a prerequisite position"""
    job_prereq_names = list()
    possible_workers = list()
    for (job_title, year_req) in job.prereq_jobs_list:
        job_prereq_names.append(job_title)
        
    for worker in worker_list:
        if worker.current_job_name in job_prereq_names:
            possible_workers.append(worker)
            
    return possible_workers
    
    
def jobs_for_worker(worker, job_list):
    """Returns all jobs that are next in sequence for worker"""
    worker_job_name = worker.current_job_name
    possible_jobs = list()
    for job in job_list:
        for (job_title, year_req) in job.prereq_jobs_list:
            if worker_job_name == job_title:
                possible_jobs.append(job)
                
    return possible_jobs


# **Test out the code, and model of problem**

# In[26]:


for worker in workers:
    results = jobs_for_worker(worker, all_jobs)
    print('\n\n', worker, '\n')
    print(results)


# In[27]:


for job in all_jobs:
    results = workers_for_job(job, workers)
    print('\n\n', job, '\n')
    print(results)


# In[ ]:




