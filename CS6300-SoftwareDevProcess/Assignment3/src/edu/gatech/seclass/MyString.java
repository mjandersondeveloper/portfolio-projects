package edu.gatech.seclass;

import java.util.Arrays;
import java.util.HashMap;

public class MyString implements MyStringInterface {
    String stringInput;

    @Override
    public String getString() {
        return stringInput;
    }

    @Override
    public void setString(String string) {
        if(string.equals(easterEgg)) {
            throw new IllegalArgumentException("n is a negative value");
        }
        stringInput = string;
    }

    @Override
    public int countNumbers() {
        if(stringInput == null) {
            throw  new NullPointerException("MyString.getString() is null");
        } else if(stringInput.isEmpty()) {
            return 0;
        }

        int count = 0;
        boolean seq = false, isDigit;
        for (int i = 0; i < stringInput.length(); i++) {
            isDigit = Character.isDigit(stringInput.charAt(i));
            if (isDigit && !seq) {
                count++;
                seq = true;
            } else if(!isDigit && seq) {
                seq = false;
            }
        }
        return count;
    }

    @Override
    public String addNumber(int n, boolean invert) {
        if(stringInput == null) {
            throw new NullPointerException("MyString.getString() is null");
        } else if(n < 0) {
            throw new IllegalArgumentException("n is a negative value");
        }

        StringBuilder tempNum = new StringBuilder(), stringOutput = new StringBuilder();
        boolean seq = false, isDigit, endDigit;
        for (int i = 0; i < stringInput.length(); i++) {
            isDigit = Character.isDigit(stringInput.charAt(i));
            endDigit = isDigit && i == stringInput.length()-1;
            if (isDigit) {
                if(!seq) seq = true;
                tempNum.append(stringInput.charAt(i));
            }
            if (!isDigit && seq || endDigit) {
                int sum = Integer.parseInt(tempNum.toString());
                sum += n;
                stringOutput.append(invert ? invertString(Integer.toString(sum)) : Integer.toString(sum));

                tempNum = new StringBuilder();
                seq = false;
            }
            if (!seq && !endDigit) stringOutput.append(stringInput.charAt(i));
        }
        return stringOutput.toString();
    }

    @Override
    public void convertDigitsToNamesInSubstring(int initialPosition, int finalPosition) {
        if(stringInput == null) {
            throw new NullPointerException("MyString.getString() is null");
        } else if(initialPosition < 1 || initialPosition > finalPosition) {
            throw new IllegalArgumentException("initialPosition is les than 1 or greater than finalPosition");
        } else if (finalPosition > stringInput.length()) {
            throw new MyIndexOutOfBoundsException("finalPosition out of bounds");
        }

        initialPosition -= 1;
        boolean isDigit;
        HashMap<String, String> digitMap = digitHashMap();
        String extractedStr = stringInput.substring(initialPosition, finalPosition);
        for (int i = 0; i < extractedStr.length(); i++) {
            isDigit = Character.isDigit(extractedStr.charAt(i));
            if(isDigit) {
                String oldDigit = String.valueOf(extractedStr.charAt(i)), newDigit = digitMap.get(oldDigit);
                extractedStr = extractedStr.replace(oldDigit, newDigit);
            }
        }
        StringBuilder sb = new StringBuilder(stringInput);
        sb.replace(initialPosition, finalPosition, extractedStr);
        stringInput = sb.toString();
    }

    private String invertString(String s) {
        StringBuilder sb = new StringBuilder();
        sb.append(s);
        return sb.reverse().toString();
    }

    private HashMap<String, String> digitHashMap() {
        HashMap<String, String> digitMap = new HashMap<>();
        digitMap.put("0", "zero");
        digitMap.put("1", "one");
        digitMap.put("2", "two");
        digitMap.put("3", "three");
        digitMap.put("4", "four");
        digitMap.put("5", "five");
        digitMap.put("6", "six");
        digitMap.put("7", "seven");
        digitMap.put("8", "eight");
        digitMap.put("9", "nine");

        return digitMap;
    }
}