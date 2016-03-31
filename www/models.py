#!/urs/bin/env python3
# _*_ coding:utf-8 _*_

'models for user,blog,comment.'

import time,uuid
from orm import Model,StingField,BooleanField,TextField

def next_id():
    return '%015d%s000'%(int(time.time()*1000),uuid.uuid4().hex)


