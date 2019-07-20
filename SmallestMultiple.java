public class SmallestMultiple {

    public static long factorial (int n) {
        long fact = 1;
        for(int i = 1; i <= n; i++) {
            fact *= i;
        }
        return fact;
    }
    
    public static long smallestMulitiple (int num) {
        long multiple = 0;
        long maxNum = factorial(num);
        int counter = 0;

        for(int i = num; i <= maxNum; i+=num) {
            for(int j = 1; j <= num; j++) {
                if(i % j == 0) {
                    counter++;
                } else if(i % j != 0) {
                    counter = 0;
                    break;
                }                                                 
            }
            if(counter == num) {
                multiple = i;
                break;
            }
        }
        return multiple;
    }

    public static void main(String[] args) {
        System.out.println(smallestMulitiple(20)); 
    }
}