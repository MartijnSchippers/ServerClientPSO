# File: createEnvironment.py python script       
# Date: 29-10-2023     
# Description: this script creates an environment for the DTPA lab setup by 
#               -generating the map with black and white tiles as a .txt file
#               -generating the image that corresponds to the map as a .png file
#               Given that there are 5x5 tiles  
# Author: Martijn Schippers

# fill_ratio = 0.52

from PIL import Image, ImageDraw 
import numpy as np
import random

# Create and possibly save the map that represents the black and white tiles 
# in a .txt file. 

class Arena:
    nr_tiles = 25 #hardcoded value and intended 
    
    def __init__(self, fill_ratio, tiles = None):
        # self.fill_array = np.array([[0,1,1,1,1],
        #                             [0,1,1,1,1],
        #                             [0,1,1,1,1],
        #                             [0,1,1,1,1],
        #                             [0,1,1,1,1]])
        self.fill_ratio = fill_ratio
        if tiles is None:
            self.map = self.__create()
        else:
            self.map = self.__create_map_from_2D(tiles)

    # Create the map as tuples (x, y) in a numpy array
    def __create(self):
        # empty map 
        map = np.zeros((int(self.nr_tiles*self.fill_ratio),2), dtype=int)

        # create random unique numbers between 0 and 100, and use them as 
        # indexes for colored tiles
        random_numbers =  random.sample(range(0, self.nr_tiles), int(self.nr_tiles * self.fill_ratio) )
        
        # update the map with the random generated numbers
        for idx, number in enumerate(random_numbers):
            map[idx][0] = int(number / 5) # x coordinate
            map[idx][1] = int(number % 5) # y coordinate
        return map

    def __create_map_from_2D(self, tiles):
        map_list = []
        for x, row in enumerate(tiles):
            for y, value in enumerate(row):
                if value == 1:
                    map_list.append((y, x))
        return  np.array(map_list)
    
    # save the map (to a .txt file) 
    def save(self, filename = "../controllers/bayesV2/world.txt"):
        print(self.map)
        return np.savetxt(filename, self.map.astype(int), delimiter=',', fmt='%d')


class ImageGenerator:
    pic_dim = 500
    tile_size = pic_dim / 5

    def __init__(self, map: np.ndarray):
        self.map = map
        self.img = Image.new('1', (self.pic_dim, self.pic_dim))
        self.draw = ImageDraw.Draw(self.img)
        self.__generate()

    def __generate(self):
        # fill the image with white tiles for each tile in the map
        for tile in self.map:
            x = tile[0] * self.tile_size
            y = tile[1] * self.tile_size
            self.draw.rectangle((x, y, x + self.tile_size,y + self.tile_size), fill=1)
        return
    
    def save(self, filename = "world.png"):
        self.img.save(filename)
        return
    
# # Convert custom maps via:
# tiles = np.array( [[1,0,1,1,0],
#                     [0,1,0,0,1],
#                     [0,1,1,0,0],
#                     [1,0,0,1,1],
#                     [0,1,1,0,0]])
# tiles = np.flip(tiles,axis =0).transpose()
# arena = Arena(0.52, tiles)

# # arena = Arena(0.52)
# arena.save()
# img = ImageGenerator(arena.map)
# img.save()