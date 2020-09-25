import topogenesis as tg
import numpy as np
np.random.seed(0)

# agent class


class agent():
    def __init__(self, origin, stencil, id):

        # define the origin attribute of the agent and making sure that it is an intiger
        self.origin = np.array(origin).astype(int)
        # define old origin attribute and assigning the origin to it as the initial state
        self.old_origin = self.origin
        # define stencil of the agent
        self.stencil = stencil
        # define agent id
        self.id = id
        # define the list of occupied cells by agent
        self.occ_cells = [self.origin]

    # definition of walking method for agents
    def walk(self, env):
        # find available spaces
        #######################

        # retrieve the list of neighbours of the agent based on the stencil
        neighs = env.availibility.find_neighbours_masked(
            self.stencil, loc=self.origin)
        # find availability of neighbours
        neighs_availibility = env.availibility.flatten()[neighs]
        # separate available neighbours
        free_neighs = neighs[neighs_availibility == 1]
        # check to see if there is any available neighbour
        if len(free_neighs) == 0:
            return 1
        # retrieve the myvalue of each neighbour
        free_neighs_myvalue = env.myvalue.flatten()[free_neighs]
        # find the neighbour with maximum my value
        selected_neigh = free_neighs[np.argmax(free_neighs_myvalue)]

        # update information
        ####################

        # set the current origin as the ol origin
        self.old_origin = self.origin
        # update the current origin with the new selected neighbour
        self.origin = np.array(np.unravel_index(
            selected_neigh, env.availibility.shape)).flatten()

        # update environment information
        ################################

        # making previous position available
        env.availibility[tuple(self.old_origin)] = env.availibility[tuple(
            self.old_origin)] * 0 + 1
        # removing agent from previous position
        env.agent_origin[tuple(self.old_origin)] *= 0
        # making the current position unavailable
        env.availibility[tuple(self.origin)] *= 0
        # adding agent to the new position
        env.agent_origin[tuple(self.origin)] = self.id

    # definition of walking method for agents
    def occupy(self, env):
        # find available spaces
        #######################

        # retrieve the list of neighbours of the agent based on the stencil
        neighs = []
        for cell in self.occ_cells:
            cell_neighs = env.availibility.find_neighbours_masked(
                self.stencil, loc=cell)
            neighs.append(cell_neighs)
        neighs = np.concatenate(tuple(neighs))
        # find availability of neighbours
        neighs_availibility = env.availibility.flatten()[neighs]
        # separate available neighbours
        free_neighs = neighs[neighs_availibility == 1]
        # check to see if there is any available neighbour
        if len(free_neighs) == 0:
            return 1
        # retrieve the myvalue of each neighbour
        free_neighs_myvalue = env.myvalue.flatten()[free_neighs]
        # find the neighbour with maximum my value
        selected_neigh = free_neighs[np.argmax(free_neighs_myvalue)]

        # update information
        ####################

        # retrieve the neighbour 3d indicies
        sel_neigh_3dind = np.array(np.unravel_index(
            selected_neigh, env.availibility.shape)).flatten()
        # add neighbour to the list of occpied cells
        self.occ_cells.append(sel_neigh_3dind)

        # update environment information
        ################################

        # making previous position available
        # env.availibility[tuple(self.old_origin)] = env.availibility[tuple(self.old_origin)] * 0 + 1
        # removing agent from previous position
        # env.agent_origin[tuple(self.old_origin)] *= 0
        # making the current position unavailable
        env.availibility[tuple(sel_neigh_3dind)] *= 0
        # adding agent to the new position
        env.agent_origin[tuple(sel_neigh_3dind)] = self.id


# initiate availibility lattice
unit = 1
bounds = np.array([[0, 0, 0], [lattice_size, lattice_size, lattice_size]])
avail_lattice = tg.lattice(bounds, unit=unit, default_value=1, dtype=int)

# randomly scattering the agents
selected_cells = np.random.choice(avail_lattice.size, agent_count)
agent_ind = np.array(np.unravel_index(selected_cells, avail_lattice.shape))

# creating neighborhood definition
stencil = tg.stencil(np.array([[[0, 0, 0],
                                [0, 1, 0],
                                [0, 0, 0]],
                               [[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]],
                               [[0, 0, 0],
                                [0, 1, 0],
                                [0, 0, 0]]]), origin=np.array([1, 1, 1]))

agents = []
# creating agent objects
for id, ind in enumerate(agent_ind.T.tolist()):
    myagent = agent(ind, stencil, id+1)
    agents.append(myagent)

# environment class


class environment():
    def __init__(self, lattices, agents):
        self.availibility = lattices["availibility"]
        self.myvalue = lattices["myvalue"]
        self.agent_origin = self.availibility * 0
        self.agents = agents
        self.update_agents()

    def update_agents(self):
        # deprecated since the availibility lattice is updated inside the agent method
        for a in self.agents:
            # making previous position available
            self.availibility[tuple(a.old_origin)] = self.availibility[tuple(
                a.old_origin)] * 0 + 1
            # removing agent from previous position
            self.agent_origin[tuple(a.old_origin)] *= 0
            # making the current position unavailable
            self.availibility[tuple(a.origin)] *= 0
            # adding agent to the new position
            self.agent_origin[tuple(a.origin)] = a.id

    def agents_walk(self):
        # iterate over egents and perform the walk
        for a in self.agents:
            a.walk(self)
        # update the agent states in environment
        self.update_agents()

    def agents_occupy(self):
        # iterate over egents and perform the walk
        for a in self.agents:
            a.occupy(self)
        # update the agent states in environment
        # self.update_agents()

# construct a dummy value field
###############################


# create a series of sin values for 0 to pi
sin_a = np.sin(np.arange(lattice_size+1) /
               float(lattice_size) * np.pi).astype(np.float16)
# compute the outer product of the series with itself to create a radial value field
myvalue_2d_field = np.outer(sin_a, sin_a)
# add extra dimension to array to make it comaptible with lattices
myvalue_field = myvalue_2d_field[:, :, None] * sin_a[None, None, :]
# construct the lattice
myvalue_lattice = tg.to_lattice(myvalue_field, np.array([0, 0, 0]))


# initiate the environment
env_lattices = {"availibility": avail_lattice,
                "myvalue": myvalue_lattice}
env = environment(env_lattices, agents)

# main simulation
agent_history = [[]]
occ_count = [0]
for i in range(max_iteration):
    # print(env.availibility)
    # print(env.agent_origin)
    agn_occ = np.argwhere(env.availibility == 0)
    agn_occ_list = agn_occ.tolist()
    agent_history.append(agn_occ_list)
    occ_count.append(len(agn_occ_list) + occ_count[i])
    # agn_org = [a.origin for a in env.agents]
    # agent_history.append(np.array(agn_org).tolist())
    # env.agents_walk()
    env.agents_occupy()

Agent_History = agent_history
Occupation_Count = occ_count
print(occ_count)
