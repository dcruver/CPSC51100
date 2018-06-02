# -*- coding: utf-8 -*-
# Name: Don Cruver, Bill O'Keefe
# Date: May 15, 2018
# Course: CPSC51100 - Statistical Programming, Lewis University
# Term: Summer 2018
# Assignment Name: Programming Assignment 2 – k-Means Clustering

def average(l):
    """Accepts a numeric list and returns the average of the values in that list.
       The data structure used to store the groups is a list where each element
       of the list is a list of two values. The first inner-list value is the 
       mean of the second inner-list value which is a list of the group members.

       example:
          [[4, [2, 4, 6]], [6, [3, 6, 9]], [10, [12, 8, 10, 12, 8]]...]
       """
    return sum(l)/float(len(l))
     
def distance(p, q):
    """Accepts values and returns the distance between them.
       The distance is always a positive integer. """
    return abs(p - q)
    
def initialize(values, k):
    """Accepts a numeric list and the number of groups to be created.
       Initializes the module based on the supplied values."""
    if k < len(values):
        global groups
        groups = [ [x, [x]] for x in values[0:k] ]
        groups.sort()
        
        for value in values[k:len(values)]:
            group = find_best_group(value, groups)
            group[1].append(value)
             
def find_best_group(p, l):
    """Given a value and a list, this function does a binary search to
       locate and return the group with the nearest mean value."""
    if len(l) == 1:
        return l[0];
        
    midpoint = int((len(l)-1) / 2)
    d1 = distance(p, l[midpoint][0])
    d2 = distance(p, l[midpoint + 1][0])
    
    if d1 < d2:
        return find_best_group(p, l[0:midpoint + 1])

    return find_best_group(p, l[midpoint + 1:len(l)])
    
def recalculate_centroids():
    """Recalculates the mean for each group."""
    for group in groups:
        group[0] = average(group[1])           
    
def rebalance():
    """Iterates over the values in each inner-most list to find the
       group that's the closest fit. Returns a boolean indicating whether
       any points were moved between groups."""
       
    recalculate_centroids()    
    point_moved = False
    
    for group in groups:
        mean = group[0]
        values = group[1]
    
        for value in values:
            new_group = find_best_group(value, groups)
            
            if new_group[0] != mean:
                point_moved = True
                values.remove(value)
                new_group[1].append(value)
    
    return point_moved

def groups():
    """Returns the current state of the groups."""
    return groups

def converge(output_fn=None):
    """Calls 'rebalance()' repeatedly until convergence is reached. Optionally
       accepts a function that will be pasdsed the current state of 'groups' 
       on each iteration."""
    iteration_num = 0
    while (rebalance()):
        iteration_num += 1
        if output_fn:
            output_fn(iteration_num)

def output(iteration_num):
    """
    Prints a single iteration of the required CLI output.
    
    params:
        iteration_num: int, num of times rebalance executed
    """
    # print as shown in sample output
    print("Iteration %d" % iteration_num)
    clusters = groups
    
    for cluster in clusters:
        print("%d %s" % (cluster[0], cluster[1]))  
    # [print("%d %s" % (cluster[0], cluster[1])) for cluster in clusters]
    print("\n")

def write_results(out_file, input_file):
    """
    Writes all points and their associated cluster number to file.
    
    params:
        out_file: str, name of output file
        input_file: str, name of input file
    """    
    # create dict to store key=number, value=cluster_num
    # not sure if ideal, but can be done with one pass through of groups
    # and then cluster_num can be retrieved in constant time
    current_cluster = 0
    cluster_dict = {}
    for group in groups:
        for item in group[1]:
            cluster_dict[item] = current_cluster
        current_cluster += 1
    
    # need to grab numbers as originally ordered
    with open(input_file) as file:
        nums = [float(line.strip()) for line in file]
    
    with open(out_file, 'w+') as file:
        for number in nums:
            file.write("Point %s in cluster %d \n" % (number, cluster_dict[number]))

            
def main():
    """
    Retrieves input from user to start clustering.  Calls initialize, 
    converge, write_results.
    """
    
    input_file = raw_input("Enter the name of the input file: ")
    output_file = raw_input("Enter the name of the output file: ")
    k = int(raw_input("Enter the number of clusters: "))
    print("\n")
    
    with open(input_file) as file:
        nums = [float(line.strip()) for line in file]
        
    initialize(nums, k)            # creates k groups
    converge(output)               # shuffles until convergence
    write_results(output_file, input_file)     # creates required out file
    

if __name__ == "__main__":
    print("CPSC-51100, Summer 2018")
    print("NAME: Don Cruver, Bill OKeefe")
    print( "PROGRAMMING ASSIGNMENT #2 \n")
    
    main()
