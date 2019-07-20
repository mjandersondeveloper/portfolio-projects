public class CollatzSequence {   
    public static boolean isEven(long num) {                        
        if(num % 2 == 0) {
            return true;
        }             
        return false;
    }
    public static boolean isOdd(long num) {                        
        if(num % 2 != 0) {
            return true;
        }             
        return false;
    }
    public static void main(String[] args) {
        long counter = 1;
        long chain = 0;
        long beginChain = 0;
        for(long i = 2; i < 1000000; i++) {
            long seq = i;
            while (seq != 1) {
                if(isEven(seq)) {
                    seq /= 2;
                    counter++;                
                } else if(isOdd(seq)) {
                    seq = (3 * seq) + 1;
                    counter++;                 
                }
            }
            if(counter > chain){
                chain = counter;
                beginChain = i;
            }
            counter = 1;
        }                     
        System.out.println(beginChain);        
    }
}