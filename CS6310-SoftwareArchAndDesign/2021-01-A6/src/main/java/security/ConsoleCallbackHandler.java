package security;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import javax.security.auth.callback.Callback;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.callback.NameCallback;
import javax.security.auth.callback.PasswordCallback;
import javax.security.auth.callback.UnsupportedCallbackException;

public class ConsoleCallbackHandler implements CallbackHandler { 	
	public void handle(Callback[] callbacks) throws UnsupportedCallbackException, IOException {
    	for (Callback callback : callbacks) {
            if (callback instanceof NameCallback) {
                NameCallback nameCallback = (NameCallback) callback;
                nameCallback.setName(readLine(nameCallback.getPrompt()));
            } else if (callback instanceof PasswordCallback) {
                PasswordCallback passwordCallback = (PasswordCallback) callback;
                passwordCallback.setPassword(readPassword(passwordCallback.getPrompt()));
            } else {
                throw new UnsupportedCallbackException(callback);
            }
        }         
    }
 	
   private String readLine(String format, Object... args) throws IOException {
        if (System.console() != null) { return System.console().readLine(format, args); }
        System.out.print(String.format(format, args));
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        return reader.readLine();
    }

    private char[] readPassword(String format, Object... args) throws IOException {
        if (System.console() != null) { return System.console().readPassword(format, args); }
        return this.readLine(format, args).toCharArray();
    }
}
