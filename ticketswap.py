import sys
import fileinput
import os
from math import *

num_of_passenger = 0;
last = -1;
first = -1;
passengers = []
mini = 0.0;
a = []

class passenger():
    def __init__(self,name="",start = 0, end = 0):
        self.name = name
        self.start = start
        self.end = end

    def get_payment(self):
        station = self.end - self.start
        total = 0.0
        init_charge = 1.0
        if(station >= 10):
            total = 5.5
        else:
            for i in range(station):
                total += (init_charge -0.1*i)
        return total
    
def count_discount(length):
    total = 0.0
    init_charge = 1.0
    if(length >= 10):
        total = 5.5
    else:
        for i in range(length):
            total += (init_charge -0.1*i)
    return total

def reset_first():
    global a,first
    for i in range(len(a)):
        if(a[i] != 0):
            first = i
            break
    
    
def get_total(passengers):
    total = 0.0
    global num_of_passenger
    for i in range(num_of_passenger):
        total += passengers[i].get_payment()
    return total
        
    
def read_file(inputfile):
    try:
        file = open(inputfile,"r")
    except IOError:
        raise RuntimeError("File does not exit")
        exit()

    #create passenger object array
    global passengers

    # record first station and last station
    global first
    global last
    
    i = 0
    for line in file:
        passengers.append(passenger())
        passengers[i].name = line[line.find('(')+1:line.find(',')]
        passengers[i].start = int(line[line.find(',')+1:line.rfind(',')])
        passengers[i].end = int(line[line.rfind(',')+1:line.find(')')])

        if(passengers[i].start<first or first == -1):
            first = passengers[i].start
        if(passengers[i].end > last or last == -1):
            last = passengers[i].end          
        i+=1
    file.close()
    global num_of_passenger
    num_of_passenger = i

def find_min():
    global num_of_passenger, mini,passengers,a
    if(num_of_passenger <= 1):
        if(num_of_passenger == 1):
            mini = passengers[0].get_payment()
    else:       
        for i in range(last):
            a.append(0)
        #assign value to array
        for i in range(num_of_passenger):
            for j in range(passengers[i].start,passengers[i].end):
                a[j] +=1
        find_min1()
        
def find_min1():
    global a,mini,first
    length = 0
    if(not check_arr(a)):
        for i in range(first,len(a)):
            if(a[i]>0):
                length +=1
                a[i] -=1
            else:
                reset_first()
                break
        mini += count_discount(length)
        find_min1()
    

# check array if items are all 0's
def check_arr(a):
    for i in range(len(a)):
        if(a[i] != 0):
            return False
    return True

def main():
    argv = sys.argv
    inputFile = argv[1]
    read_file(inputFile)
    total = get_total(passengers)
    find_min()
    loss = total - mini
    print("loss("+str(loss)+")")
main()

    
