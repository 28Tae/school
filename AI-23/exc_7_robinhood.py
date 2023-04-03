def ultrasound(i):
    return (get_ultrasound()[i] + get_ultrasound()[i] + get_ultrasound()[i])/3

u_init = ultrasound(2)       # ultrasound
i_init = get_intensity()[0]  # intensity

u_li = [u_init]
i_li = [i_init]

for i in range(10):
    while u_init - ultrasound(2) < 50:
        go(50, 50, 0.1)
    u_init = ultrasound(2)  # refresh after every 50km dist travelled
    go(0, 0, 1.5)   # counteract inertia
    u_li.append(u_init)
    i_li.append(i_init)

print('ultrasound list', u_li)
print('intensity list', i_li)
