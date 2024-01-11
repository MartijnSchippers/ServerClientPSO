import subprocess
from world_generation.createWorldParallel import WorldGenerator
print("running webots")
p_id = 4
wg = WorldGenerator(fill_ratio = 0.48, instance_id=4)
wg.createWorld()
# subprocess.run("c:/Program Files/Webots/msys64/mingw64/bin/webots.exe --mode=fast --no-rendering C:/Users/marti/OneDrive/Documenten/IEM/IP/project/demo/worlds/main.wbt")#, cwd="c:/Program Files/Webots/msys64/mingw64/bin")

print("done running")