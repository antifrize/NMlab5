__author__ = 'Antifrize'

import os
from configparser import ConfigParser


class TaskLoader:
    mathFs = ['sin','cos','exp','pi']

    @staticmethod
    def addMath(string,mathFs):
        for f in mathFs:
            pass
            # string = string.replace(f,'math.'+f)
        return string

    @staticmethod
    def init():
        TaskLoader.tasks = []
        cp = ConfigParser()
        cp.optionxform = str
        for file in os.listdir("tasks"):
            cp.read_file(open("tasks/"+file))
            items = {}
            for (key, value) in cp.items("task"):
                newValue = TaskLoader.addMath(value,TaskLoader.mathFs)
                items[key]=newValue
            TaskLoader.tasks.append(items)

    @staticmethod
    def getTask(n):
        return TaskLoader.tasks[n-1]


TaskLoader().init()
print TaskLoader.getTask(0)