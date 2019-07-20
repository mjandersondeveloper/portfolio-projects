public class SummationOfPrimes {
    public static boolean isPrime(long num) {
        int counter = 0;
        long square = (long)Math.sqrt(num);

        for(long n = 1; n <= square; n++) {
            if(num % n == 0) {
                counter++;
            }
            if(counter > 1) {
                return false;
            }
        }
        return true;
    }    
    public static long primeSummation (long maxPrime) {                        
        long primeSum = 0;
        
        for(long i = 2; i < maxPrime; i++) {                
            if(isPrime(i)) {
                primeSum += i;
            }          
        }
        return primeSum;                                                              
    }
    public static void main(String[] args) {
        System.out.println(primeSummation(2000000));    
    }
}