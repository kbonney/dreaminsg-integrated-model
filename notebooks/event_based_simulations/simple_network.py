#!/usr/bin/env python
# coding: utf-8

# # Testing the Integrated Simulation Platform
# This notebook contains codes to test the various functionalities of the integrated simulation platform. You can call any of the modules from the package here. 

# In[5]:


# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')

import warnings 
warnings.filterwarnings('ignore')

from IPython.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# ## Import required packages

# In[6]:


from pathlib import Path
from infrarisk.src.network_recovery import *
import infrarisk.src.simulation as simulation
from infrarisk.src.physical.integrated_network import *
import infrarisk.src.recovery_strategies as strategies

from infrarisk.src.physical.interdependencies import *

from infrarisk.src.optimizer import *
import infrarisk.src.plots as model_plots

#import random


# ## Create an IntegratedNetwork object

# In[7]:


simple_network = IntegratedNetwork(name = "Simple")


# ### Load the three infrastructure models: Water, Power and Transportation
# 
# Three different models are used:
# - Water distribution network using **wntr** package
# - Power systems using **pandapower** package
# - Transportation network using static traffic assignment package developed by Dr. Stephen Boyles (University of Texas at Austin)

# In[8]:


MAIN_DIR = Path('../..')
SIM_STEP = 60

network_dir= 'infrarisk/data/networks/in2'
water_folder = MAIN_DIR/f'{network_dir}/water'
power_folder = MAIN_DIR/f'{network_dir}/power'
transp_folder = MAIN_DIR/f'{network_dir}/transportation/'

# load all infrastructure networks
simple_network.load_networks(water_folder=water_folder, 
                             power_folder=power_folder, 
                             transp_folder=transp_folder,
                             sim_step=SIM_STEP)


# ### Create a Networkx graph of the integrated infrastructure network.

# In[31]:


simple_network.generate_integrated_graph()


# ### Build interdependencies
# 
# Three types of dependencies:
# - Power - Water dependencies (eg.: water pump on electric motor, generator on reservoir)
# - Power - Transportation dependencies (eg.: road access to power system components for M&R)
# - Water - Transportation dependencies (eg.: road access to water network components for M&R)
# 
# The dependencies are referenced using two tables in the model.
# - **wp_table** for water - power dependencies
# - **access_table** for transportation dependencies

# In[10]:


dependency_file = MAIN_DIR/f"{network_dir}/dependecies.csv"
simple_network.generate_dependency_table(dependency_file = dependency_file)
simple_network.dependency_table.wp_table


# In[11]:


simple_network.dependency_table.access_table.head()


# ### Set failed components

# In[12]:


scenario_folder = "scenarios/test1"
disruption_file = MAIN_DIR/f"{network_dir}/{scenario_folder}/disruption_file.csv"

simple_network.set_disrupted_components(disruption_file=disruption_file)
simple_network.get_disrupted_components()


# ### Set initial crew locations

# In[13]:


simple_network.deploy_crews(
    init_power_crew_locs=['T_J8'], 
    init_water_crew_locs=['T_J8'],
    init_transpo_crew_locs= ['T_J8']
    )


# ## Simulation of interdependent effects using a test scenario
# ### (a) Create NetworkRecovery

# In[14]:


network_recovery = NetworkRecovery(simple_network, 
                                   sim_step=SIM_STEP, 
                                   pipe_close_policy="repair",
                                   pipe_closure_delay= 10, 
                                   line_close_policy="sensor_based_line_isolation",
                                   line_closure_delay= 10)


# ### (b) Create a simulation object

# In[16]:


bf_simulation = simulation.NetworkSimulation(network_recovery)


# ### (c) Generation of random repair order

# In[17]:


capacity_strategy = strategies.HandlingCapacityStrategy(simple_network)
capacity_strategy.set_repair_order()
repair_order = capacity_strategy.get_repair_order()

import os
if not os.path.exists(MAIN_DIR/f"{network_dir}/{scenario_folder}/capacity"):
    os.makedirs(MAIN_DIR/f"{network_dir}/{scenario_folder}/capacity")


# In[18]:


#Generate a random repair order
# repair_order = network_recovery.network.get_disrupted_components()
# random.shuffle(repair_order)
print('Current repair order is {}'.format(repair_order))


# ### (d) Generation of event tables

# In[19]:


bf_simulation.network_recovery.schedule_recovery(repair_order)


# In[21]:


#bf_simulation.network_recovery.event_table.to_csv("event_tbl.csv", sep = "\t", index = False)
bf_simulation.expand_event_table()


# ### (e) Simulation of interdependent effects

# In[22]:


resilience_metrics = bf_simulation.simulate_interdependent_effects(
    bf_simulation.network_recovery)


# In[23]:


strategy = 'capacity'
bf_simulation.write_results(f"{MAIN_DIR}/{network_dir}/{scenario_folder}/{strategy}", 
                            resilience_metrics)


# ### (f) Calculation of resilience metric

# In[24]:


resilience_metrics.calculate_power_resmetric(network_recovery)


# In[25]:


resilience_metrics.calculate_water_resmetrics(network_recovery)


# In[26]:


resilience_metrics.set_weighted_auc_metrics()


# # Plot network performance during the disruption

# ### Overall system performance considering indirect effects

# In[27]:


model_plots.plot_interdependent_effects(resilience_metrics, metric = 'pcs', title = False)


# In[35]:


model_plots.plot_disruptions_and_crews(simple_network)

