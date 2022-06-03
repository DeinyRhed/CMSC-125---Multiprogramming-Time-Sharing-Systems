"""
CMSC 125 - Machine Problem 1: Multiprogramming Time Sharing Systems
Programmed by: Dianne M. Mondido

"""

from math import floor  # For progress bar
import random

class User:
    def __init__(self, index):
        self.__index = index

    def __repr__(self):
        return f'User {str(self.__index)}'

class Task:
    def __init__(self, user, time):
        self.__requester = user
        self.__maxTime = time
        self.__remainingTime = 0
        self.__status = 'waiting'

    def getTaskStatus(self):
        return self.__status

    def getRemainingTime(self):
        return self.__remainingTime

    def getMaxTime(self):
        return self.__maxTime

    def activate(self):
        self.__status = 'active'

    def update(self):
        if (self.__status == 'active'):
            self.__remainingTime += 1
            if (self.__remainingTime >= self.__maxTime):
                self.__status = 'done'
        else:
            print(f'ERROR: {self} is not yet active.')

    def __repr__(self):
        # Progress Bar Value
        taskStat = f'{str(self.__remainingTime)}/{str(self.__maxTime)}'
        statusStat = '{:<7}'.format(self.__status.upper())

        # Progress Bar Status
        rawTaskNumbers = floor((self.__remainingTime/self.__maxTime) * 10)
        progressBar = '█'*rawTaskNumbers + '░'*(10-rawTaskNumbers)

        return f'{str(self.__requester)}: {statusStat}, {taskStat} {progressBar}'

class Resource:
    def __init__(self, index):
        self.__index = index
        self.__taskQueue = []
        self.__currentTask= None
        self.__doneTask = None
        self.__status = 'offline'

    def getResourceStatus(self):
        return self.__status

    def addTask(self, user, time):
        self.__taskQueue.append(Task(user, time))

    def start(self):
        if self.__taskQueue:
            self.__status = 'busy'
            self.nextTask()
        else:
            self.__status = 'free'
    
    def nextTask(self):
        self.__doneTask = self.__currentTask
        if self.__taskQueue:
            self.__currentTask = self.__taskQueue.pop(0)
            self.__currentTask.activate()
        else:
            self.__currentTask = None
            self.__status = 'free'

    def update(self):
        self.__doneTask = None
        if self.__currentTask:
            if self.__currentTask.getTaskStatus() != 'done':
                self.__currentTask.update()
                if self.__currentTask.getTaskStatus() == 'done':
                    self.nextTask()
        print(self.status())

    def status(self):
        resourceStatus = f'======= | Resource {str(self.__index)} | =======\n'
        waitTime = 0

        if self.__status == 'busy':
            resourceStatus += f'\t{self.__doneTask}\n' if self.__doneTask else ''
            resourceStatus += f'\t{self.__currentTask}\n'
            waitTime += self.__currentTask.getMaxTime() - self.__currentTask.getRemainingTime()

            for task in self.__taskQueue:
                resourceStatus += f'\t{task}, {waitTime}s for task to start\n'
                waitTime += task.getMaxTime()
        else:
            if self.__doneTask:
                resourceStatus += f'\t{self.__doneTask}\n'
            else:
                resourceStatus += "\tNo Processes in Queue.\n"
        return resourceStatus

    def __repr__(self) -> str:
        return f'Resource {str(self.__index)}'


def ifBusy(resourceList):
    for resource in resourceList:
        if resource.getResourceStatus() != 'free':
            return True
    return False
    

def main():
    userList = []
    resourceList = []
    timer = 0
    
    # Generate User list
    for i in range(random.randint(1, 30)):
        userList.append(User(i+1))

    # Generate Resource List
    for i in range(random.randint(1, 30)):
        resourceList.append(Resource(i+1))

    # Generate each User a random needed resource with random time
    for user in userList:
        chosenResource = random.choice(resourceList)
        chosenResource.addTask(user, random.randint(1,30))

    # Initializing Resources    
    print('-'*100)
    print(f'USERS: {userList}')
    print(f'RESOURCES: {resourceList}\n')
    print(f'======= | Time: {timer} ms | =======\n')

    for resource in resourceList:
        resource.start()
        print(resource.status())

    print('-'*50 + '\n')

    key = input("")
    timer += 1

    # Start of Processing
    while ifBusy(resourceList):
        print('-'*100)
        print(f'USERS: {userList}')
        print(f'RESOURCES: {resourceList}')
        print(f'\n======= | Time: {timer} ms | =======\n')

        for resource in resourceList:
            resource.update()

        print('-'*100 + '\n')
        
        key = input("")
        timer += 1

main()