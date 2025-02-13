package models;

import java.util.*;

import calculator.MiscMath;

public  class ServiceProvider {

    public String shortname;
    public String longname;
    public Map<String,Event> eventsAvailable;
    public int subcriptionProfit = 0;
    public int ppvProfit = 0;
    public int subscriptionPrice;
    public List<Event> order;
    Map<String,Integer> subscriptionsByMonth;
    Map<String,Integer> ppvByMonth;
    String currentMonth = "10,2020";
    String previousMonth = null;
    int licensingCosts = 0;
    //updates
    boolean isValidToUpdateService = true;
    
    public ServiceProvider(String shortname,String longname,int price )
    {
        this.shortname = shortname;
        this.longname  = longname;
        this.subscriptionPrice = price;
        this.order = new ArrayList<>();
        this.subscriptionsByMonth = new HashMap<>();
        this.eventsAvailable = new HashMap<>();
        this.ppvByMonth= new HashMap<>();
    }

    public void displayEvents()
    {
        for(Event x : order)
        {
            eventsAvailable.get(x.name+x.year);
            if(x.type.equals("movie"))
                System.out.println(this.shortname+","+ x.type+","+x.name+","+x.year);
            else
                System.out.println(this.shortname+","+ x.type+","+x.name+","+x.year+","+x.streamViewerPrice);
        }

    }

    public void itemsSold(String key, int count)
    {
        if(count == 0)
            return;

        Event event = eventsAvailable.get(key);
        if(event.type.equals("ppv"))
        {
            ppvProfit+=event.streamViewerPrice*count;
        }
        else{
            subcriptionProfit+=subscriptionPrice*count;
        }

    }

    //offer_ppv or offer_movie
    public void  purchaseMovieLicense(Pair<License,Event> purchase)
    {
        purchasePPVLicense(purchase,0);
    }

    public void purchasePPVLicense(Pair<License,Event> purchase,int ppvPrice)
    {

        Event eventPurchased = copyEvent(purchase.value);
        eventPurchased.streamViewerPrice = ppvPrice;
        License licensePurchased = purchase.key;
        eventPurchased.license = licensePurchased;
        licensingCosts+=licensePurchased.soldFor;
        eventsAvailable.put(eventPurchased.name+eventPurchased.year,eventPurchased);
        order.add(eventPurchased);
    }

    //returns a subscription for billing purposes
    public void sellSubscription(int count)
    {

        subcriptionProfit +=count*subscriptionPrice;
    }

    public void sellPPV(int count, int price)
    {
        ppvProfit+=price*count;
    }

    //Returns profit made from ppv sales and subsriptions sales 
    public int getRevenue()
    {
        return ppvProfit+subcriptionProfit;
    }

    public int getLicensingCosts()
    {
        return licensingCosts;
    }

    public void nextMonth()
    {

        previousMonth = currentMonth;
        subscriptionsByMonth.put(currentMonth, subcriptionProfit);
        ppvByMonth.put(currentMonth, ppvProfit);
        subcriptionProfit = 0;
        ppvProfit = 0;
        currentMonth = MiscMath.calculatenextMonth(currentMonth);
        eventsAvailable.clear();
        order.clear();
        
        //updates
        setIsValidToUpdateService(true);
    }
    public int subscriptionsForPreviousMonth()
    {
        if(previousMonth == null)
            return 0;

        int total = 0;

        for(int  v: subscriptionsByMonth.values())
        {
            total+= v;
        }

        return total;
    }
    public int ppvForPreviousMonth()
    {
        if(previousMonth == null)
            return 0;

        int total = 0;

        for(int  v: ppvByMonth.values())
        {
            total+= v;
        }

        return total;
    }
    public void displayoffer(String key)
    {
        if(!eventsAvailable.containsKey(key))
            return;
        String c = ",";
        Event event = eventsAvailable.get(key);
        if(event.type.equals("movie"))
            System.out.println(shortname+c+"movie"+c+event.name+c+event.year);
        else
            System.out.println(shortname+c+"ppv"+c+event.name+c+event.year+c+event.streamViewerPrice);
    }

    public Event copyEvent(Event prev){
        return new Event(prev.type, prev.name, prev.year,
                prev.duration,prev.eventDeveloper,prev.licenseFee);
    }

    public void displayInfo()
    {
        String c = ",";

        System.out.println("stream"+c + shortname+c+longname);
        System.out.println("subscription"+c+subscriptionPrice);
        int current = subcriptionProfit+ppvProfit;
        System.out.println("current_period"+c+current);

        if(previousMonth!= null)
        {
            int previous = subscriptionsByMonth.get(previousMonth)+ppvByMonth.get(previousMonth);
            System.out.println("previous_period"+c+previous);
        }

        else
            System.out.println("previous_period"+c+0);

        int total = subscriptionsForPreviousMonth()+ppvForPreviousMonth();
        System.out.println("total"+c+total);
        System.out.println("licensing"+c+ getLicensingCosts());
    }
    
    
    
    // updates
    public void updateService(String longname, int price)
    {
    	this.longname = longname;
    	this.subscriptionPrice = price;
    
    }
    
    public boolean getIsValidToUpdateService() {
        return isValidToUpdateService;
    }

    public void setIsValidToUpdateService(boolean value) {
        this.isValidToUpdateService = value;
    }
    
    public void retractMovie(String eventName, String year) {
    	
    	// remove the move from eventsAvailable
    	Event eventToBeRetract = eventsAvailable.get(eventName+year);
    	eventsAvailable.remove(eventName+year);
    	
    	//remove from order
    	order.remove(eventToBeRetract);
    }
}
