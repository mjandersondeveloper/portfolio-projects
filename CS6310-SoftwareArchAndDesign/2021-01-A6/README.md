# Assignment 6: Streaming Wars Project Group 46
## Main features
```
1. Implemented authetication method with javax.security modules and database for storing credentials.
2. Implemented Authorization method with role based access control.
3. Implemented auditability functionality with system logs and additional log diplay functions.
4. Deployed AWS DynamoDB on cloud to supply storage for credentials and system logs.
5. Implemented extra update functions to meet project expections.
```
## To run the applicaiton
### Step 1 run executable jar file
```
java -jar streaming_wars.jar
(Please don't move .jar file to another location)
```
### Step 2 use below credentials to log in
```
Username: adon      Password: pass3     => name: Angela Don         role: editor
Username: andem     Password: pass1     => name: Marcus Anderson    role: user
Username: irene     Password: pass4     => name: Irene Yuan         role: admin
Username: nicole    Password: pass5     => name: Nicole Wang        role: user
Username: ryanan    Password: pass2     => name: Ryan An            role: admin
```
### Step 3 run commands
* Original commands
```
create_demo,<short name>,<long name>,<number of accounts>
create_studio,<short name>,<long name>
create_event,<type>,<name>,<year produced>,<duration>,<studio>,<license fee>
create_stream,<short name>,<long name>,<subscription price>
offer_movie,<streaming service>,<movie name>
offer_ppv,<streaming service>,<pay-per-view name>,<price>
watch_event,<demographic group>,<percentage>,<streaming service>,<event name>
next_month
display_demo,<short name>
display_stream,<short name>
display_studio,<short name>
display_events
display_offers
stop
```

* New commands
```
logs_for_user
logs_for_date
display_logs
display_time
update_demo,<short name>,<long name>,<number of accounts>
update_event,<name>,<year produced>,<duration>,<license fee>
update_stream,<shortname>,<longname>,<duration>,<subscription price>
retract_movie, <streaming service>, <movie name>, <movie year>
logout
```
## To setup development environment
### Step 1 install eclipse
```
1. Install latest eclipse version from: https://www.eclipse.org/downloads/
2. After eclipse is installed, open source code on eclipse.
```
### Step 2 set up AWS Credentials
```
1. To set up access key (Skip to next step because it's setup for our use case): https://docs.aws.amazon.com/toolkit-for-eclipse/v1/user-guide/setup-credentials.html
2. Open Eclipse’s Preferences dialog box and click AWS Toolkit in the sidebar
3. Type or paste your AWS access key ID in the Access Key ID box
4. Type or paste your AWS secret access key in the Secret Access Key box
5. Click Apply or OK to store your access key information
```
### Step 3 maven and run
```
1. Get all dependecies by right clicking project on explorer and maven -> update project
2. Run or debug as java applicaiton
```
