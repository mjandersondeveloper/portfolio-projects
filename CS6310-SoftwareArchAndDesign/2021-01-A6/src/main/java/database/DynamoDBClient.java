package database;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBMapper;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBQueryExpression;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.ItemCollection;
import com.amazonaws.services.dynamodbv2.document.PutItemOutcome;
import com.amazonaws.services.dynamodbv2.document.ScanOutcome;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.document.TableCollection;
import com.amazonaws.services.dynamodbv2.document.spec.DeleteItemSpec;
import com.amazonaws.services.dynamodbv2.model.AttributeDefinition;
import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.KeySchemaElement;
import com.amazonaws.services.dynamodbv2.model.KeyType;
import com.amazonaws.services.dynamodbv2.model.ListTablesResult;
import com.amazonaws.services.dynamodbv2.model.ProvisionedThroughput;
import com.amazonaws.services.dynamodbv2.model.ScalarAttributeType;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;

import models.User;

public class DynamoDBClient {

	private static AmazonDynamoDB client;
	private static DynamoDB dynamoDB;

	public DynamoDBClient() {
		client = AmazonDynamoDBClientBuilder.standard().withRegion("us-east-1").build();
		dynamoDB = new DynamoDB(client);
	}

	public void getAllTables() {
		TableCollection<ListTablesResult> tables = dynamoDB.listTables();
		Iterator<Table> iterator = tables.iterator();

		while (iterator.hasNext()) {
			Table table = iterator.next();
			System.out.println(table.getTableName());
		}
	}

	public void getAllItems(String tableName) {
		ScanRequest scanRequest = new ScanRequest().withTableName(tableName);

		ScanResult result = client.scan(scanRequest);
		for (Map<String, AttributeValue> item : result.getItems()) {
			System.out.println(item);
		}
	}

	public Item getItem(String tableName, String key, String value) {
		Item item = null;
		Table table = dynamoDB.getTable(tableName);

		try {
			item = table.getItem(key, value);
			System.out.println("Successfully inserted item with key: " + key + ", value: " + value);
		} catch (Exception e) {
			System.err.println("Unable to insert item with key: " + key + ", value: " + value);
			System.err.println(e.getMessage());
		}
		return item;
	}

	public boolean insertItem(String tableName, String key, String value, Map<String, Object> infoMap) {
		boolean result = false;
		Table table = dynamoDB.getTable(tableName);

		try {
			PutItemOutcome outcome = table.putItem(new Item().withPrimaryKey(key, value).withMap("info", infoMap));
			System.out.println("Successfully inserted item " + outcome + " with key: " + key + ", value: " + value);
			result = true;
		} catch (Exception e) {
			System.err.println("Unable to insert item with key: " + key + ", value: " + value);
			System.err.println(e.getMessage());
		}
		return result;
	}

	public boolean deleteItem(String tableName, String key, String value) {
		boolean result = false;
		Table table = dynamoDB.getTable(tableName);
		DeleteItemSpec deleteItemSpec = new DeleteItemSpec().withPrimaryKey(key, value);

		try {
			table.deleteItem(deleteItemSpec);
			result = true;
			System.out.println("Successfully deleted item with key: " + key + ", value: " + value);
		} catch (Exception e) {
			System.err.println("Unable to delete item with key: " + key + ", value: " + value);
			System.err.println(e.getMessage());
		}
		return result;
	}

	public boolean mapObject(Object item) {
		boolean result = false;
		DynamoDBMapper mapper = new DynamoDBMapper(client);
		try {
			mapper.save(item);
			result = true;
		} catch (Exception e) {
			System.err.println("Unable to insert item to table");
			System.err.println(e.getMessage());
		}
		return result;
	}

	public User getUser(String userId, String password) {
		DynamoDBMapper mapper = new DynamoDBMapper(client);

		User partitionKey = new User();
		partitionKey.setUserId(userId);

		DynamoDBQueryExpression<User> queryExpression = new DynamoDBQueryExpression<User>()
				.withHashKeyValues(partitionKey);

		List<User> users = mapper.query(User.class, queryExpression);

		if (!users.isEmpty()) {
			User currentUser = users.get(0);
			if (currentUser.getPassword().equals(password)) {
				return currentUser;
			}
		}
		return null;
	}
	
	public void resetTable(String tablename, String partitionKey) {
		Table table = dynamoDB.getTable(tablename);
		ItemCollection<ScanOutcome> deleteoutcome = table.scan();
		Iterator<Item> iterator = deleteoutcome.iterator();

		while (iterator.hasNext()) {
		    table.deleteItem(partitionKey, iterator.next().get(partitionKey));
		}
	}
	
	public void getLogsForUser(String user)
	{
		try
		{
			Map<String,AttributeValue> expressionAttributeValues =  new HashMap<String, AttributeValue>();
			expressionAttributeValues.put(":val", new AttributeValue().withS(user));

			Map<String,String> expressionAttributeNames =  new HashMap<String, String>();
			expressionAttributeNames.put("#ts","timestamp");

			ScanRequest scanRequest = new ScanRequest()
				    .withTableName("Logs")
				    .withFilterExpression("user_id = :val")
				    .withProjectionExpression("user_id,message,#ts")
				    .withExpressionAttributeNames(expressionAttributeNames)
				    .withExpressionAttributeValues(expressionAttributeValues);

			ScanResult result = client.scan(scanRequest);

			for (Map<String, AttributeValue> item : result.getItems())
			{
			    System.out.println(item);
			}
		}

		catch(Exception e)
		{
			System.err.println("Unable to print for specified user");
			System.err.println(e.getMessage());
		}
	}

	public void getLogsByDate(String date)
	{
		try 
		{
			Map<String,AttributeValue> expressionAttributeValues =  new HashMap<String, AttributeValue>();
			Map<String,String> expressionAttributeNames =  new HashMap<String, String>();
			expressionAttributeNames.put("#ts","timestamp");
			expressionAttributeValues.put(":val2", new AttributeValue().withS(date));

			ScanRequest scanRequest = new ScanRequest()
				    .withTableName("Logs")
				    .withFilterExpression("#ts = :val2")
				    .withProjectionExpression("user_id,message,#ts")
				    .withExpressionAttributeNames(expressionAttributeNames)
				    .withExpressionAttributeValues(expressionAttributeValues);

			ScanResult result = client.scan(scanRequest);
			for (Map<String, AttributeValue> item : result.getItems()) {
			    System.out.println(item);
			}

		}

		catch(Exception e)
		{
			System.err.println("Unable to print for specified date");
			System.err.println(e.getMessage());
		}


	}

}
