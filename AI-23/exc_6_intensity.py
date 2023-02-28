def ultrasound(i):  # standard
	return (get_ultrasound()[i] + get_ultrasound()[i] + get_ultrasound()[i])/3

# surprisingly enough, considering exc 6.1 and 6.2 instructions,
# intensity would be directly proportional to the power of the car
# in other words, you can DIRECTLY get the power FROM finding intensity

# obviously there's the issue of "exceeding power range"
# where the raw power exceeds 100
# so you MUST reduce the intensity value first (i.e. by dividing)

set(500, 60, 180)
while ultrasound(2) > 30:
	i = get_intensity()[0] / 2.5
	go(i,i,0.1)
