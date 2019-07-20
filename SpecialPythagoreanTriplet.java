public class SpecialPythagoreanTriplet {

    public static int productABC(int num) {
        for(int a = 1; a <= num/3; a++) {
            for (int b = a + 1; b <= num/2; b++) {
                int c = num - a - b;

                if(Math.pow(a, 2) + Math.pow(b, 2) == Math.pow(c, 2)) {
                    return a * b * c;                
                }
            }
        }
        return 0;
    }
    
    public static void main(String[] args) {
        System.out.println(productABC(1000)); 
    }
}