#include <cs50.h>
#include <stdio.h>
#include <math.h>


int main(void)

{
    int bottles = 12;
    
    printf("minutes: ");
    int minutes = GetInt();
    
    printf("bottles: %i\n", (minutes * bottles));
  
    
    return 0;
}