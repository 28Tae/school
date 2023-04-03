"generally, these serve as geometric representations, and remain impractical in problem-solving."

def oval():
    for i in range(2):
        go(100,100,.6)
        go(100,0,2.65)
    
def tree_point_turn():
    go(50,50,1)
    go(98,0,1.35)
    go(50,50,1)
    go(-70,-70,2)
    go(33,33,1)
    go(98,0,1.35)
    go(50,50,1.2)

def infinity():
    go(100,5,5.5)
    go(5,100,5.5)

def star():
    for i in range(5):
        go(80,80,2)
        go(100,-100,1.06)
