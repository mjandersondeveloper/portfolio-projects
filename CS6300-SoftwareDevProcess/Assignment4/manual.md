## Assignment 4: Android Development Manual

Hello world! This is my SDP Encryptor Android application for CS-6300.

How to Use:
1.) There are three required fields that need to be filled in before clicking the **Encipher** button.
    - **Missive:** The message that is being encoded. This needs to include at least one letter before execution.
    - **Parameter A:** The first encryption parameter. This should be a co-prime number to 26 (1, 3, 5, 7, 9, 11, 15, 													17, 19, 21, 23, or 25).
		- **Parameter B:** The second encryption parameter. This should be a number between 1 and 26 (1 <= number < 26)
2.) After all inputs are entered, click **Encipher**
3.) The encrypted result will appear under **Encrypted Missive** at the bottom

**Notes**
1.) If any of the three fields are invalid the following errors (below) will appear on the right hand side of the invalid input
	and the previous output (if any) will be cleared:
		- **Missive:** Invalid Missive
		- **Parameter A:** Invalid Parameter A
		- **Parameter B:** Invalid Parameter B
2.) In order to cipher the missive input, each letter in the alphabet was assigned a numeric value (a = 0, b = 1,...z = 25).The
	message is put in an Affine Cipher (*E(x) = (ax + b) % 26*: where *a* and *b* are the values of **Parameter A** and **Parameter B** respectively. The result of that formula gets translated back into the associated letter in the list. 
			- Example: Missive: "C", Parameter A: 5, Parameter B: 3 -> (2 * 5 + 3) % 26 = 13 -> "13" corresponds to "N", which will be 
								 displayed as the output.
3.) If the original character in the missive input is lowercase, the resulting character in the output will be uppercase, 					and vice-versa.
4.) If one of the input character is non-alphabetic, it will not go through the cipher formula and will just be reflected in 			the output unchanged.
