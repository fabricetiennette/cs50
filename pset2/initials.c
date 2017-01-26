#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    string n ;
    
         n = get_string();
      
            printf("%c", toupper(n[0]));
    
    for(int l = 1, s = strlen(n) ; l < s ; l++)
    {
         if (n[l] == ' ' )
         {
            printf("%c",toupper(n[l+1]));
         }     
    }
     printf("\n");
}