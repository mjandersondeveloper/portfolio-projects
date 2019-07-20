public class LargestPalindrome {

    public static boolean isPalindrome(long product) {
        long potenPoli = product;
        long reverseProduct = 0;

        while(potenPoli != 0) {
            reverseProduct = reverseProduct * 10 + potenPoli % 10;
            potenPoli /= 10;
        }
        if(reverseProduct == product) {
            return true;
        } else {
            return false;
        }                    
    } 
   
    public static long largestPalindrome() {
        long palindrome = 0;

        for(int i = 100; i < 1000; i++) { 
            for(int j = i; j < 1000; j++ ) {
                if((isPalindrome(i * j)) && ((i * j) > palindrome)) {
                    palindrome = i * j;
                }
            }
        }
        return palindrome;
    }

    public static void main(String[] args) {
        System.out.println(largestPalindrome()); 
    }
}