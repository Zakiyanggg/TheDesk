/* * TheDesk.c
 * This program is for ESE519 Final Project
 * Group 44 
 * The Desk
 * Author : Ziyi Yang, Keran Wang
 */ 


#define F_CPU 16000000UL
#include <avr/io.h>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <util/delay.h>
#define BAUD_RATE 9600
#define BAUD_PRESCALER (((F_CPU / (BAUD_RATE * 16UL))) - 1)
#include "uart.h"
#include <avr/interrupt.h>

int step_delay;
int last_step_time = 0;
int step_number = 0;
int number_of_steps;

int temp;
int temp1;
int count;
char String[25];

//function sets steps for stepper to run the sequence
//The sequence of control signals for 4 control wires is as follows:
/*
* Step C0 C1 C2 C3
*    1  1  0  1  0
*    2  0  1  1  0
*    3  0  1  0  1
*    4  1  0  0  1
*/
void stepMotorForward(int step)
{
	switch(step){
		case 0:
		PORTB |= (1<<PORTB1);//pb1 high
		PORTB &= ~(1<<PORTB2);//pb2 low
		PORTB |= (1<<PORTB3);//pb3 high
		PORTB &= ~(1<<PORTB4);//pb4 low
		case 1:
		PORTB &= ~(1<<PORTB1);//pb1 low
		PORTB |= (1<<PORTB2);//pb2 high
		PORTB |= (1<<PORTB3);//pb3 high
		PORTB &= ~(1<<PORTB4);//pb4 low
		case 2:
		PORTB &= ~(1<<PORTB1);//pb1 low
		PORTB |= (1<<PORTB2);//pb2 high
		PORTB &= ~(1<<PORTB3);//pb3 low
		PORTB |= (1<<PORTB4);//pb4 high
		case 3:
		PORTB |= (1<<PORTB1);//pb1 high
		PORTB &= ~(1<<PORTB2);//pb2 low
		PORTB &= ~(1<<PORTB3);//pb3 low
		PORTB |= (1<<PORTB4);//pb4 high
	}
}

void stepMotorBackward(int step)
{
	switch(step){
		case 0:
		PORTB |= (1<<PORTB1);//pb1 high
		PORTB &= ~(1<<PORTB2);//pb2 low
		PORTB |= (1<<PORTB3);//pb3 high
		PORTB &= ~(1<<PORTB4);//pb4 low
		case 1:
		PORTB |= (1<<PORTB1);//pb1 high
		PORTB &= ~(1<<PORTB2);//pb2 low
		PORTB &= ~(1<<PORTB3);//pb3 low
		PORTB |= (1<<PORTB4);//pb4 high
		case 2:
		PORTB &= ~(1<<PORTB1);//pb1 low
		PORTB |= (1<<PORTB2);//pb2 high
		PORTB &= ~(1<<PORTB3);//pb3 low
		PORTB |= (1<<PORTB4);//pb4 high
		case 3:
		PORTB &= ~(1<<PORTB1);//pb1 low
		PORTB |= (1<<PORTB2);//pb2 high
		PORTB |= (1<<PORTB3);//pb3 high
		PORTB &= ~(1<<PORTB4);//pb4 low
	}
}
void stepForward(int step)
{
	int step_left = step;
	while(step_left >0){
		time_t now = time(0);
		if(now -last_step_time >= step_delay){
			last_step_time = now;
			step_number++;
			if(step_number == number_of_steps){
				step_number = 0;
			}
			stepMotorForward(step_number%4);
		}		
	}
}

void stepBackward(int step)
{
	int step_left = step;
	while(step_left >0){
		time_t now = time(0);
		if(now -last_step_time >= step_delay){
			last_step_time = now;
			step_number++;
			if(step_number == number_of_steps){
				step_number = 0;
			}
			stepMotorBackward(step_number%4);
		}
	}
}
void Initialize()
{
	cli();
	//set 4 output pins to drive 4pin stepper motor
	DDRB |= (1 << DDB1);//PB1 as output
	DDRB |= (1 << DDB2);//PB2 as output
	DDRB |= (1 << DDB3);//PB3 as output
	DDRB |= (1 << DDB4);//PB4 as output
	DDRD &= ~(1<< DDD5);//PD5 as input
	DDRD &= ~(1<< DDD7);//PD7 as input
	int forward;
	int backward;
	int motorstep;
	
	sei();
	UART_init(BAUD_PRESCALER);
}
int main(void)
{
	Initialize();
    while (1) 
    {
		if(PIND & (1<<PIND5)){
		sprintf(String,"PD5 HIGH,forward");
		UART_putstring(String);	
		temp = 0 ;
    }
	}
	while(temp ==0){
	count++;
		if(PIND & ~(1<<PIND5)){
			sprintf(String,count);
			UART_putstring(String);
			count = count/4;
			stepMotorForward(count);
			stepForward(count);
			temp = 1;
		}
	}
	if(PIND & (1<<PIND7)){
		sprintf(String,"PD7 HIGH,backward");
		UART_putstring(String);
		temp = 0;
	}
	while(temp ==0){
		count++;
		if(PIND & ~(1<<PIND7)){
			sprintf(String,count);
			UART_putstring(String);
			count = count/4;
			stepMotorBackward(count);
			stepBackward(count);
			temp = 1;
		}
	}
}


