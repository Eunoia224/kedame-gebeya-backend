import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
import random
import time
import math
# t = time.time()
# t_ms = int(t*1000)
# random_num = (random.randint(1, 2147483647))
# new_id = (t_ms*random_num)
# new_id = (str(new_id) + uuid.uuid4().hex + str(new_id))
# print(new_id)

t = time.time()
t_ms = int(t*1000)
y = datetime.now()
newtime = y.strftime("%f")
newtime = int(newtime)

random_num = (random.randint(1, 2147483647))
random_div = random.randint(1, 1555555555)
new_id = (math.floor(t_ms * newtime / 2147483647))
print(new_id)