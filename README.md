# What is Particle Swarm Optimization
Particle Swarm Optimization (PSO) is a nature-inspired algorithm developed in the 1990s. It mimics the collective behavior of organisms like bird flocks to solve optimization problems. In PSO, a population of particles moves through a problem space, adjusting positions based on personal best and global best information. The algorithm is simple, easy to implement, and effective for various optimization tasks, making it popular in fields such as engineering design and data clustering (source: ChatGPT).

## This project divides computing power between clients
For this project, a mathematical problem that (could potentially be a computationally expensive operation), implements the PSO method by giving the command of a calculation, to a client. In other words, the server gets a request from a computer "I want to do a calculation", then the server responds with "OK, here is a set of problems to solve: {x = 2, y = 2}". THen, the client computes the answer by putting it into the equation and returns "4" (for example). 

# How to use the server-client PSO method
**Important: all functions related to Webots cannot be used** (they belong to another project). The RosenBrock function, however, is.

 ## Start up server
First, indicate the settings (number of runs, number of particles, etc.) in the file 'settings.json'. To start up the server, open the 'server' folder in a terminal, and run "flask run" (to be accessible from the device) or "flask run --host=0.0.0.0" (to be accessible from the local network). It will display information about the ip address and port it is on.

 ## Start up client 
Each client has to be started up separately. To start up the client, open the folder "client" in a terminal and type "python app.py IP-address port ID", where  IP-address is the IP address of the server, port is the port of the server (standard on 5000) and ID is a uinque integer number (start with 0). For future research, it is recommended to automate the process of deploying a number of clients at once, to save time and prevent errors due to numbers being not unique.  

To start up a client for calculating the Rosensenbrock example, follow the same instructies as for following the normal client, but then in the folder "client/rosenbrock".

 ## obtain results
To obtain the results of the PSO run, copy the "results.json" file into the folder "results". Rename the file if desired. Edit (if result file is renamed) and run the file 'get_best_fitness_val.py' to obtain the best fitness score. Run webots.py to see the results of the Webots run and run rosenbrock.py to see the results of a Rosenbrock test.

## flowcharts client and server (might be usefull for further extension)
![alt text](/demo/server-client/images/client%20klein.png)
![alt text](/demo/server-client/images/server%20klein.png)
