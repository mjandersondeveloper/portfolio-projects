package edu.gatech.seclass;

/**
 * This is a Georgia Tech provided code example for use in assigned
 * private GT repositories. Students and other users of this template
 * code are advised not to share it with other students or to make it
 * available on publicly viewable websites including repositories such
 * as Github and Gitlab.  Such sharing may be investigated as a GT
 * honor code violation. Created for CS6300 Summer 2021.
 *
 * Template provided for the White-Box Testing Assignment. Follow the
 * assignment directions to either implement or provide comments for
 * the appropriate methods.
 */

public class ImperfectClass {

    public static void exampleMethod1(int a) {
        // ...
        int x = a / 0; // Example of instruction that makes the method
                       // fail with an ArithmeticException
        // ...
    }

    public static int exampleMethod2(int a, int b) {
        // ...
        return (a + b) / 0; // Example of instruction that makes the
                            // method fail with an ArithmeticException
    }

    public static void exampleMethod3() {
        // NOT POSSIBLE: This method cannot be implemented because
        // <REPLACE WITH REASON> (this is the example format for a
        // method that is not possible) ***/
    }

    public static int imperfectMethod1(boolean x) {
        int dividend = 0;
        if (x) {
            dividend += 1;
        }
        if(dividend > 0) {
            dividend = 1;
        }
        return 1 / dividend;
    }

    public static void imperfectMethod2() {
        // NOT POSSIBLE: This method cannot be implemented because 100% branch coverage implies 100% statement coverage.
        // Therefore, we cannot fulfill the second requirement (it is possible to create a
        // test suite that achieves 100% statement coverage and does reveal the fault), because
        // the first requirement needs us to do 100% branch coverage that does NOT reveal the fault.
    }

    public static void imperfectMethod3() {
        // NOT POSSIBLE: This method cannot be implemented because 100% branch coverage implies 100% statement coverage.
        // Therefore, we cannot fulfill the second requirement (it is possible to create a
        // test suite that achieves 100% statement coverage and does not reveal the fault), because
        // the first requirement needs us to do 100% branch coverage that DOES reveal the fault.
    }

    public static int imperfectMethod4(boolean x, boolean y) {
        int num1 = 1;
        int num2 = 1;
        if (x) {
            num1 *= 2;
        }
        if (y) {
            num2 += num1;
        } else {
            num2 *= 2;
        }
        return 1 / (num1 - num2);
    }

    public static String[] imperfectMethod5() {
        String[] a = new String[7];
        /*
				public static boolean providedImperfectMethod(boolean a, boolean b) {
  					int x = 24;
                    int y = 24;
                    if (a)
                        x = y;
                    else
                        x = -2*x;
                    if (b)
                        y = 0-x;
                    return ((100/(x-y))>= 0);
				}
        */
        //
        // Replace the "?" in column "output" with "T", "F", or "E":
        //
        //         | a | b |output|
        //         ================
        a[0] =  /* | T | T | <T, F, or E> (e.g., "T") */ "T";
        a[1] =  /* | T | F | <T, F, or E> (e.g., "T") */ "E";
        a[2] =  /* | F | T | <T, F, or E> (e.g., "T") */ "F";
        a[3] =  /* | F | F | <T, F, or E> (e.g., "T") */ "F";
        // ================
        //
        // Replace the "?" in the following sentences with "NEVER",
        // "SOMETIMES" or "ALWAYS":
        //
        a[4] = /* Test suites with 100% statement coverage */ "NEVER";
               /*reveal the fault in this method.*/
        a[5] = /* Test suites with 100% branch coverage */ "NEVER";
               /*reveal the fault in this method.*/
        a[6] =  /* Test suites with 100% path coverage */ "SOMETIMES";
                /*reveal the fault in this method.*/
        // ================
        return a;
    }
}

