#ifndef ADG725_H
#define ADG725_H

#include <stdint.h>

//DRDY pin
#define DRDY														12//18						

#define CSA 6
#define CSB 5

extern int i;
extern int k;

void ADG725_spi_init(void);
void ADG725_spi_uninit(void);
void ADG725_spi_clear(void);
void set_mux(uint8_t reg);

void loop_init(void);
void move_to_next_16_16_square(void (*)(void));
void move_to_next_16_16_trapezoid(void (*)(void));

inline int get_index(void) {
  return 16*i+k;
}


#endif  // ADG725_H
