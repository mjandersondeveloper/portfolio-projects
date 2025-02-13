import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import audit.SystemAudit;
import calculator.MiscMath;
import database.DynamoDBClient;
import models.DemographicGroup;
import models.Event;
import models.EventDeveloper;
import models.Pair;
import models.ServiceProvider;
import security.AccessControl;


public class SystemHandler {
	// DB Instance
	DynamoDBClient dbClient;

	// list of demographic groups
	Map<String, DemographicGroup> demographicGroups;

	// list of streaming services
	Map<String, ServiceProvider> serviceProviders;

	// list of event developers/studios
	Map<String, EventDeveloper> eventDevelopers;

	Map<String, Event> events;

	List<String> eventOrder;

	List<Pair<String, String>> offers;
	// current time
	public static String currentTime = "10,2020";

	private static final Logger logger = LoggerFactory.getLogger(SystemHandler.class);

	private SystemAudit audit;
	
	private AccessControl accessControl;
	
	boolean properAuth;

	// function nextMonth or we

	// constructor initializes items
	public SystemHandler() {
		dbClient = new DynamoDBClient();
		accessControl = new AccessControl();
		dbClient.resetTable("Logs", "log_id");
		demographicGroups = new HashMap<>();
		serviceProviders = new HashMap<>();
		eventDevelopers = new HashMap<>();
		events = new HashMap<>();
		eventOrder = new ArrayList<>();
		offers = new ArrayList<>();
		audit = new SystemAudit(logger,currentTime);
		
	}

	// #1 Create_demo,<short name>,<long name>,<number of accounts>
	public void create_demo(String shortname, String longname, String numAccounts) {
		DemographicGroup dg = new DemographicGroup(shortname, longname, Integer.parseInt(numAccounts));
		demographicGroups.put(shortname, dg);
		audit.info(dbClient, "Demographic group created " + longname);
	}

	// #2 Create_studio,<short name>,<long name>
	public void create_studio(String shortname, String longname) {
		EventDeveloper eventDeveloper = new EventDeveloper(shortname, longname, "studio");
		eventDevelopers.put(shortname, eventDeveloper);
		audit.info(dbClient, "Studio created " + longname);
	}

	// #3 Create_event,<type>,<name>,<year produced>,<duration>,<studio>, <license
	// fee>
	public void create_event(String type, String name, String year, int duration, String dev, String price) {
		// check for a valid studio
		if (!eventDevelopers.containsKey(dev))
			return;

		Event event = new Event(type, name, year, duration, dev, Integer.parseInt(price));

		events.put(name + year, event);
		eventOrder.add(name + year);
		// add event to studio it was created in
		eventDevelopers.get(dev).produceEvent(event);
		audit.info(dbClient, "Event created " + name + " " + year );
	}

	// #4 Create_stream,<short name>,<long name>,<subscription price>
	public void create_stream(String shortname, String longname, String subscriptionPrice) {
		ServiceProvider serviceProvider = new ServiceProvider(shortname, longname, Integer.parseInt(subscriptionPrice));
		serviceProviders.put(shortname, serviceProvider);
		audit.info(dbClient, "Streaming service created " + longname);
	}

	// #5 offer_movie,<streaming service>,<movie name>,<year produced>
	public void offer_movie(String stream, String name, String year) {
		if (!serviceProviders.containsKey(stream) || !events.containsKey(name + year))
			return;

		Event event = events.get(name + year);
		ServiceProvider sp = serviceProviders.get(stream);
		sp.purchaseMovieLicense(
				eventDevelopers.get(event.eventDeveloper).sellEventLicense(event.name, event.year, sp.shortname));

		offers.add(new Pair<>(name + year, stream));
		audit.info(dbClient, stream + " offering  " + name + " in " + year);

		// updates
		serviceProviders.get(stream).setIsValidToUpdateService(false);
	}

	// #6 offer_ppv,<streaming service>,<pay-per-view name>, <year
	// produced>,<viewing price>
	public void offer_ppv(String stream, String name, String year, String price) {
		if (!serviceProviders.containsKey(stream) || !events.containsKey(name + year))
			return;

		Event event = events.get(name + year);
		ServiceProvider sp = serviceProviders.get(stream);
		EventDeveloper eventDeveloper = eventDevelopers.get(event.eventDeveloper);
		sp.purchasePPVLicense(eventDeveloper.sellEventLicense(event.name, event.year, sp.shortname),
				Integer.parseInt(price));
		offers.add(new Pair<>(name + year, stream));
		audit.info(dbClient, stream + " offering  " + name + " at " + price);

		// updates
		serviceProviders.get(stream).setIsValidToUpdateService(false);
	}

	// #7 watch_event,<demographic group>,<percentage>, <streaming service>,<event
	// name>,<year produced>
	public void watch_event(String demo, String percentage, String stream, String event, String year) {
		// gets account capacity to see how many are watching based on %
		int numWatching = MiscMath.percentOf(Double.parseDouble(percentage),
				demographicGroups.get(demo).accountCapacity);
		// grab the demo groub and update the events watched
		int num = demographicGroups.get(demo).updateEventsWatched(event, year, numWatching,
				serviceProviders.get(stream));

		serviceProviders.get(stream).itemsSold(event + year, num);
		audit.info(dbClient, numWatching + " users in " + demo + " watched " + event + " " + year);

		// updates
		demographicGroups.get(demo).setIsValidToUpdateGroup(false);
		events.get(event + year).setIsValidToUpdateEvent(false);

	}

	// #8 next_month
	public void next_month() {
		// trigger next month function for all
		for (ServiceProvider sp : serviceProviders.values())
			sp.nextMonth();

		for (EventDeveloper ev : eventDevelopers.values())
			ev.nextMonth();

		for (DemographicGroup dg : demographicGroups.values())
			dg.nextMonth();
		// update the systems month too
		currentTime = MiscMath.calculatenextMonth(currentTime);

		// clear previous months offers
		offers.clear();
		audit.nextMonth(currentTime); //sets logs to display new month 
		audit.info(dbClient, "Next Month - " + currentTime );
	}

	// #9 display_demo,<short name>
	public void display_demo(String shortname) {
		demographicGroups.get(shortname).displayInfo();
		audit.info(dbClient, "Display " + shortname );
	}

	// #10 display_stream, <short name>
	public void display_stream(String shortname) {
		serviceProviders.get(shortname).displayInfo();
		audit.info(dbClient, "Display " + shortname );
	}

	// [11] display_studio,<short name>
	public void display_studio(String shortname) {
		eventDevelopers.get(shortname).displayInfo();
		audit.info(dbClient, "Display " + shortname);
	}

	// [12] display_events
	public void display_events() {
		for (String key : eventOrder)
			events.get(key).displayEvent();
		audit.info(dbClient, "Display all events");
	}

	// [13] display_offers
	public void display_offers() {
		for (Pair<String, String> x : offers) {
			String key = x.key;
			String streamingService = x.value;

			serviceProviders.get(streamingService).displayoffer(key);
		}
		audit.info(dbClient, "Display all Offers" );
	}

	// [14] display_time
	public void displayTime() {
		audit.info(dbClient, "Display Time");
	}

	// [15] stop
	public void stop() {
		System.exit(0);
	}

	// [16] update_demo
	public void update_demo(String shortname, String longname, String numAccounts) {
		DemographicGroup foundGroup = demographicGroups.get(shortname);
		/* 1. check if <short name> exist */
		if (foundGroup != null) {
			if (foundGroup.getIsValidToUpdateGroup()) { /* 2. demographic group has NOT accessed any movies or PPV */
				foundGroup.updateGroup(longname, Integer.parseInt(numAccounts));
				// demographicGroups.(shortname,new DemographicGroup(tokens[1], tokens[2],
				// Integer.parseInt(tokens[3])));
			}
			
			audit.info(dbClient,"Demo group " +longname+" updated to "+numAccounts +" accounts");
		}

	}

	// [17] update_event,<name>,<year produced>,<duration>,<license fee>
	public void update_event(String name, String year, int duration, int price) {
		Event foundEvent = events.get(name + year);
		EventDeveloper foundEventDeveloper = eventDevelopers.get(foundEvent.eventDeveloper);

		if (foundEvent != null && foundEventDeveloper != null) {
			if (foundEvent.getIsValidToUpdateEvent()) {
				foundEvent.updateEvent(duration, price);
				foundEventDeveloper.updateProduceEvent(foundEvent);
				
				audit.info(dbClient, "Update event "+name+" "+year + " to $"+price 
						+ " and duration"+duration );
			}
      
		}
		
	}

	// [18] update_stream
	public void update_stream(String shortname, String longname, String subscriptionPrice) {
		ServiceProvider foundService = serviceProviders.get(shortname);
		/* 1. check if <short name> exist */
		if (foundService != null) {
			if (foundService.getIsValidToUpdateService()) { /*
															 * 2. streaming service has NOT been used to access and view
															 * any movies
															 */
				foundService.updateService(longname, Integer.parseInt(subscriptionPrice));
				audit.info(dbClient, "Update streaming service "+longname+" to "+ "$"+subscriptionPrice);
			}
		}
	}

	// [19] retract_movie
	public void retract_movie(String serviceName, String movieName, String year) {
		ServiceProvider foundService = serviceProviders.get(serviceName);
		if (foundService != null) {
			foundService.retractMovie(movieName, year);
			audit.info(dbClient, "Retract movie " + movieName +" "+year+ " from " +serviceName );
		}
	}
	
	public void display_logs()
	{
			dbClient.getAllItems("Logs");
			audit.info(dbClient, "Display Logs ");
	}

	public void logs_for_user(String user)
	{
		dbClient.getLogsForUser(user);
		audit.info(dbClient, "Logs for user "+user);
	}

	public void logs_for_date(String currentTime)
	{
		dbClient.getLogsByDate(currentTime);
		audit.info(dbClient,"Logs for date "+currentTime);
	}
	
	public void authenticate()
	{
		accessControl.authenicate(); 
	}
	
	public void logout()
	{
		accessControl.systemLogout();
	}
}