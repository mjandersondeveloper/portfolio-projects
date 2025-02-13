package security;

import javax.security.auth.login.LoginContext;
import javax.security.auth.login.LoginException;

public class AccessControl { 
    private LoginContext loginContext;
	private static final String jaasConfig = "src/main/resources/jaas.config";
    
    public void intialize(LoginContext loginContext) {
			this.loginContext = loginContext;
    }
    
    public void authenicate() {
    	try {    	
       	 	System.setProperty("java.security.auth.login.config", jaasConfig);
			loginContext = new LoginContext("jaasApplication", new ConsoleCallbackHandler());
			loginContext.login();			
		} catch (LoginException e1) {
			e1.printStackTrace();
		}
    }
    
    public void systemLogout() {
    	try {
			loginContext.logout();
		} catch (LoginException e) {
			e.printStackTrace();
		}
    }
}