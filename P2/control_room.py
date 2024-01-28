from mpi4py import MPI
import numpy as np
import sys



# get the input file path from arguments
input_file = sys.argv[1]
# get the output file path from arguments
output_file = sys.argv[2]

N = 0 # number of machines
C = 0 # cycles number
wear_factors = {'enhance':0 ,'reverse': 0, 'chop':0, 'trim':0, 'split': 0} # wear factors for each machine
threshold = 0 
machine_tree = {} # machine tree
products = [] # list of products to be processed


with open(input_file, 'r') as f:
    # read first line: number of machines
    N = int(f.readline())
    # read second line: cycles number
    C = int(f.readline())
    # read third line: wear factors
    wear_factors_values = f.readline().split()
    # read fourth line: threshold
    threshold = int(f.readline())

    # read the machine tree
    for machineID in range(2,N + 1 ):
        line = f.readline()
        child_id, parent_id, operation_type = line.split()
        
        # Convert IDs to integers
        child_id = int(child_id)
        parent_id = int(parent_id)

        machine_tree[child_id] = {'parent': parent_id, 'operation': operation_type, 'children': []}
        if parent_id in machine_tree:
            machine_tree[parent_id]['children'].append(child_id)
        else:
            machine_tree[parent_id] = {'parent': None, 'operation': None, 'children': [child_id]}
    # add machine 1 to the tree
    
    # read the products list till the end of file
    for line in f:
        products.append(line.strip('\n'))
    #close the file
    f.close()

# Swap n processes as machines 
inter_comm = MPI.COMM_SELF.Spawn('python',
                           args=['machine.py'],
                           maxprocs=N)

# Send the input data to the machines
common_values = wear_factors_values + [N, C, threshold]
# send wear factors(5) , N , C +, threshold
common_values = np.array(common_values , dtype='i')
inter_comm.Bcast(common_values, root=MPI.ROOT)

# send the machine tree to each machine each machine id is rank + 1
for machine_id in range(1, N + 1):
    # send the machine tree
    inter_comm.send(machine_tree[machine_id], dest=machine_id - 1)

# send the products to the machines
for machine_id in range(2, N + 1):
    
    if not machine_tree[machine_id]['children']:
        # send the product
        inter_comm.send(products.pop(0), dest=machine_id - 1, tag=1001)
cycle = 1
logs = []
with open(output_file, 'w') as file:
    # Truncate the file to the current position (0 in this case)
    file.close()

while C > 0:
    final_product = inter_comm.recv(source=0, tag=0)

    
    # receive the logs from the machines
    for machine_id in range(1, N + 1):
        probe = False
        probe = inter_comm.iprobe(source=machine_id -1, tag=1002)

        if probe:
            # Message is available, determine its size
            
            data = inter_comm.recv(source=machine_id - 1, tag=1002)

            logs.append(data)

    with open(output_file, 'a') as f:
     
        f.write(f"{final_product}\n")
        f.close()
    C -= 1
    cycle += 1

logs = sorted(logs, key=lambda log: int(log.split('-')[0]))
with open(output_file, 'a') as f:
    for log in logs:
        f.write(log + '\n')
        
    f.close()

inter_comm.Disconnect()


    

        





