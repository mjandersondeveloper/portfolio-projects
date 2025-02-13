package models;

import java.util.*;

import calculator.MiscMath;

public class DemographicGroup
{

    String shortName;
    String longName;
    public int accountCapacity;
    double budget = 0;
    int moneySpent = 0;
    Map<Event,Integer> eventsWatched;
    List<Account> accounts;
    Map<String, Integer> profitsForMonth;
    String currentMonth = "10,2020";
    String previousMonth = null;
    //keeps track of subscriptions purchased
    Map<String, SubscriptionTracker> subscriptions;
  //  private Logger audit;
    //updates
    boolean isValidToUpdateGroup = true; /* service can make modifications before Group have accessed the content. */

    //inner class
    class SubscriptionTracker
    {
        Subscription subscription;
        public int numOfSubs = 0;

        SubscriptionTracker(Subscription subscription)
        {
            this.subscription = subscription;
        }

        public void incrementBy(int num)
        {
            numOfSubs+=num;
        }
    }

    public DemographicGroup(String shortname, String longname, int acountnum)
    {
        this.shortName = shortname;
        this.longName = longname;
        this.accountCapacity = acountnum;
        this.subscriptions = new HashMap<>();
        this.accounts = new ArrayList<>();
        this.eventsWatched = new HashMap<>();
        this.profitsForMonth = new HashMap<>();
    }

    public void removeAccounts(int num)
    {
        int i = 0;

        for(Account x: accounts)
        {
            if(i > accounts.size())
                break;
            accounts.remove(x);

            i++;
        }

    }


    public void addAccounts(int num)
    {
        for(int i =0;i < num; i++)
        {
            accounts.add(new Account());
        }
    }

    //returns the number of subcriptions purchased from streaming the passed in event
    public int updateEventsWatched(String eventname, String year, int timesWatched,ServiceProvider sp)
    {
        //does not contain the specified event
        if(!sp.eventsAvailable.containsKey(eventname+year))
            return 0;

        int purchasesNeeded = 0;
        Event event = sp.eventsAvailable.get(eventname+year);
        //if its a PPV handle transaction accordingly
        if(event.type.equals("ppv"))
        {
            ppvTransaction(event, timesWatched);
            purchasesNeeded = timesWatched;
        }

        //else if it's a Movie & part of a subscription
        else if(event.type.equals("movie"))
        {
            purchasesNeeded =  movieTransaction(timesWatched, sp);
        }

        //ADD TO EVENTS WATCHED 
        if(eventsWatched.containsKey(event))
        {
            int num = eventsWatched.get(event);
            num+=timesWatched;
            eventsWatched.put(event,Integer.valueOf(num));
        }
        else
        {
            eventsWatched.put(event, Integer.valueOf(timesWatched));
        }

        return purchasesNeeded;
    }

    //handles ppv transactions 
    private void ppvTransaction(Event event, int timesWatched)
    {
        eventPurchased(event.streamViewerPrice, timesWatched);
    }

    //handles movie transactions
    private int movieTransaction(int timesWatched, ServiceProvider sp)
    {   int subscriptionsBought = 0;

        if(BuyMore(timesWatched,sp.shortname))
        {
            subscriptionsBought = purchaseSubscription(timesWatched, sp.shortname, sp);
        }
        return subscriptionsBought;
    }

    private void eventPurchased(int price, int numWatched)
    {
        moneySpent += price*numWatched;
    }

    //returns tr
    public boolean BuyMore(int numWatching ,String subscription)
    {
        int numCurrent = 0;

        if(subscriptions.containsKey(subscription))
        {
            numCurrent += subscriptions.get(subscription).numOfSubs;
        }

        return (numCurrent < numWatching);
    }

    public int purchaseSubscription(int count, String subscription , ServiceProvider sp )
    {
        int needToBuy = 0;

        if(subscriptions.containsKey(subscription))
        {
            needToBuy = count - subscriptions.get(subscription).numOfSubs;
            SubscriptionTracker s = subscriptions.get(subscription);
            s.numOfSubs +=needToBuy;
            //subscription exists but needs to be updated
            subscriptions.put(subscription, s);
        }

        else
        {
            //didnt have any subscriptions, need to buy and add to sub tracker
            needToBuy = count;
            SubscriptionTracker t = new SubscriptionTracker(new Subscription(sp.subscriptionPrice, currentMonth));
            t.numOfSubs = count;
            subscriptions.put(subscription,t );
        }

        eventPurchased(sp.subscriptionPrice, needToBuy);

        return needToBuy;
    }

    public void nextMonth()
    {
        //subscriotions not valid 
        //save profits for month
        profitsForMonth.put(currentMonth, moneySpent);
        previousMonth = currentMonth;
        currentMonth = MiscMath.calculatenextMonth(currentMonth);
        moneySpent = 0;
        //reset subscription counts
        //clear subscriptions
        subscriptions.clear();
        
        //updates
        setIsValidToUpdateGroup(true);

    }

    private int previousMonthsSpending()
    {
        int totalSpent = 0;

        for(int month:profitsForMonth.values())
        {
            totalSpent+=month;
        }

        return totalSpent;
    }

    public void displayInfo()
    {
        String c = ",";

        System.out.println("demo"+c+shortName+c+longName);
        System.out.println("size"+c+accountCapacity);
        System.out.println("current_period"+c+moneySpent);

        if(previousMonth == null)
        {
            System.out.println("previous_period"+c+"0");
            System.out.println("total"+c+"0");
        }
        else
        {
            System.out.println("previous_period"+c+profitsForMonth.get(previousMonth));
            System.out.println("total"+c+previousMonthsSpending());
        }

    }
    // updates
    public boolean getIsValidToUpdateGroup() {
    	return isValidToUpdateGroup;
    }

    public void setIsValidToUpdateGroup(boolean value) {
    	this.isValidToUpdateGroup = value;
    }
    
    public void updateGroup(String longname, int acountnum) {
        this.longName = longname;
        this.accountCapacity = acountnum;
    }



}