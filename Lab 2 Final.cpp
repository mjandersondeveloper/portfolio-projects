// Lab 2 Final.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

//Constant Hash Table Size
const int tableSize = 7;

using namespace std;

//This stores the keys and key values in hash table
//Also creates the navigation functionality
struct HashObject {
	int k;
	int element;

	HashObject* forward;
	HashObject* backward;
};


//This class creates the intial hash table and holds the math, insert, and search hash functions
class HashArea {
public:
	HashObject** HashTable, **top;

	//HashArea Class Constructed
	HashArea() {
		HashTable = new HashObject *[tableSize];
		top = new HashObject *[tableSize];
		for (int i = 0; i < tableSize; i++) {
			HashTable[i] = NULL;
			top[i] = NULL;
		}
	}
	//HashArea Class Destroyed
	~HashArea() {
		delete[] HashTable;
	}

	//Hash Math Function: h = k mod 7
	int HashMath(int k) {
		return k % tableSize;
	}

	//Hash Insert Function: Inserts the random key values in the hash table
	void HashInsert(int value) {
		int hVal = HashMath(value);
		HashObject* input = HashTable[hVal];

		//If there are no exisiting values in a specific key(hVal)
		if (input == NULL) {
			
			input = new HashObject;
			input->element = value;
			input->k = hVal;
			input->forward = NULL;
			input->backward = NULL;
			HashTable[hVal] = input;
			top[hVal] = input;
		}
		else {
			//If there are existing values in a specific key
			while (input != NULL)
				input = input->forward;
			
			input = new HashObject;
			input->element = value;
			input->k = hVal;
			input->forward = NULL;
			input->backward = top[hVal];
			top[hVal]->forward = input;
			input = top[hVal];
		}
	}

	//Hash Search Function: Searches to if if there are random key values between 0-10
	void HashSearch(int k) {
		int hVal = k;
		HashObject* input = HashTable[hVal];

		//If both key values are not between 0-10, then the input will equal NULL and reset back into the HashSearch for-loop and move on to the next key
		while (input != NULL) {
			//This checks if each key values in the specifc key is bewteen 0-10
			if (input->element <= 10) {
				//If a key value between 0-10 is found, this message prints, and ends the program
				cout << "A random key value between 0 and 10 was found in the hash table! Congrats!" << endl;
				cout << "Random Key Value Found: " << input->element << endl;
				exit(0);
			}
			//If the key value is not bewteen 0-10, then this will point to the second values in the specific key
			input = input->forward;
		}

	}

};

	int main() {
		//Call to the HashArea class
		HashArea h;

		//int k = 0;
		int x = 0;

		//This function resets the random number list for the RandomKey function on compile time
		//Without this, the same list of random number each compile time
		srand(time(NULL));

		//HashInsert for-loop inserts 100 random key values into the hash table
		for (int i = 0; i < 100; i++) {
			//Intializes the random key values
			int RandomKey = (rand() % 100) + 1;
			h.HashInsert(RandomKey);
		}

		//HashSearch for-loop searches the random key values within each key until a key value between 0-10 is found
		for (int j = 0; j < 7; j++) {
			h.HashSearch(x);
			x++;
		}

		//If no key value is found between 0-10, this message prints
		cout << "A random key value between 0 and 10 was NOT found in the hash table, better luck next time!" << endl;
		return 0;
}
