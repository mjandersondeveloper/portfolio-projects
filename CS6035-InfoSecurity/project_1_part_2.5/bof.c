#include <stdio.h>
#include <unistd.h>

int unsafe(){
  char buffer[420];
  int characters_read;
  printf("Feed Me A Stray String:\n");  
  characters_read = read(0, buffer, 1000);
  printf("You shouldn't see this if attack worked: %s", buffer);
  return 0;
}

void main(){
  unsafe();
}

