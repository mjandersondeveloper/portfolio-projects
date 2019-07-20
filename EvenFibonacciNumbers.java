public class EvenFibonacciNumbers {
    public static int input(int limit) {
        int f1 = 1;
        int f2 = 2;
        int sum = 0;
        int fn;

        while (f1 <= limit){
            fn = f1;
            f1 = f2;
            f2 += fn;
            if(fn % 2 == 0){
                sum += fn;
            }
        }
        return sum;        
    }
    public static void main(String[] args) {
        System.out.println(input(4000000));
    }
}