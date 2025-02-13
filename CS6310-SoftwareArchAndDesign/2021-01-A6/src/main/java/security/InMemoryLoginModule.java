package security;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import javax.security.auth.Subject;
import javax.security.auth.callback.Callback;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.callback.NameCallback;
import javax.security.auth.callback.PasswordCallback;
import javax.security.auth.callback.UnsupportedCallbackException;
import javax.security.auth.login.LoginException;
import javax.security.auth.spi.LoginModule;

import database.DynamoDBClient;
import models.User;


public class InMemoryLoginModule implements LoginModule { 
	private DynamoDBClient dbClient;
    private Subject subject;

    private CallbackHandler callbackHandler;
    private Map<String, ?> sharedState;
    private Map<String, ?> options;
    
    private boolean userFound = false;
    private boolean loginSucceeded = false;
    private int loginAttempts = 3;
   
    private static String fname;
    private static String lname;
    public static String role;
    public static String userId;

    public void initialize(Subject subject, CallbackHandler callbackHandler, Map<String, ?> sharedState, Map<String, ?> options) {
    	dbClient = new DynamoDBClient();
    	this.subject = subject;
	    this.callbackHandler = callbackHandler;
	    this.sharedState = sharedState;
	    this.options = options;
	    
    	System.out.println("Please enter your username and password:");
	}
    
    @Override
    public boolean login() throws LoginException {
        NameCallback nameCallback = new NameCallback("username: ");
        PasswordCallback passwordCallback = new PasswordCallback("password: ", false);
        try {
            callbackHandler.handle(new Callback[]{nameCallback, passwordCallback});
            String username = nameCallback.getName();
            String password = new String(passwordCallback.getPassword());     
            
            User userInfo = dbClient.getUser(username, password);           
            userFound = canSetUserInformation(userInfo);           
            	
            if (userFound && loginAttempts > 0) {
                loginSucceeded = true;
        		System.out.println("Login successful! Welcome: " + fname + " " + lname);
        		System.out.println("Your authorization role is: '" + role + "'. You have access to the following commands: " + commandAccessMessage(role));
        		System.out.println("To switch accounts, enter 'logout'. To exit the system, enter 'stop'.");
            } else { 
            	if(loginAttempts > 1) {
            		loginAttempts--;
            		System.out.println("Incorrect username/password - Login attempts remaining: " + loginAttempts);
            		login();
            	} else {
            		System.out.println("Three incorrect login attempts - exiting the system");
                	System.exit(0); 
            	}            
            }            
        } catch (IOException | UnsupportedCallbackException e) {
        	e.printStackTrace();
        }
        return loginSucceeded;
    }
    
    public static String commandAccessMessage(String role) {
    	if(role.equals("admin")) {
    		return "'create', 'update', 'revoke', 'offer', 'watch', 'next_month','display_logs','logs_for_user','logs_for_date', and 'display'";
    	} else if(role.equals("editor")) {
    		return "'update', 'revoke', 'offer', 'watch', and 'display'";
    	} else {
    		return "'watch' and 'display'";
    	}
    }
    
	public static boolean authorizathonRoleCheck(String command, String role) {
		List<String> logCommands = Arrays.asList("display_logs", "logs_for_user", "logs_for_date");
		List<String> createCommands = Arrays.asList("create_demo", "create_studio", "create_event", "create_stream");
		List<String> updateCommands = Arrays.asList("update_demo", "update_event", "update_stream");
		List<String> offerCommands = Arrays.asList("offer_movie", "offer_ppv");
		
		if (command.equals("logout") || command.equals("stop")) {
			return false;
		} else if (role.equals("editor")) {
			if (createCommands.contains(command)|| logCommands.contains(command) || command.equals("next_month")) {
				System.out.println("You are unauthorized to access this command. You can only access: " + commandAccessMessage(role)); return false;
			}
		} else if (role.equals("user")) {
			if (createCommands.contains(command)  || logCommands.contains(command)|| updateCommands.contains(command) || command.equals("retract_movie")
					|| offerCommands.contains(command) || command.equals("next_month")) {
				System.out.println("You are unauthorized to access this command. You can only access: "
						+ commandAccessMessage(role)); return false;
			}
		}

		return true;
	}

    private boolean canSetUserInformation(User user) {
    	if(user != null) {
        	fname = user.getFirstName();
    		lname = user.getLastName();
    		role = user.getRole();
    		userId = user.getUserId();
    		
        	return true;
        } 
    	return false;
    }
    
    @Override
    public boolean commit() throws LoginException {
        if (!loginSucceeded) {
            return false;
        }
        return true;
    }

	@Override
	public boolean abort() throws LoginException { return false; }

	@Override
	public boolean logout() throws LoginException { 
    	System.out.println("Logout successful! Please enter your username and password:");
		login(); return true;
	}
}