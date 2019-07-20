public class LargestPrimeFactor {
    public static long primeFactor(long num) {        
        long largestPrime = -1;
        
        while(num % 2 == 0) {
            largestPrime = 2;
            num /= 2;
        }        
        for(int i = 3; i <= Math.sqrt(num); i+=2) {
            while(num % i == 0) {
                largestPrime = i;
                num /= i;  
            }
        }
        if(num > 2) {
            largestPrime = num;                   
        }
        return largestPrime;
    }

    public static void main(String[] args) {
        System.out.println(primeFactor(600851475143l));        
    }
}