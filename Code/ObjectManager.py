#!/usr/bin/python

from Object import *

# This class is responsible for managing all the object related information
# extracted from the images
# it contains multiple instances of the class Object
class ObjectManager:

   # ctor to assign values
   def __init__(self, list_objects=[]):
      # a list of objects 
      self.list_objects=list_objects

   # debug print function to print all the values of this object
   def __str__(self):
      return 'This is the object manager and it contains %d Objects ' % (self.getNoOfObjects()) 

   # methods that adds a given object (obj) to the list
   def addObject(self, obj):
      self.list_objects.append(obj)

   # methods that appends an new object at the end of the list
   def newObject(self):
      self.list_objects.append(Object())

   # method that returns the number of empty voxels
   def getNoOfObjects(self):
      return len(self.list_objects)
      
