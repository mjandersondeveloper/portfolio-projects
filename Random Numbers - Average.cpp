#include <iostream>
#include <cstdlib> 

using namespace std;

int main() {

int numberGenerator[5];
float avg;
float sum = 0.0;
string answer;

srand((unsigned)time(0)); 

cout << "Numbers: ";
for(int j = 0; j < 5; j++) {
    
numberGenerator[j] = (rand() % 10 + 1);

if(j == 4) {
cout << numberGenerator[j] << endl;
    } else {
cout << numberGenerator[j] << " | ";
    }
 
sum += numberGenerator[j];

}
    avg = sum / 5;
    cout << "Total Average = "<< avg << endl;
    cout << " " << endl;

    cout << "Would you like to add a new value? Type 'yes' or 'no': ";
    getline (cin, answer);
    cout << " " << endl;
    
    if(answer == "yes" || answer == "Yes"){
        for(int j = 5; j >= 5; j--) {
            numberGenerator[j] = (rand() % 10 + 1);
            numberGenerator[j + 1] = numberGenerator[j];
            
            cout << "Number "<<numberGenerator[j] << " was added to the list!" << endl;
            sum += numberGenerator[j];
            
            avg = sum / 6;
            cout << "Your new Total Average = "<< avg << endl;
            return 0;
        }                 
    } 
    else if (answer == "no" || answer == "No"){
        cout << "Thank you for using the program!";
        return 0;
    } else {
        cout << "Invalid answer, the program will now exit.";
        return 0;
    }

}