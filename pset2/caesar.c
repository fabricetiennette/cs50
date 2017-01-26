#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
 
 int a = 0;
 int k = 0;
 int b = 0;
 
    if (argc != 2)
    {
     printf("usage: ./caesar k\n");
     return 1;
    }
    
    for(int i = 0, n = strlen(argv[1]); i < n; i++)
    {
     
     a = (int) argv[1][i] - '0';
     
     k = k * 10 + a;
    }

    string plaintext;
    
    printf("plaintext: ");
    plaintext = get_string();
    
    printf("ciphertext: ");
    
   for(int i = 0, n = strlen(plaintext); i < n; i++)
   {
        b = (int) plaintext[i];
        if(b >= 65 && b <= 90)
        {
            int p = (int) plaintext[i] - 65;
            int c =(p + k) % 26;
            int j = c + 65;
            printf("%c", (char) j);
        }
        else if(b >= 97 && b <= 122)
        {
            int p = (int) plaintext[i] - 97;
            int c = (p + k) % 26;
            int j = c + 97;
            printf("%c", (char) j);
        }
        else
        {
         printf("%c", b);
        }
   }
   printf("\n");
}  