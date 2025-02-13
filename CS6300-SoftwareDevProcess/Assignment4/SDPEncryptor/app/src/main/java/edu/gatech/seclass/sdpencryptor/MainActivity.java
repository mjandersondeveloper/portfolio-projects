package edu.gatech.seclass.sdpencryptor;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private EditText missiveText;
    private EditText paramAText;
    private EditText paramBText;
    private TextView encryptedMissive;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        missiveText = findViewById(R.id.missiveID);
        paramAText = findViewById(R.id.aParamID);
        paramBText = findViewById(R.id.bParamID);
        encryptedMissive = findViewById(R.id.encryptedMissiveID);
    }

    public void handleClick(View view) {
        String missive = missiveText.getText().toString();
        String stringParamA = paramAText.getText().toString();
        String stringParamB = paramBText.getText().toString();
        StringBuilder finalMissive = new StringBuilder();
        boolean invalid = errorHandler(missive, stringParamA, stringParamB);

        if (!invalid) {
            int paramA = Integer.parseInt(stringParamA);
            int paramB = Integer.parseInt(stringParamB);

            for (int i = 0; i < missive.length(); i++) {
                String letter;
                if (Character.isLetter(missive.charAt(i)))
                    letter = affineCipher(String.valueOf(missive.charAt(i)), paramA,paramB);
                else
                    letter = String.valueOf(missive.charAt(i));
                finalMissive.append(letter);
            }
            encryptedMissive.setText(finalMissive);
        } else {
            // Clears any previous result if there's an error
            encryptedMissive.setText("");
        }
    }

    private HashMap<String, String> encryptionHashMap() {
        HashMap<String, String> encryptionMap = new HashMap<>();
        encryptionMap.put("a","0");
        encryptionMap.put("b","1");
        encryptionMap.put("c","2");
        encryptionMap.put("d","3");
        encryptionMap.put("e","4");
        encryptionMap.put("f","5");
        encryptionMap.put("g","6");
        encryptionMap.put("h","7");
        encryptionMap.put("i","8");
        encryptionMap.put("j","9");
        encryptionMap.put("k","10");
        encryptionMap.put("l","11");
        encryptionMap.put("m","12");
        encryptionMap.put("n","13");
        encryptionMap.put("o","14");
        encryptionMap.put("p","15");
        encryptionMap.put("q","16");
        encryptionMap.put("r","17");
        encryptionMap.put("s","18");
        encryptionMap.put("t","19");
        encryptionMap.put("u","20");
        encryptionMap.put("v","21");
        encryptionMap.put("w","22");
        encryptionMap.put("x","23");
        encryptionMap.put("y","24");
        encryptionMap.put("z","25");


        return encryptionMap;
    }

    private boolean errorHandler(String missive, String paramA, String paramB) {
        boolean isError = false;
        if (missive.isEmpty() || !missive.matches(".*[a-zA-Z]+.*")) {
            missiveText.setError("Invalid Missive");
            isError = true;
        }
        if (paramA.isEmpty() || calculateCoprime(Integer.parseInt(paramA)) != 1) {
            paramAText.setError("Invalid Parameter A");
            isError = true;
        }
        if (paramB.isEmpty() || (Integer.parseInt(paramB) < 1 || Integer.parseInt(paramB) >= 26)) {
            paramBText.setError("Invalid Parameter B");
            isError = true;
        }
        return isError;
    }

    private int calculateCoprime(int param) {
        // Code reference: http://www.blackwasp.co.uk/Coprime.aspx
        int max = 26;
        if (param < 1 || param >= max) { return 0; }
        while (param != 0 && max != 0) {
            if (param > max)
                param %= max;
            else
                max %= param;
        }
        return Math.max(param, max);
    }

    private String affineCipher(String letter, int paramA, int paramB) {
        HashMap<String, String> encryptionMap = encryptionHashMap();
        String encryptedNum = encryptionMap.get(letter.toLowerCase());
        if (encryptedNum != null) {
            int translatedNum = (Integer.parseInt(encryptedNum) * paramA + paramB) % 26;
            for (Map.Entry<String, String> entry: encryptionMap.entrySet()) {
                if (entry.getValue().equals(String.valueOf(translatedNum)))
                    return Character.isUpperCase(letter.charAt(0)) ? entry.getKey() : entry.getKey().toUpperCase();
            }
        }
        return "";
    }
}

