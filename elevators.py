import sys
import fileinput
import os
from math import *

num_of_elevator = 0;
top = 0;
elevators = []
mini = 0;


class elevator():
    def __init__(self,lower=0,upper=0,timer=0):
        self.lower = lower
        self.upper = upper
        self.location = lower
        self.timer = timer
    #get time 
    def get_time_on_lower(self):
        l = self.upper - self.lower
        if( (self.timer % l) == 0):                 # case on the lower or upper 
            if( ((self.timer/l) %2) == 0):          # case on the lower
                time = 0
            else:                                   # case on the upper
                time = l
        else:                                       # case on the processing
            if((floor(self.timer/l)%2) ==0 ):       #case going up
                time = 2*l - self.timer%l
            else:                                   #case going down
                time = l - self.timer%l
                
        return time
    
    def get_time_on_upper(self):
        l = self.upper - self.lower
        if( (self.timer % l) == 0):                 # case on the lower or upper 
            if( ((self.timer/l) %2) == 0):          # case on the lower
                time = l
            else:                                   # case on the upper
                time = 0
        else:                                       # case on the processing
            if((floor(self.timer/l)%2) ==0 ):       #case going up
                time = l - self.timer%l
            else:                                   #case going down
                time = 2*l - self.timer%l
                
        return time

    def get_length(self):
        return (self.upper - self.lower)
        

def check_arr(i,a):
    if(a[i] == 0):
        return False
    else:
        return True
    
def find_min():
    global elevators
    global mini
    global top
    time = 0

    # assign default arry to record used elevator
    a = []
    for i in range(num_of_elevator):
        a.append(1);
        
    # check if lower floor in base floor 0
    for i in range(num_of_elevator):
        if(elevators[i].lower == 0):
            
            if(elevators[i].upper == top):
                mini = top
            else:
                time = elevators[i].upper
                a[i]=0
                find_min1(i,time,a)
                a[i] = 1

# function find next valid elevators from upper floor
def find_min1(i,time,a):
    global elevators
    global mini
    global top
    tmp = time

    for j in range(num_of_elevator):

        #reset time
        time = tmp
        
        # if pre elevoto upper == to next lower and not used 
        if( elevators[i].upper == elevators[j].lower and check_arr(j,a) ):

            #update record arr
            a[j] = 0
            
            # update time value
            elevators[j].timer = time
            time += (elevators[j].get_time_on_lower()+elevators[j].get_length())
            if(elevators[j].upper == top):
                if( time < mini or mini == 0 ):
                    mini = time
            else:
                find_min1(j,time,a)  # go to loop upper floor match
            a[j] = 1

                
        # if pre elevoto upper == to next upper and not used 
        if( elevators[i].upper == elevators[j].upper and check_arr(j,a) ):
            #update record arr
            a[j] = 0
            
            # update time value
            elevators[j].timer = time
            time += (elevators[j].get_time_on_upper()+elevators[j].get_length())

            # go to loop lower floor match
            find_min2(j,time,a) 

            a[j] =1


# function find next valid elevators from lower floor
def find_min2(i,time,a):
    global elevators
    global mini
    global top
    
    tmp = time
    
    for j in range(num_of_elevator):
        
        #reset time
        time = tmp
        
        # if pre elector lower == to next lower and not used 
        if( elevators[i].lower == elevators[j].lower and check_arr(j,a) ):

            #update record arr
            a[j] = 0
            
            # update time value
            elevators[j].timer = time
            time += (elevators[j].get_time_on_lower()+elevators[j].get_length())
            if(elevators[j].upper == top):
                if( time < mini or mini == 0 ):
                    mini = time
            else:
                find_min1(j,time,a)  # go to loop upper floor match
            a[j] =1

                
        # if pre elevoto lower == to next upper and not used 
        if( elevators[i].lower == elevators[j].upper and check_arr(j,a) ):
            #update record arr
            a[j] = 0
            
            # update time value
            elevators[j].timer = time
            time += (elevators[j].get_time_on_upper()+elevators[j].get_length())

            # go to loop lower floor match
            find_min2(j,time,a)
            a[j] =1
        
def read_file(inputfile):
    # check if file exists
    try:
        file = open(inputfile,"r")
    except IOError:
        raise RuntimeError("File does not exit")
        exit()

    # get top floor
    str1 = file.readline()
    global top
    top = int(str1[str1.find('(')+1:str1.find(')')])

    #get num of elevator
    str1= file.readline()
    global num_of_elevator
    num_of_elevator = int(str1[str1.find('(')+1:str1.find(')')])

    #create elavator object array
    global elevators
    for i in range(num_of_elevator):
        str1 = file.readline()
        elevators.append(elevator())
        elevators[i].lower = int(str1[str1.find(',')+1:str1.rfind(',')])
        elevators[i].upper = int(str1[str1.rfind(',')+1:str1.find(')')])
    file.close()



    
def main():
    argv = sys.argv
    inputFile = argv[1]
    read_file(inputFile)
    find_min()
    print("time("+str(mini)+")")
       
main()
