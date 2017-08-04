#include <pthread.h>
#include <stdio.h>

int sum = 0;
float size;
float avg;

/* the thread */
void *runnerSumAvg(void *param); 

int main(int argc, char*argv[])
{

/* thread identifier and set of attributes */
pthread_t tid; 
pthread_attr_t attr; 

if (argc < 2) {

fprintf(stderr, "Usage: prog.c <integer vaulues> \n");
/*exit(1);*/
return -1;
}

/* Creates array for argv[], stores the values */
int nums[argc-1];
int i;
/* Displays the list of numbers entered*/
printf("\nNumbers added: ");

for(i = 1; i <= argc-1; i++) {

nums[i-1] = atoi(argv[i]);
size++;

printf("%d ",nums[i-1]);

}

/*Get the default attributes*/
pthread_attr_init(&attr);
/*Create the thread*/
pthread_create(&tid,&attr,runnerSumAvg,(void*)nums);
/*Wait for the thread to exit*/
pthread_join(tid,NULL);

printf("The sum of the value(s) is: %d.\n", sum);
printf("The average of the value(s) is: %.2f.\n\n",avg);

}

/*runnerSumAvg function*/
void *runnerSumAvg(void *param){

int *nums = (int*)param;
int i;

for(i = 0; i < size; i++) {
sum = sum + nums[i];
}

avg = sum/size;

printf("\n");

pthread_exit(0);

}





