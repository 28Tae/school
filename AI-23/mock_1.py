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

"""
Due to complicated code and techniques utilised (recursive functions),
Section B Q2 will not have its answers put up.
"""
            
            
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
