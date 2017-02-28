print("O hai! How much change is owed?")
while True:
    owed = float(input(""))
    if owed >= 0:
        break
    else:
        print("Invalid input :( Try again")
        continue

owed *= 100
cents = int(owed)
finalAmount= 0

while True:
    if cents >= 25:
        cents -= 25
        finalAmount += 1
    elif ((cents < 25) and (cents >= 10)):
        cents -= 10
        finalAmount += 1
    elif ((cents < 10) and (cents >= 5)):
        cents -= 5
        finalAmount += 1
    elif ((cents < 5) and (cents >= 1)):
        cents -= 1
        finalAmount += 1
    else:
        break

print("" + str(finalAmount))