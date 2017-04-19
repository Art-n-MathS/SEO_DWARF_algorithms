#!/usr/bin/python

# This class contains an addition to the metadata:: i.e. turbitity (mean, min and maz)
class Metadata_addition:

   # ctor to assign values
   def __init__(self, mean_v=0.0, min_v=0.0, max_v=0.0):
      self.mean_v=float(mean_v)
      self.min_v=float(min_v)
      self.max_v=float(max_v)

   # debug print function to print all the values of this object
   def __str__(self):
      return 'This addition contains the following information \n mean: %f\n min: %f\n max: %f\n' % ( self.mean_v, self.min_v, self.max_v)

   # method that modifies the min value of this metadata addition
   def setMin(self,m_v):
      self.min_v=m_v

   # method that modifies the max value of this metadata addition
   def setMax(self,m_v):
      self.max_v=m_v

   # method that modifies the mean value of this metadata addition
   def setMean(self,m_v):
      self.mean_v=m_v

   # method that returns the min value
   def getMin(self):
      return self.min_v

   # method that returns the min value
   def getMax(self):
      return self.max_v

   # method that returns the min value
   def getMean(self):
      return self.mean_v
   
