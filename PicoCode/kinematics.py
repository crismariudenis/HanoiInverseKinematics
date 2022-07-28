import math
class Kinematics:
    def __init__(self):
        self.l1 = 2.5
        self.l2 = 15
        self.l3 = 15
        
    def calc(self, y, z):
        
        z -= self.l1
        
        if(y == 0):
            y = 0.00001
        if(z == 0):
            z = 0.00001
        
        q3 = -math.acos((y * y + z * z - self.l2 * self.l2 - self.l3 * self.l3) / (2 * self.l2 * self.l3))
        q2 = math.atan(z / y) - math.atan((self.l3 * math.sin(q3)) / (self.l2 + self.l3 * math.cos(q3)))
        q4 = q3 + q2
        
        return [ q2, q3, q4 ]
#         except:
#             return []
#         
#         return []
            
            
            