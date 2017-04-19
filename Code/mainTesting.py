#!/usr/bin/python

from ObjectManager import *
from Metadata import *
from Processed_Img import *

obj1 = Object()
obj1.x=2
obj2 = Object(3,4)
obj_m = ObjectManager([obj1,obj2])
print obj_m.getNoOfObjects()

print obj_m.__str__() 

print obj_m.getNoOfObjects()

obj_m.addObject(obj2) 
print obj_m.getNoOfObjects()
obj3 = obj_m.list_objects[0]
obj3.x = 45
obj3.__str__()

obj_m.list_objects[2].__str__()
obj_m.list_objects[1].__str__()
obj_m.newObject()
print obj_m.__str__() 


# testing metadata 
a = Metadata_addition( 0.0, 100.0, 200.0)
a.setMin(3) # not working
print a.__str__()

md = Metadata("in", "out", [a])
print md.__str__()
md.exportNewMetadata()


pm = Processed_Img(obj_m,a)
print pm.getMetadataAdditionStr()
pm.algorithm()
pm.exportImg("<outFileName>")


print "End of test script"

