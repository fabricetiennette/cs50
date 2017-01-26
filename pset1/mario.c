#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h, s, r, l;
    
    do 
    {
        printf("Height: ");
        h = get_int();
    }
    while(h < 0 || h > 23);
    
    
    for(s = 1 ; s <= h ; s++)
    {
    for(r = 1 ; r <= h-s ; r++)
        {
            printf(" ");
        }    
    for(l = 1 ; l <= s+1 ; l++)
        {      
          printf("#");
        }
     printf("\n");
    }
return 0;
}