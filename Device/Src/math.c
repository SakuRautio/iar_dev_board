#include <stdint.h>
#include "math.h"

uint16_t math_sum(uint16_t a, uint16_t b)
{
	uint16_t ret = (a + b) % UINT16_MAX;
	return ret;
}

uint16_t math_mul(uint16_t a, uint16_t b)
{
	uint16_t ret = (a * b) % UINT16_MAX;
	return ret;
}
