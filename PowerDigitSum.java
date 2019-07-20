import java.math.BigInteger;

public class PowerDigitSum {   
    public static long sumCalculator (int num) {                        
        BigInteger n = new BigInteger("2");        
        BigInteger powerSum = n.pow(num);
        String digits = powerSum.toString();
        int sum = 0;

        for(int i = 0; i < digits.length(); i++) {
            sum += Integer.parseInt(digits.charAt(i) + ""); 
        }
        return sum;
    }
    public static void main(String[] args) {                    
        System.out.println(sumCalculator(1000));        
    }
}