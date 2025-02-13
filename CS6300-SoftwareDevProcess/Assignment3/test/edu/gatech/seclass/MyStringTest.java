package edu.gatech.seclass;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

/**
 * Junit test class created for use in Georgia Tech CS6300.
 *
 * You should implement your tests in this class.
 */

public class MyStringTest {

    private MyStringInterface mystring;

    @Before
    public void setUp() {
        mystring = new MyString();
    }

    @After
    public void tearDown() {
        mystring = null;
    }

    @Test
    // Description: Instructor-provided test 1
    public void testCountNumbersS1() {
        mystring.setString("My numbers are 11, 96, and thirteen");
        assertEquals(2, mystring.countNumbers());
    }

    @Test
    // Description: Current string is empty
    public void testCountNumbersS2() {
        mystring.setString("");
        assertEquals(0, mystring.countNumbers());
    }

    @Test
    // Description: Current string is a continuous number
    public void testCountNumbersS3() {
        mystring.setString("Here's a long sequence of numbers: 1234567890");
        assertEquals(1, mystring.countNumbers());
    }

    @Test(expected = NullPointerException.class)
    // Description: Current string is null
    public void testCountNumbersS4() {
        mystring.countNumbers();
        fail();
    }

    @Test
    // Description: Instructor-provided test 2
    public void testAddNumberS1() {
        mystring.setString("hello 90, bye 2");
        assertEquals("hello 92, bye 4", mystring.addNumber(2, false));
    }

    @Test
    // Description: Current string is a long sequence
    public void testAddNumberS2() {
        mystring.setString("Here's a long sequence of numbers: 987654");
        assertEquals("Here's a long sequence of numbers: 987664", mystring.addNumber(10, false));
    }

    @Test
    // Description: Current string is inverted
    public void testAddNumberS3() {
        mystring.setString("Reverse, reverse: 98735, reverse, reverse!");
        assertEquals("Reverse, reverse: 53789, reverse, reverse!", mystring.addNumber(0, true));
    }

    @Test
    // Description: Current string is inverted and negative
    public void testAddNumberS4() {
        mystring.setString("Reverse and negate: -987");
        assertEquals("Reverse and negate: -7801", mystring.addNumber(100, true));    }

    @Test(expected = NullPointerException.class)
    // Description: Current string is null with valid method arguments
    public void testAddNumberS5() {
        mystring.addNumber(0, false);
        fail();
    }

    @Test(expected = IllegalArgumentException.class)
    // Description: Current string is not null and n is negative
    public void testAddNumberS6() {
        mystring.setString("Even though the string is set, this will still fail");
        mystring.addNumber(-10, false);
        fail();
    }

    @Test
    // Description: Instructor-provided test 3
    public void testConvertDigitsToNamesInSubstringS1() {
        mystring.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
        mystring.convertDigitsToNamesInSubstring(17, 23);
        assertEquals("I'd b3tt3r put szerome donesix1ts in this 5tr1n6, right?", mystring.getString());
    }

    @Test
    // Description: Substring is replaced starting at position zero
    public void testConvertDigitsToNamesInSubstringS2() {
        mystring.setString("abcd3fgh1jklm8975");
        mystring.convertDigitsToNamesInSubstring(1, 14);
        assertEquals("abcdthreefghonejklmeight975", mystring.getString());
    }

    @Test
    // Description: Substring is mixed between normal/string digits
    public void testConvertDigitsToNamesInSubstringS3() {
        mystring.setString("1 2 3 four 5 6 seven 8");
        mystring.convertDigitsToNamesInSubstring(3, 14);
        assertEquals("1 two three four five six seven 8", mystring.getString());        }

    @Test(expected = IllegalArgumentException.class)
    // Description: Position less than 0 - throws an IllegalArgumentException
    public void testConvertDigitsToNamesInSubstringS4() {
        mystring.setString("This is be error 1");
        mystring.convertDigitsToNamesInSubstring(0, 9);
        fail();
    }

    @Test(expected = IllegalArgumentException.class)
    // Description: finalPosition is less than initialPosition - throws an IllegalArgumentException
    public void testConvertDigitsToNamesInSubstringS5() {
        mystring.setString("This is be error 2");
        mystring.convertDigitsToNamesInSubstring(5, 4);
        fail();
    }

    @Test(expected = MyIndexOutOfBoundsException.class)
    // Description: finalPosition is out of bounds - throws an IndexOutOfBoundsException
    public void testConvertDigitsToNamesInSubstringS6() {
        mystring.setString("This is be error 3");
        mystring.convertDigitsToNamesInSubstring(1, 20);
        fail();
    }
}

