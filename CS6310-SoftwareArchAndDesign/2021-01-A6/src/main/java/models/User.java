package models;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBAttribute;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBHashKey;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBTable;

@DynamoDBTable(tableName="Users")
public class User {

	String userId;
	String password;
	String firstName;
	String lastName;
	String role;
	
	public User() {
		super();
	}

	public User(String userId, String password) {
		this.userId = userId;
		this.password = password;
	}
	
	public User(String userId, String password, String firstName, String lastName, String role) {
		this.userId = userId;
		this.password = password;
		this.firstName = firstName;
		this.lastName = lastName;
		this.role = role;
	}
	
	@DynamoDBHashKey(attributeName = "user_id")
	public String getUserId() {
		return userId;
	}
	public void setUserId(String userId) {
		this.userId = userId;
	}
	
	@DynamoDBAttribute(attributeName="password")
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}

	@DynamoDBAttribute(attributeName="first_name")
	public String getFirstName() {
		return firstName;
	}
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}

	@DynamoDBAttribute(attributeName="last_name")
	public String getLastName() {
		return lastName;
	}
	public void setLastName(String lastName) {
		this.lastName = lastName;
	}

	@DynamoDBAttribute(attributeName="role")
	public String getRole() {
		return role;
	}
	public void setRole(String role) {
		this.role = role;
	}
    
	
}
