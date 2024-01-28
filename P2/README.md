# Command to run our code is given below: 
mpiexec -n 1 python control_room.py input.txt output.txt

# IMPORTANT: If the Operating System(like MacOS) doesn’t allow the create processes more than the number of processors in the computer, you should add “—oversubscribe” flag and command will be:
mpiexec -n 1 –-oversubscribe python control_room.py input.txt output.txt


# Libraries that needs to be installed:
python >= 3.9.0
mpi4py == 3.1.4
openmpi == 4.1.1
numpy == 1.23.2
