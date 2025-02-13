package audit;

import org.slf4j.Logger;

import database.DynamoDBClient;
import security.InMemoryLoginModule;

public class SystemAudit {
	private static Logger logger;
	
	private String currentTime;
	
	public static String user = InMemoryLoginModule.userId;

	public SystemAudit(Logger logger,String time) {
		SystemAudit.logger = logger;
		currentTime = time;
	}

	public void info(DynamoDBClient dbClient, String message) {
		logger.info(message);
		dbClient.mapObject(new Log(message,InMemoryLoginModule.userId, "INFO",currentTime));
	}
	
	public void error(DynamoDBClient dbClient, String message) {
		logger.error(message);
		dbClient.mapObject(new Log(message, InMemoryLoginModule.userId, "ERROR",currentTime));
	}

	public void debug(DynamoDBClient dbClient, String message) {
		logger.error(message);
		dbClient.mapObject(new Log(message, InMemoryLoginModule.userId, "DEBUG",currentTime));
	}
	
	public void warn(DynamoDBClient dbClient, String message) {
		logger.error(message);
		dbClient.mapObject(new Log(message,InMemoryLoginModule.userId, "WARN",currentTime));
	}
	
	public void trace(DynamoDBClient dbClient, String message) {
		logger.error(message);
		dbClient.mapObject(new Log(message, InMemoryLoginModule.userId, "TRACE",currentTime));
	}
	
	public void nextMonth(String newDate)
	{
		this.currentTime = newDate;
	}
}
