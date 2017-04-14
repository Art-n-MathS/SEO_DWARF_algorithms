#!/usr/bin/python

# This class contains object based information extracted from the images
# for example it could contain a vector defining the location of a dark spot
class Object:

   # ctor to assign values
   def __init__(self, x=0.0, y=0.0):
      self.x=float(x)
      self.y=float(y)

   # debug print function to print all the values of this object
   def __str__(self):
      return 'This is an object class. For now it has two indicative number [%f,%f]' % (self.x, self.y) 
