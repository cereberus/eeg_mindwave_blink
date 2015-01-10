/*
Fast Artificial Neural Network Library (fann)

Script for recognizing blinking artifacts. 
Features of raw EEGS signal were used to train the network.

Now new data is being read from file. 
By default 3 features are taken to input[0], input[1], input[2]
Then output is calculated.

Output:
 * Not blinking:    0
 * Blinking:        1
*/

#include <stdio.h>
#include <stdlib.h>     /* strtof */

int main()
{
   float num=123412341234.123456789; 
   char output[50];
   snprintf(output,50,"%f",num);
   printf("%s",output);

  return 0;
}
