#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
 
int main(int argc, string argv[])
{
    
    int k = 0;
    int aa = 0;
    int ee = 0;
    int cc = 0;
    
    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (isalpha(argv[1][i]))
            {
                ;
            }
            else
            {
                printf("Error 110 : alphabetical only.\n");
                return 1;
            }
        }
    }
    
  
    printf("plaintext: ");
    string plaintext = get_string();
    int n = strlen(plaintext);
    int amc[n];
    printf("ciphertext: ");
    
    do
    {
       
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            k = (int) argv[1][i];
            if (k >= 65 && k <= 90)
            {
                k = k - 65;
                amc[ee] = k;
            }
            else if (k >= 97 && k <= 122)
            {
                k = k - 97;
                amc[ee] = k;
            }
            ee++;
            aa++;
            if (aa == n)
            {
                break;
            }
        }
    }
    while (aa < n);
    
    
    for (int i = 0; i < n; i++)
    {
        int b = (int) plaintext[i];
        k = amc[cc];
        if (b >= 65 && b <= 90)
        {
            int p = (int) plaintext[i] - 65;
            int c = (p + k) % 26;
            int j = c + 65;
            printf("%c", (char) j);
            cc++;
        }
        else if (b >= 97 && b <= 122)
        {
            int p = (int) plaintext[i] - 97;
            int c = (p + k) % 26;
            int j = c + 97;
            printf("%c", (char) j);
            cc++;
        }
        else
        {
            printf("%c", b);
        }
    }
    
    printf("\n");
    
}
