#include <stdint.h>

//DRDY pin
#define DRDY														12//18						


void ADG725_spi_init(void);
void ADG725_spi_uninit(void);
void ADG725_spi_clear(void);
void set_mux(uint8_t reg);
