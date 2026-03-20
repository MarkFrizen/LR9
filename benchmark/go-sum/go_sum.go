package main

/*
#include <stdint.h>

uint64_t sum_of_squares_c(uint64_t n);
*/
import "C"

//export sum_of_squares_c
func sum_of_squares_c(n C.uint64_t) C.uint64_t {
	var sum C.uint64_t = 0
	for i := C.uint64_t(1); i <= n; i++ {
		sum += i * i
	}
	return sum
}

func main() {}
