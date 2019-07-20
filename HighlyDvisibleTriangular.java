public class HighlyDvisibleTriangular {  
    
    public static int termNumber (int num) {
        int term = 0;
        for(int i = 0; i <= num; i++) {
            term += i;
        }
        return term;
    }
    
    
    public static int divisorCalculator (int divisorLimit) {                                
        int divisors = 0;
        int term = 0;
        int counter = 0;

        while(divisors <= divisorLimit) {                                        
            divisors = 0;
            counter++;
            term = termNumber(counter);

            for(int i = 1; i <= Math.sqrt(term); i++) {
                if(term % i == 0) {
                    divisors++;
                }
            }
            divisors *= 2;               
        }
        return term;
    }
    public static void main(String[] args) {
        System.out.println(divisorCalculator(500));    
    }
}