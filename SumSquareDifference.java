public class SumSquareDifference {

    public static long naturalSum() {
        long sum = 0;
        for(int i = 1; i <= 100; i++) {
            double square = Math.pow(i, 2);
            sum += square;
        }
        return sum;
    }

    public static long squareSum() {
        long sum = 0;
        for(int i = 1; i <= 100; i++) {
            sum += i;
        }
        long square = (long) Math.pow(sum, 2);
        return square;
    }
    
    public static void main(String[] args) {
        System.out.println(squareSum() - naturalSum()); 
    }
}