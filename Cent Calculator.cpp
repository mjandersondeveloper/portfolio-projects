#include <iostream>

using namespace std;

int main()
{
    int cents;
    int quarters = 0;
    int nickels = 0;
    int dimes = 0;
    int pennies = 0;
    
    cout << "Please enter the total amount of cents:"<<endl;
    cin >> cents;
    
    int result = cents;
    
    while(cents) {
        
        if(cents >= 25) {
            cents -= 25; //cents = cents - 25
            quarters++; //quarter counter
        }
        else if(cents >= 10) {
            cents -= 10; //cents = cents - 10
            dimes++; //dime counter
        }
        else if(cents >= 5) {
            cents -= 5; //cents = cents - 5
            nickels++; //nickel counter
        }
        else {
            cents -= 1; //cents = cents - 1
            pennies++; //penny counter
        }   
    } 
    
    cout << " " << endl;
    cout << "The minimum amount of coins to use for the cent total of " << result << " are:" << endl;
    cout << " " << endl;
    
    cout << quarters << " quarter(s)" << endl;
    cout << dimes << " dime(s)" << endl;
    cout << nickels << " nickel(s)" << endl;
    cout << pennies << " penny(ies)" << endl;
    
    return 0;
}