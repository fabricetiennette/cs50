import sys

def cc(k, plaintext):
    print("ciphertext: ", end="")
    for i in range(0, textlength):
        
        if plaintext[i].isupper():
            int_char = ((((ord(plaintext[i])) - 65) + k) % 26) + 65
            char = chr(int_char)
            print("%c"% (char), end="")
            
        elif plaintext[i].islower():
            int_char = ((((ord(plaintext[i]) - 97) + k) % 26) + 97)
            char = chr(int_char)
            print("%c"% (char), end="")
            
        else:
            print("%c"% (plaintext[i]), end="")

    print("")
    
if len(sys.argv) > 1:
    k = int(str(sys.argv[1]))
    if k >= 0:
        plaintext = input("plaintext: ")
        textlength = len(plaintext)
        cc(k, plaintext)
    else:
        print("Try again using an integer as key")
else:
    print("usage: python caesar.py k")    