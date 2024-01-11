
# Code heavily sourced from Johannes Boghaert's Masters Thesis:
# "Decentralized Collective Decision-Making Algorithms in Simulated Soft-Bodied Robot Swarms for 3D Surface Inspection in Space"

import math
import numpy as np
import random 
from world_generation.ArenaGenerator import Arena, ImageGenerator

class WorldGenerator():
    """
    Generates the .wbt folder based an input seed.

    Inputs:
        - particle_id
        - instance_id
        - robot_number
    Output:
        - A single .wbt file that is specific to the given seed.
    """

    def __init__(self, baseline=0, particle_id=0, instance_id=0, fill_ratio= 0.48, robot_number=4, path=None, dynamic_env=0, env_upper=0.55, env_lower=0.45):
        self.baseline = baseline
        self.particle_id = particle_id
        self.instance_id = instance_id
        self.fill_ratio = fill_ratio
        self.robot_number = robot_number
        self.path = path
        self.dynamic_env = dynamic_env
        self.env_upper = env_upper
        self.env_lower = env_lower

        #This will store the intial positions of the robots.
        self.initialX = [] 
        self.initialY = []

        self.orientation = [[1, 0, 0, -1.57], [0.577, 0.577, 0.577, -2.09], [0, 0.707106, 0.707107, 3.14159], [0.577, -0.577, -0.577, -2.09]]

    def checkCoord(self, x, y, array):
    #Iterates through 
      for coord in array:
        if ((coord[0] == x) & (coord[1] == y)):
            return 0
    
      return 1

    def createArena(self):
      #Do not use dynamic environment
      arena = Arena(self.fill_ratio)
      arena.save("../../project/demo/controllers/bayesV2/world.txt")
      img = ImageGenerator(arena.map)
      img.save("../../project/demo/world_generation/world.png")


    def createPos(self):
        for i in range(self.robot_number):
            while(1):
                x = random.uniform(0.05,0.95)
                y = random.uniform(0.05,0.95)
                if ((x not in self.initialX) and (y not in self.initialY)):
                    self.initialX.append(x)
                    self.initialY.append(y)
                    break

    def generateRot(self):
      # angle
      rot = str(round(random.uniform(0.0, 2*math.pi), 2))

      return rot

    def createTitle(self):
        title = "/bayes_pso_"
        title += str(self.particle_id)
        title += "_"
        title += str(self.instance_id)

        return title

    def createHeader(self, file):
        file.write("""#VRML_SIM R2021b utf8

# Author: Johannes Boghaert, Darren Chiu\n""")

    def createEnv(self, file):
        file.write(
        """
WorldInfo {
  CFM 0.1
  ERP 0.1
  basicTimeStep 8
  coordinateSystem "NUE"
  contactProperties [
    ContactProperties {
      material2 "WheelMat"
    }
  ]
}
Viewpoint {
  orientation -0.37410009861715926 -0.8017314106520007 -0.4661285888985836 2.0110979679680656
  position -0.4573118151367981 1.0734694097374347 0.21413139964469322
}
TexturedBackground {
}
TexturedBackgroundLight {
}
DEF surface Solid {
  translation 0.5 0 0.5
  rotation -1 0 0 1.5707953071795862
  children [
    Shape {
      appearance Appearance {
        texture ImageTexture {
          url [
              "../world_generation/world.png"
          ]
        }
      }
      geometry Plane {
      }
    }
  ]
  contactMaterial "Metal"
  boundingObject Plane {
  }
}
Wall {
  translation 0.5 0 -0.015
  size 1 0.05 0.025
}
Wall {
  translation 0.5 0 1.015
  name "wall(1)"
  size 1 0.05 0.025
}
Wall {
  translation 1.015 0 0.5
  rotation 0 1 0 1.5708
  name "wall(2)"
  size 1 0.05 0.025
}
Wall {
  translation -0.015 0 0.5
  rotation 0 1 0 1.5708
  name "wall(3)"
  size 1 0.05 0.025
}\n""")
    
    def createRobots(self, file):
        arg = "\"" + str(self.instance_id) + "\""
        arg2 = "\"" + str(self.dynamic_env) + "\""
        baselineArg = "\"" + str(self.baseline) + "\""
        file.write(
        """Robot {
  name "Bayes Bot Supervisor"
  controller "cpp_supervisor"
  controllerArgs [
    """ + arg + """
    """ + baselineArg + """
  ]
  supervisor TRUE
}\n""")

        for i in range(self.robot_number):
            index = np.random.randint(0, 4)
            rotationArg = str(self.orientation[index][0]) + " " + str(self.orientation[index][1]) + " " + str(self.orientation[index][2]) + " " + str(self.orientation[index][3]) 
            rov_number = str(i)
            file.write(
            """DEF r""" + rov_number + """ RovableV2 {
  translation """ + str(self.initialX[i]) + """ 0.023 """ + str(self.initialY[i]) + """
  rotation """ + rotationArg + """
  name "r""" + rov_number + """"
  controller "bayesV2"
  controllerArgs [
    """ + arg + """
    """ + arg2 + """
  ]
  supervisor TRUE
  customData "0.500000-"
  extensionSlot [
    Receiver {
    }
    Emitter {
    }
  ]
}\n""")

    def createWorld(self):
        random.seed(self.instance_id) 

        file = open(r"../../project/demo/worlds" + self.createTitle() + ".wbt", 'w')
        #file = open(r"/usr/local/efs/demo/worlds" + self.createTitle() + ".wbt", 'w')
        #file = open(r"/home/darren/Documents/ICRA_LAUNCH/Rovables_Bayesian_Inspection_Optimization/demo/worlds" + self.createTitle() + ".wbt", 'w')
        #Start with Header
        self.createHeader(file)

        #Create the bounding box 
        self.createEnv(file)

        self.createPos()

        #Creates the number of Rovables in a randomized position
        self.createRobots(file)

        print("World Written with Seed: " + str(self.instance_id))

        file.close()

        self.createArena()