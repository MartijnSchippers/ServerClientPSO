import subprocess
import os
from world_generation.createWorldParallel import WorldGenerator
print("running webots")
p_id = 4
wg = WorldGenerator(fill_ratio = 0.48, instance_id=1)
wg.createWorld()
# subprocess.run("c:/Program Files/Webots/msys64/mingw64/bin/webots.exe --mode=fast --no-rendering C:/Users/marti/OneDrive/Documenten/IEM/IP/project/demo/worlds/main.wbt")#, cwd="c:/Program Files/Webots/msys64/mingw64/bin")

demo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../")

command = ["webots", "--mode=fast", "--no-rendering", demo_path + "worlds/bayes_pso_0_" + str(0) + ".wbt"]

# Use subprocess.run with the list of strings
subprocess.run(command)
print("done running")