#!/usr/bin/python

from Metadata_addition import *
from ObjectManager import *

# This class manages all the inputs (satellite images) and outputs (producs)
class Processed_Img:

   # ctor to assign values
   def __init__(self, obj_manager=ObjectManager(), medata_addition=Metadata_addition(), phenomenon=""):
      self.obj_manager=obj_manager
      self.metadata_addition=medata_addition
      self.phenomenon=phenomenon

   # debug print function to print all the values of this object
   def __str__(self):
      return 'This is the proceessed_img class'

   
   # method that run the algorithm
   def algorithm(self):
      print 'algorithm has not been implemented yet'

   
   # method that exports the processed img into a file
   def exportImg(self, filename):
      print 'exporting processed image into: '
      print filename
      print 'exportingImg function not implemented yet'


   def getMetadataAdditionStr(self):
      return  '   <gmd:%s>\n        <gmd:%s_max>\n            <gco:Decimal>%f</gco:Decimal>\n        </gmd:%s_max>\n        <gmd:%s_min>\n            <gco:Decimal>%f</gco:Decimal>\n        </gmd:%s_min>\n        <gmd:%s_mean>\n            <gco:Decimal>%f</gco:Decimal>\n        </gmd:%s_mean>\n    </gmd:%s>' % (self.phenomenon, self.phenomenon, self.metadata_addition.getMax(), self.phenomenon, self.phenomenon, self.metadata_addition.getMin(), self.phenomenon, self.phenomenon, self.metadata_addition.getMean(), self.phenomenon, self.phenomenon)
