while True:
    height = int(input("Height: "))
    if ((height >= 0) and (height <= 23)):
        break
    else:
        print("Invalid input :( Try again")
        continue


if height > 0:
    for s in range(0, height):
        for r in range((height -1), s, -1):
            print(" ", end="")

        for l in range(-2, s):
            print("#", end="")
        print("")
