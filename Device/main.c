#include <stdio.h>
#include <stdint.h>

#include "math.h"

#define VERSION (10)

int main()
{
   printf("Hello!\r\n");
   printf("Version: %d\r\n", VERSION);

   const uint16_t a = 15;
   const uint16_t b = 16;
   const uint16_t c = 17;

   uint16_t sum = math_sum(a, b);
   printf("Sum = %d\r\n", sum);

   uint16_t mul = math_mul(sum, c);
   printf("Mul = %d\r\n", mul);

   printf("Bye!\r\n");

   return 0;
}
