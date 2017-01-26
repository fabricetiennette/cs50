/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // reject non-positive n
    if (n <= 0)
    {
        return false;
    }
    
    // determine the sizes of the bottom and top arrays
    int sizeLower = n / 2;
    int sizeUpper = n - sizeLower - 1;
    int middleValue = values[sizeLower];
    
    // if the value we're looking for is greater than the middle value, search the upper half of the array
    if (value > middleValue)
    {
        int newValues[sizeUpper];
        for (int i = 0; i < sizeUpper; i++)
        {
            // the second half of the values array begins at index sizeLower + 1
            newValues[i] = values[sizeLower + 1 + i];
        }
        return search(value, newValues, sizeUpper);
    }
    // if the value we're looking for is less than the middle value, search the lower half of the array
    else if (value < middleValue)
    {
        int newValues[sizeLower];
        for (int i = 0; i < sizeLower; i++)
        {
            newValues[i] = values[i];
        }
        return search(value, newValues, sizeLower);
    }
    // if it is neither (ie it is equal), then we have found the value and return true
    else
    {
        return true;
    }
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // implementation of bubble sort
    // there are n-1 pairs at the start
    for (int i = 0; i < n - 1; i++)
    {
        int swaps = 0;
        int pairsRemaining = n - 1 - i;
        // compare the j'th and j+1'th elements, rearrange if out of order
        for (int j = 0; j < pairsRemaining; j++)
        {
            if (values[j] > values[j + 1])
            {
                int temp = values[j + 1];
                values[j + 1] = values[j];
                values[j] = temp;
                swaps++;
            }
        }
        // if no swaps made, array is sorted
        if (swaps == 0)
        {
            return;
        }
    }
    return;
}