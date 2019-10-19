#ifndef UNIT_TESTS_H
#define UNIT_TESTS_H

#define UNIT_TEST_OK (0)
#define UNIT_TEST_FAIL (1)
#define UNIT_TEST_FATAL (2)

int unit_tests_init(void);
int unit_tests_run(void);

#endif /* UNIT_TESTS_H */
