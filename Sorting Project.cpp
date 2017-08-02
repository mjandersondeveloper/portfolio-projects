// Lab1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <string>
#include <ctime>

using namespace std;

// Calls the random array and all sorting methods
void RandomArray(int x[], int arrsize);
void insertionSort(int array[], int x);
void mergeSort(int array[], int left, int right);
void quickSort(int array[], int less, int great);
void countSort(int array[], int len);

int main()
{
	// Intialize arraySize and sorting method input
	int arraySize;
	string method;

	// Method Selection
	cout << "Which sorting method would you like to use?" << endl;
	cout << "I = Insertion" << endl;
	cout << "M = Merge" << endl;
	cout << "Q = Quick" << endl;
	cout << "C = Counting" << endl;
	cout << "Selection (I, M, Q, C): ";
	getline(cin, method);
	cout << endl;

	// Method Selection Error Handling 
	if (method != "I" && method != "M" && method != "Q" && method != "C") {
		cout << "Invalid method choice, please restart program." << endl;
		return 0;
	}

	// Array Size Selection 
	cout << "Enter the desired size of array (10, 100, 1,000, 10,000, 100,000): ";
	cin >> arraySize;
	cout << endl;

	// Array Size Selection Error Handling
	if (arraySize != 10 && arraySize != 100 && arraySize != 1000 && arraySize != 10000 && arraySize != 100000) {
		cout << "Invalid array size, please restart program." << endl;
		return 0;
	}

	// Constant Array Size
	int* array = new int[arraySize];
	RandomArray(array, arraySize);

	// Displays the first and last five elements of the RANDOM array
	cout << "The first five elements of RANDOM array are: ";
	for (int i = 0; i <= 4; i++) cout << array[i] << " ";
	cout << endl;

	cout << "The last five elements of RANDOM array are: ";
	for (int i = arraySize - 6; i <= arraySize - 1; i++) cout << array[i] << " ";
	cout << endl;
	cout << endl;

	// Begin Time
	clock_t beginTime = clock();
	if (method == "I") {
		insertionSort(array, arraySize);
	}
	else if (method == "M") {
		mergeSort(array, 0, arraySize - 1);
	}
	else if (method == "Q") {
		quickSort(array, 0, arraySize - 1);
	}
	else if (method == "C") {
		countSort(array, arraySize);
	}
	// End Time
	clock_t endTime = clock();
	clock_t timeTaken = endTime - beginTime;

	// Displays the first and last five elements of the SORTED array
	cout << "The first five elements of SORTED array are: ";
	for (int i = 0; i <= 4; i++) cout << array[i] << " ";
	cout << endl;

	cout << "The last five elements of SORTED array: ";
	for (int i = arraySize - 6; i <= arraySize - 1; i++) cout << array[i] << " ";
	cout << endl;
	cout << endl;

	// Displays the method name and run time
	if (method == "I"){
	cout << "Method used: Insertion Sort" << endl;
	}
	if (method == "M") {
		cout << "Method used: Merge Sort" << endl;
	}
	if (method == "Q") {
		cout << "Method used: Quick Sort" << endl;
	}
	if (method == "C") {
		cout << "Method used: Counting Sort" << endl;
	}
	cout << "Time taken: " << timeTaken << " ms" << endl;

	// Delete array to prevent a memory leak
	delete[] array;

	return 0;
}


// Random Array Generator
void RandomArray(int x[], int arrsize) {
	for (int i = 0; i < arrsize; i++)
		x[i] = rand() % 100;
}
/* ********************************************************************************************************* */

// InsertionSort Method
void insertionSort(int array[], int x)
{
	int y;
	int z;
	int key;

	// This sets up the insertion sort array. 
	for (y = 1; y < x; y++)
	{
		key = array[y];
		z = y - 1;

		/* This moves the array elements > key to the next postion 
		ahead of thier current one. */
		while (z >= 0 && array[z] > key)
		{
			array[z + 1] = array[z];
			z = z - 1;
		}
		array[z + 1] = key;
	}
}
/* ********************************************************************************************************* */

// MergeSort Method
void merge(int arrray[], int left, int mid, int right)
{
	int a;
	int b;
	int c;

	int n1 = mid - left + 1;
	int n2 = right - mid;

	/* Creates Temporary Arrays */
	int* L = new int[n1];
	int* R = new int[n2];
	

	/* Copies data to temporary arrays L[] and R[] */
	for (a = 0; a < n1; a++)
		L[a] = arrray[left + a];

	for (b = 0; b < n2; b++)
		R[b] = arrray[mid + 1 + b];

	/* Merges the temporary arrays back into original merge array[] */
	a = 0; // First subarray
	b = 0; // Second subarray
	c = left; // Merged subarray
	while (a < n1 && b < n2)
	{
		if (L[a] <= R[b])
		{
			arrray[c] = L[a];
			a++;
		}
		else
		{
			arrray[c] = R[b];
			b++;
		}
		c++;
	}

	/* Copies any remaining elements of L[] */
	while (a < n1)
	{
		arrray[c] = L[a];
		a++;
		c++;
	}

	/* Copies any remaining elements of R[] */
	while (b < n2)
	{
		arrray[c] = R[b];
		b++;
		c++;
	}
	/* Delete arrays to prevent a memory leak*/
	delete[] L;
	delete[] R;
}

void mergeSort(int array[], int left, int right)
{
	if (left < right)
	{
		int mid = left + (right - left) / 2;

		/* Sort the first(left) and second(right) halves */
		mergeSort(array, left, mid);
		mergeSort(array, mid + 1, right);

		merge(array, left, mid, right);
	}
}

/*  ********************************************************************************************************* */

//QuickSort Method
void swap(int* a, int* b)
{
	int t = *a;
	*a = *b;
	*b = t;
}

/* This function takes the last element in the array as a pivot point, 
and places it in the correct position in sorted array. 
Places all smaller elements < pivot to the left.
Places all greater elements > pivot to the right */
int partition(int array[], int less, int great)
{
	int pivot = array[great]; 
	int i = (less - 1);  // Smaller element

	for (int j = less; j <= great - 1; j++)
	{
		// When current element <= pivot
		if (array[j] <= pivot)
		{
			i++;    
			swap(&array[i], &array[j]);
		}
	}
	// Implements swap function
	swap(&array[i + 1], &array[great]);
	return (i + 1);
}

void quickSort(int array[], int less, int great)
{
	if (less < great)
	{
		// pindex represents the partitioning index of the partition array[]  
		int pindex = partition(array, less, great);

		// Separately sort elements before and after the partition
		quickSort(array, less, pindex - 1);
		quickSort(array, pindex + 1, great);
	}
}

/* ********************************************************************************************************* */

// CountingSort Method
void countSort(int array[], int len) {
	int l;
	int m;
	int n;
	int min;
	int max;
	int index = 0; // Intial index at 0
	 
	// Changes the array elements so it sorts them in order
	min = max = array[0];
	for (l = 1; l < len; l++) {
		min = (array[l] < min) ? array[l] : min;
		max = (array[l] > max) ? array[l] : max;
	}

	// Copies data into a new consistant array
	n = max - min + 1;
	int *A = new int[n];
	for (l = 0; l < n; l++) A[l] = 0;

	for (l = 0; l < len; l++) A[array[l] - min]++;
	for (l = min; l <= max; l++)
		for (m = 0; m < A[l - min]; m++) array[index++] = l;
}
