# Hard coding, or naive solution, is a brute force straightforward way of coding
# This is a last ditch attempt which is inefficient but may get you SOME credit.
# It's best to know what you're doing, and how to do it.

"Section B Q1"
def avg_dist(i, count = 3): 
    # i -> the sensor parameter
    # count -> defaulted to 3, but higher numbers allow more precision
    total = 0
    for k in range(count):
        total += get_ultrasound()[i]
    return total/count


"Section B Q3"
def move(distance, power = 50, t = 0.05):
    start = get_ultrasound()[3]
    temp = start
    while abs(start - temp) < distance:
        go(power, power, t)
        temp = get_ultrasound()[3]
    return abs(start - temp) # returns the deviated distance


"Section B Question 2"
def right_IF(start, end):
    while angle() < end - 15:
        go(100, -100, 1/24)
    go(-100, 100, 1/24) # counteract inertia
    while angle() < end and angle() > start: #considers infinite loops
        go(5, -5, 1/24)
        go(0, 0, 1/24)  # counteract inertia
        
def right(a = 90):
    "Note the difference between a pivot, and a turn"
    start = angle()
    end = start + a     # calculate ending angle
    if end < 360:
        right_IF(start, end)
    else: # turns beyond a full revolution
        zero = False
        prev = angle()
        while not zero: # turning until car passes 0 degrees
            go(100, -100, 1/24)
            go(0, 0, 1/24) # inertia consideration
            if angle() < prev: # only occurs as angle changes from 350+ to 0+
                zero = True
            prev = angle()
        end = end - 360 # new objective angle
        if angle() < end: # ensure that objective angle has not been overlapped
            right(end - angle()) 
            # call function within itself to turn (recursive functions)
        elif angle() > end: 
   # slowly adjust car backwards to return to objective angle
            while angle() > end and angle() < 350:
                go(-5, 5, 1/24)
                go(0, 0, 1/24) # inertia consideration
                
            
            
"Section A Question 1"
set(500,266,90)
while get_color()[0][1] < 30:   # enter green grass
    go(100, 100, 0.05)
while get_intensity()[0] > 30:  # leaving green grass
    go(100, 100, 0.05)
go(-1,-1,1/24) # counter inertia 

right() # reuse B2 function

"Section A Question 2"
for right in range(100, -1, -20):
    go(100, right, 0.5)

"Section A Question 3"
move(500, 100) # reuse B3

"Section A Question 4"
total = avg_dist(0) + avg_dist(1) + avg_dist(2) # reuse B1
print("Frontal distance sum:", total)
if total < 300:
    go(-100, 100, 1)
elif 450 > total > 300: 
    go(-100, 100, 1)
    go(100, -100, 1)
else:
    go(100, -100, 1)
