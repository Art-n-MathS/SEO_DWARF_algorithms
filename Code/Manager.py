#!/usr/bin/python

# This class manages all the inputs (satellite images) and outputs (producs)
class Metadata_addition:

   # ctor to assign values
   def __init__(self, phenomenon,mean=0.0, min_v=0.0, max_v=0.0):
      self.phenomenon=phenomenon
      self.mean=float(mean)
      self.min_v=float(min_v)
      self.max_v=float(max_v)

   # debug print function to print all the values of this object
   def __str__(self):
      return 'This addition contains information about  %s\n mean: %f\n min: %f\n max: %f\n' % (self.phenomenon, self.mean, self.min_v, self.max_v)

   # method that modifies the min value of this metadata addition
   def setMin(self,m_v):
      self.min_v=m_v

   # method that modifies the max value of this metadata addition
   def setMax(self,m_v):
      self.max_v=m_v

   # method that modifies the mean value of this metadata addition
   def setMean(self,m_v):
      self.mean=m_v
