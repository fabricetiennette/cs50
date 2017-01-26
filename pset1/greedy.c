#include <cs50.h>
#include <stdio.h>
#include <math.h>


#define QUARTER 25;
#define DIME 10;
#define NICKEL 5;

int main(void)
{
    float owed = 0;
    int quarter = 0;
    int dime = 0;
    int nickel = 0;
    int moneyLeft = 0;
    int finalAmount = 0;
    int x = 0;
   
   
   do
   { 
        printf("O hai! How much change is owed?\n");
        owed = GetFloat();
   }
   while(owed <= 0);
   
   x = (int)round(owed*100);
   
   quarter = x / QUARTER;
   moneyLeft =  x % QUARTER;
   
   dime =  moneyLeft / DIME;
   moneyLeft = moneyLeft % DIME;
   
   nickel = moneyLeft / NICKEL;
   moneyLeft =  moneyLeft % NICKEL;
   
   
   finalAmount = quarter + dime + nickel + moneyLeft;
   {
       printf("%d\n", finalAmount);
   }
   
    
    return 0;
    
}