#include "stdafx.h"
#include <iostream>
#include <string>

using namespace std;

void tripleValues(int a, int &b) {  	//"a" = Pass-by-Value "b" = Pass-by-Reference
a = a*3;
b = b*3;
}

int main() {
  int a = 3;
  int b = 12;
  cout << "Before the tripleValues() method is called: \na = "<<a<<"\nb = "<<b<<endl;
  
  tripleValues(a,b);
  cout << "After the tripleValues() method is called: \na = "<<a<<"\nb = "<<b<<endl;
  return 0;
}