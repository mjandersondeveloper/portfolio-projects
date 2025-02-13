import java.util.Scanner;

import security.AccessControl;
import security.InMemoryLoginModule;

public class TestCaseReader {

    SystemHandler sys; 
    
    public TestCaseReader() {
    	
        sys = new SystemHandler();
    }

    public void processInstructions(Boolean verboseMode) {
    	sys.authenticate();
    	
        Scanner commandLineInput = new Scanner(System.in);
        String wholeInputLine;
        String[] tokens;
        final String DELIMITER = ",";
        boolean properAuth;

        while (true) {
            try {
                // Determine the next command and echo it to the monitor for testing purposes
                wholeInputLine = commandLineInput.nextLine();
                tokens = wholeInputLine.split(DELIMITER);
                System.out.println("> " + wholeInputLine);

                properAuth = InMemoryLoginModule.authorizathonRoleCheck(tokens[0], InMemoryLoginModule.role);
                
                if(properAuth) {
                	if (tokens[0].equals("create_demo")) {
                        if (verboseMode) { System.out.println("create_demo_acknowledged"); }

                        sys.create_demo(tokens[1], tokens[2], tokens[3]);

                    } else if (tokens[0].equals("create_studio")) {
                        if (verboseMode) { System.out.println("create_studio_acknowledged"); }

                        sys.create_studio(tokens[1], tokens[2]);
                    } 
                    else if (tokens[0].equals("create_event")) {
                        if (verboseMode) { System.out.println("create_event_acknowledged"); }
                       
                        sys.create_event(tokens[1], tokens[2], tokens[3], Integer.parseInt(tokens[4]), tokens[5],tokens[6]);
                    } 
                    else if (tokens[0].equals("create_stream")) {
                        if (verboseMode) { System.out.println("create_stream_acknowledged"); }
                        
                        sys.create_stream(tokens[1], tokens[2],tokens[3]);
                    } 
                    
                    else if (tokens[0].equals("offer_movie") || tokens[0].equals("offer_ppv")) {
                        if (verboseMode) { System.out.println(tokens[0] + "_acknowledged"); }
                        String offerType = tokens[0].substring(6);
                
                        if (offerType.equals("ppv")) {
                            sys.offer_ppv(tokens[1], tokens[2], tokens[3], tokens[4]);
                        } 
                        else
                            sys.offer_movie(tokens[1], tokens[2], tokens[3]);

                    } 
                    else if (tokens[0].equals("watch_event")) {
                        if (verboseMode) { System.out.println("watch_event_acknowledged"); }
                         sys.watch_event(tokens[1], tokens[2], tokens[3], tokens[4],tokens[5]);
                    } 

                    else if (tokens[0].equals("next_month")) {
                        if (verboseMode) { System.out.println("next_month_acknowledged"); }
                        sys.next_month();
                    } 

                    else if (tokens[0].equals("display_demo")) {
                        if (verboseMode) { System.out.println("display_demo_acknowledged"); }
                        sys.display_demo(tokens[1]);
                    } 

                    else if (tokens[0].equals("display_events")) 
                    {
                        if (verboseMode) { System.out.println("display_events_acknowledged"); }
                        sys.display_events();
                    } 
                	
                    else if (tokens[0].equals("display_stream")) 
                    {
                        if (verboseMode) { System.out.println("display_stream_acknowledged"); }
                        sys.display_stream(tokens[1]);
                    } 
                	
                    else if (tokens[0].equals("display_studio")) {
                        if (verboseMode) { System.out.println("display_studio_acknowledged"); }
                       sys.display_studio(tokens[1]);
                    } 
                	
                    else if (tokens[0].equals("display_offers")) {
                        if (verboseMode) { System.out.println("display_offers_acknowledged"); }
                        sys.display_offers();
                    }

                    else if (tokens[0].equals("logs_for_user")) {
     	                if (verboseMode) { System.out.println("logs_for_user_acknowledged"); }

     	                sys.logs_for_user(tokens[1]);
     	            } 

                     else if (tokens[0].equals("logs_for_date")) {
      	                if (verboseMode) { System.out.println("logs_for_date_acknowledged"); }

      	                sys.logs_for_date(tokens[1]+","+tokens[2]);
      	            } 

                    else if (tokens[0].equals("display_logs")) {
                        if (verboseMode) { System.out.println("display_logs_acknowledged"); }
                       
                        sys.display_logs();
                    }              	
                	
                	
                    else if (tokens[0].equals("display_time")) {
                        if (verboseMode) { System.out.println("display_time_acknowledged"); }
                        sys.displayTime();
                    }
                	
                    else if (tokens[0].equals("update_demo")) {//update_demo,<short name>,<long name>,<number of accounts>
                    	if (verboseMode) { System.out.println("update_demo_acknowledged"); }
                        sys.update_demo(tokens[1], tokens[2], tokens[3]);
    	            } 
                    
                    else if (tokens[0].equals("update_event")) {//update_event,<name>,<year produced>,<duration>,<license fee>
    	            	if (verboseMode) { System.out.println("update_event_acknowledged"); }
    	                sys.update_event(tokens[1], tokens[2], Integer.parseInt(tokens[3]), Integer.parseInt(tokens[4]));
    	            } 
                    
                    else if (tokens[0].equals("update_stream")) {
    	            	if (verboseMode) { System.out.println("update_stream_acknowledged"); }
    	            	sys.update_stream(tokens[1], tokens[2],tokens[3]);
    	            }
                    
                    else if (tokens[0].equals("retract_movie")) { // retract_movie, <streaming service>, <movie name>, <movie year>
                    	sys.retract_movie(tokens[1], tokens[2],tokens[3]);
    	            } 
                	
                    else {
                        if (verboseMode) { System.out.println("command_" + tokens[0] + "_NOT_acknowledged"); }
                    }
                	
                } 
                else if (tokens[0].equals("logout")) {                    
                    sys.logout();
                } else if (tokens[0].equals("stop")) {
                    break;
                } 
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println();
            }
        }

        if (verboseMode) { System.out.println("stop_acknowledged"); }
        commandLineInput.close();
    }

}


