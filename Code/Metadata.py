#!/usr/bin/python

from Metadata_addition import *

# This class is responsible for managing all the object related information
# extracted from the images
# it contains multiple instances of the class Object
class Metadata:

   # ctor to assign values
   # metadata_file_str: is the directory and name of the original metadata file
   # metadata_out_file_str: the dir and name of the new metadata file
   # list_of_additions: are the additions to be added to the file
   def __init__(self, metadata_file_str="", metadata_out_file_str="", list_of_additions=[]):
      # a list of objects 
      self.metadata_file_str = metadata_file_str
      self.metadata_out_file_str = metadata_out_file_str
      self.list_of_additions=list_of_additions

   # debug print function to print all the values of this object
   def __str__(self):
      return 'Original metadata File: %s\nNew Metadata file: %s\nThere are %d additions' % (self.metadata_file_str,self.metadata_out_file_str, len(self.list_of_additions))


   def exportNewMetadata(self):
      print 'Exporting new metadata file have not been implemented yet'

  
      
