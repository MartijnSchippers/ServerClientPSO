# How to use the server-client PSO method
![alt text](/demo/server-client/images/Server-Client%20illustration.png)

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
