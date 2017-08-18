#include "stdafx.h"
#include <iostream>
#include <string>
#include <stdio.h>

using namespace std;

int main() {

	enum group {

		groupA, groupB, groupC, groupD
	};

	enum group g1, g2;

	enum city {

		Akron, Toledo, Dayton, Cleveland
	};

	enum city c1, c2;

	g1 = groupB;
	g2 = groupC;
	c1 = Toledo;
	c2 = Dayton;

	cout << "Intial value of g1 " << g1 << "\n";
	cout << "Intial value of g2 " << g2 << "\n";

	(g1 = (group)3);
	scanf_s("%d", &g1);

	printf("Changed value of g1 after assigning value 3 to it %d \n", g1);

	g1 = g2;

	cout << "Changed value of g1 after assigning value of g2 " << g2 << "\n";

	(c1 = (city)g2);

	cout << "Changed value of c1 after assigning value of g2 " << c1 << "\n";

	c1 = static_cast<city>(static_cast<int>(c1) + 1);

	cout << "Changed value of c1 after incrementing value of c1 " << c1 << "\n";

}
