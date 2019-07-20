public class TenThousandOnePrime {
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
    public static long primeLocator(long primeInstance) {                        
        long counter = 1;
        long primeNum = 0;
        
        for(long i = 2; counter <= primeInstance; i++) {                
            if(isPrime(i)) {
                primeNum = i;
                counter++; 
            }          
        }
        return primeNum;                                                              
    }
    public static void main(String[] args) {
        System.out.println(primeLocator(10001));       
    }
}