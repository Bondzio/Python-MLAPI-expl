#!/usr/bin/env python
# coding: utf-8

# MIPCL: https://mipcl-cpp.appspot.com/
# >MIPCL is currently one of the fastest non-commercial mixed integer programming solvers. It can be used together with a modeling tool named MIPshell.
# 

# This kernel uses the code from: [Benchmark MIP solvers(Draft)](https://www.kaggle.com/golubev/benchmark-mip-solvers-draft)

# Setup

# In[ ]:


get_ipython().run_cell_magic('bash', '', '# Install Python 2.7 because the shared library of MIPCL for Python3 is broken (link error).\ngit clone git://github.com/yyuu/pyenv.git ~/.pyenv\necho \'export PYENV_ROOT="$HOME/.pyenv"\' >> ~/.bash_profile\necho \'export PATH="$PYENV_ROOT/bin:$PATH"\' >> ~/.bash_profile\necho \'eval "$(pyenv init -)"\' >> ~/.bash_profile\nsource ~/.bash_profile\napt-get install -y libssl-dev libreadline-dev\npyenv install 2.7.17\npyenv local 2.7.17\npip install pandas numpy\n\n# Install MIPCL(mipcl_py module)\nwget https://mipcl-cpp.appspot.com/static/download/mipcl-py-2.6.1.linux-x86_64.tar.gz\ntar --exclude=\'*docs\' -xzvf mipcl-py-2.6.1.linux-x86_64.tar.gz # exclude docs directory due to `too many nested subdirectories error` in kaggle kernel\nrm -f ./mipcl_py/mipshell/mipcl.so\nln -s mipcl-py2.so ./mipcl_py/mipshell/mipcl.so # Use mipcl-py2')


# Benchmark code from https://www.kaggle.com/golubev/benchmark-mip-solvers-draft

# In[ ]:


get_ipython().run_cell_magic('bash', '', 'source ~/.bash_profile\npython <<__EOF__\nfrom __future__ import print_function\nimport time\nimport numpy as np\nimport pandas as pd\nimport mipcl_py.mipshell.mipshell as mipshell\n\ndef get_days(assigned_days, n_people):\n    days = np.zeros(assigned_days.max(), int)\n    for i, r in enumerate(assigned_days):\n        days[r-1] += n_people[i]\n    return days\n\n\ndef example_mipcl(desired, n_people):\n    def accounting_penalty(day, next_day):\n        return (day - 125.0) * (day**(0.5 + abs(day - next_day) / 50.0)) / 400.0\n    FAMILY_COST = np.asarray([0,50,50,100,200,200,300,300,400,500])\n    MEMBER_COST = np.asarray([0, 0, 9,  9,  9, 18, 18, 36, 36,235])\n    num_days = desired.max()\n    num_families = desired.shape[0]\n    solver = mipshell.Problem(name=\'Santa2019 only preference\')\n    C, B, I = {}, {}, {}\n\n    for fid, choices in enumerate(desired):\n        for cid in range(10):\n            B[fid, choices[cid]-1] = mipshell.Var(type=mipshell.BIN, lb=0.0, ub=1.0)\n            C[fid, choices[cid]-1] = FAMILY_COST[cid] + n_people[fid] * MEMBER_COST[cid]\n\n    for day in range(num_days):\n        I[day] = mipshell.Var(type=mipshell.INT, lb=125, ub=300)\n        mipshell.sum_(n_people[fid]*B[fid, day] for fid in range(num_families) if (fid,day) in B) == I[day]\n\n    for fid in range(num_families):\n        mipshell.sum_(B[fid, day] for day in range(num_days) if (fid,day) in B) == 1\n\n    objective = mipshell.sum_(C[fid, day]*B[fid, day] for fid, day in B)\n\n    solver.minimize(objective)\n    solver.optimize(silent=False, gap=0.0)\n    if solver.is_solution:\n        print("Result: ", solver.getObjVal())\n        assigned_days = np.zeros(num_families, int)\n        for fid, day in B:\n            if B[fid, day].val > 0.5:\n                assigned_days[fid] = day + 1\n        return assigned_days\n    else:\n        print("Failed", solver.is_solution, solver.is_infeasible, solver.isPureLP)\n        return None\n\n\ndef save(assigned_days):\n    with open("submission.csv", "w") as f:\n        f.write("family_id,assigned_day\\n")\n        for fid, v in enumerate(assigned_days):\n            f.write("{},{}\\n".format(fid, v))\n\n\nif __name__ == "__main__":\n    ds = pd.read_csv(\'../input/santa-workshop-tour-2019/family_data.csv\')\n    t = time.time()\n    ret = example_mipcl(ds.values[:,1:11], ds.values[:,11])\n    if ret is not None:\n        save(ret)\n    print("Elapsed time", time.time() - t)\n__EOF__')


# 43622 is the optimal preference cost mentioned in https://www.kaggle.com/mihaild/lower-bound-on-preference-cost#685643
