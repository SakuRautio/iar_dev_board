#include <stdio.h>

#include "unit_tests.h"
#include "math.h"

static int testSum(void);
static int testMultiply(void);

typedef struct {
   char* name;
   int (*func)(void);
} unit_tests_t;

#define UNIT_TESTS_COUNT (2)
static unit_tests_t unitTests[UNIT_TESTS_COUNT] = {
   {"Sum", testSum},
   {"Multiply", testMultiply}
};

static int somethingToInit = 0;

int unit_tests_init(void)
{
   int ret = UNIT_TEST_OK;
   
   somethingToInit = 1;
   
   return ret;
}

int unit_tests_run(void)
{
   int ret = UNIT_TEST_OK;
   
   int testsRan = 0;
   int testsSuccessful = 0;
   int testsFailed = 0;
   
   printf("Unit Tests: Start\r\n");
   
   int i = 0;
   for (i = 0; i < UNIT_TESTS_COUNT; i++)
   {
      printf("Unit Test Run[%d]: %s\r\n", i+1, unitTests[i].name);
      int testResult = unitTests[i].func();
      testsRan++;
      if (testResult == UNIT_TEST_FATAL)
      {
         printf("Unit Test Fail[%d]: %s\r\n", i+1, unitTests[i].name);
         testsFailed++;
         break;
      }
      if (testResult != UNIT_TEST_OK)
      {
         printf("Unit Test Fail[%d]: %s\r\n", i+1, unitTests[i].name);
         testsFailed++;
      }
      else
      {
         printf("Unit Test Succesful[%d]: %s\r\n", i+1, unitTests[i].name);
         testsSuccessful++;
      }
   }
   
   printf("Unit Tests: End. Result: Success:%d, Failed:%d, Total:%d\r\n", testsSuccessful, testsFailed, testsRan);
   
   return ret;
}

static int testSum(void)
{
   int a = 0;
   
   int sumResult = math_sum(a, somethingToInit);
   if (sumResult <= 0)
   {
      return UNIT_TEST_FAIL;
   }
   
   sumResult = math_sum(a, 2);
   if (sumResult != 2)
   {
      return UNIT_TEST_FAIL;
   }
   
   sumResult = math_sum(2, 2);
   if (sumResult != 4)
   {
      return UNIT_TEST_FAIL;
   }
   
   return UNIT_TEST_OK;
}

static int testMultiply(void)
{
   int a = 0;
   
   int mulResult = math_mul(a, somethingToInit);
   if (mulResult != 0)
   {
      return UNIT_TEST_FAIL;
   }
   
   mulResult = math_mul(1, -1);
   if (mulResult != (-1))
   {
      return UNIT_TEST_FAIL;
   }
   
   mulResult = math_mul(3, 2);
   if (mulResult != 4)
   {
      return UNIT_TEST_FAIL;
   }
   
   return UNIT_TEST_OK;
}
