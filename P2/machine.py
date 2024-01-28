# 2021400297 Soner Kuyar Group 44
# 2021400123 Yunus Kağan Aydın Group 44

from mpi4py import MPI
import numpy as np


class Machine:
    def __init__(self, machine_id, machine_tree , wear_factors, threshold):
        self.ID = machine_id
        self.Tree = machine_tree
        self.ParentID = machine_tree['parent']
        self.operation = machine_tree['operation']
        self.Children = machine_tree['children']
        self.wear_factors = wear_factors
        self.threshold = threshold
        self.accumulated_wear = 0
        self.cycle = 1

    def machine_operation_cycle(self, products) -> str:
        # process products
        product = self._apply_operation(products)
        # TODO: calculate accumulated wear factor for operated machine
        maintanence_cost = self._calculate_accumulated_wear()
        if maintanence_cost:
            log = f"{self.ID}-{maintanence_cost}-{self.cycle}"
            req = COMM.isend(log, dest=0, tag=1002)
            req.wait()
            self.accumulated_wear = 0

        # channge the operation of the machine 
        self._change_operation()

        return product
    
    def _apply_operation(self, products) -> str:
        
        product = ''.join(products)
        

        if self.operation == 'enhance':
            product = product[0] + product + product[-1]
        
        elif self.operation == 'reverse':
            product = product[::-1]
        
        elif self.operation == 'chop':
            if len(product) > 1:
                product = product[:-1]
       
        elif self.operation == 'trim':
            if len(product) > 2:
                product = product[1:-1]
        
        elif self.operation == 'split':
            product = product[:len(product)//2 + len(product)%2]
        
        return product
    # apply operation function private to the class

    def _calculate_accumulated_wear(self) -> int:
        maintanence_cost = 0
        if self.operation == None:
            return maintanence_cost
        
        wf = self.wear_factors[self.operation]
        self.accumulated_wear += wf
        if self.accumulated_wear >= self.threshold:
            maintanence_cost = (self.accumulated_wear - self.threshold + 1) * wf
        return maintanence_cost
            

    
    def _change_operation(self):
        odd_machines = ['trim', 'reverse']
        even_machines = ['split', 'chop', 'enhance']

        if self.operation in odd_machines:
            self.operation = 'reverse' if self.operation == 'trim' else 'trim'

        elif self.operation in even_machines:
            self.operation = even_machines[(even_machines.index(self.operation) + 1) % 3]

        self.Tree['operation'] = self.operation

COMM_MACHINES = MPI.COMM_WORLD
COMM = MPI.Comm.Get_parent()
rank = COMM.Get_rank()

machine_id = rank + 1 # machine id is rank + 1

# get wear factors from control room
common_values = np.empty(8, dtype='i')
COMM.Bcast(common_values, root=0)

# wear factors are in the first 5 elements of common_values
wear_factors = {'enhance': common_values[0], 'reverse': common_values[1], 'chop': common_values[2], 'trim': common_values[3], 'split': common_values[4]}
N = common_values[5]
C = common_values[6]
threshold = common_values[7]

del common_values # free resource
# get the machine tree from control room
machine_tree = COMM.recv(source=0)


# Create machine instance
products = []
machine = Machine(machine_id, machine_tree, wear_factors, threshold)
if not machine.Children :
    products.append(COMM.recv(source=0, tag=1001)) # 1001 is the tag for input products
  
while machine.cycle <= C:
    if not machine.Children:
        product = machine.machine_operation_cycle(products)
        # send product to parent
        COMM_MACHINES.send(product, dest=machine.ParentID - 1, tag=machine.ID)

    # If machine is not leaf, get the products from children
    else: 
        for child_id in machine.Children:
            products.append(COMM_MACHINES.recv(source=child_id - 1, tag=child_id))
        
        product = machine.machine_operation_cycle(products)
        
        # If machine is root, send the product to control room
        if machine.ID == 1:
            COMM.send(product, dest=0, tag=0)
        # If machine is not root, send the product to parent
        else:
            
            COMM_MACHINES.send(product, dest=machine.ParentID - 1, tag=machine.ID)
        products.clear()
    machine.cycle += 1


COMM.Disconnect()
