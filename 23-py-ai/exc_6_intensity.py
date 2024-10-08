def ultrasound(i):  # standard
	return (get_ultrasound()[i] + get_ultrasound()[i] + get_ultrasound()[i])/3

# surprisingly enough, considering exc 6.1 and 6.2 instructions,
# intensity would be directly proportional to the power of the car
# basically, you can DIRECTLY get power FROM finding intensity

set(500, 60, 180)
while ultrasound(2) > 30:
	i = get_intensity()[0] / 2.5	# limit to acceptable range (max 100)
	go(i, i, 0.1)
