package models;
import java.util.*;

public class Account {
    
    String name;
    int id;
    Map<String,Subscription> subscriptions;
    List<Event> purchases;
    double totalSpent;

    public Account()
    {
        subscriptions = new HashMap<>();
        purchases = new ArrayList<>();
    }
    public void addSubscription(int price, String startDate)
    {
        Subscription s = new Subscription(price, startDate);
        subscriptions.put(startDate,s);
    }
    
    public void addPPV(Event event)
    {
        purchases.add(event);
    }
    
}
