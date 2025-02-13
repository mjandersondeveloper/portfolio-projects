package models;

import java.util.*;

import calculator.MiscMath;



public  class EventDeveloper {
    public Map<String, Event> eventsProduced;
    public Map<String, Integer> eventPrices;
    public String type;
    public int profits;
    public Map<String,License> eventsSold;
    public List<String> order;
    public String shortname;
    public String longname;
    public Map<String,Integer> profitsByMonth;
    String currentMonth = "10,2020";
    String previousMonth = null;
    

    public EventDeveloper(String shortname,String longname, String type)
    {
        this.shortname = shortname;
        this.longname = longname;
        this.type = type;
        this.eventsProduced = new HashMap<>();
        this.eventsSold = new HashMap<>();
        this.order = new ArrayList<>();
        this.profitsByMonth = new HashMap<>();
        this.eventPrices = new HashMap<>();
    }
    
    public Pair<License,Event> sellEventLicense(String event, String eventYr, String provider)
    {
        //check if i carry that event, if not then return
        if(!eventsProduced.containsKey(event+eventYr))
            return null;

        Event eventToBeSold = eventsProduced.get(event+eventYr);
        License license = new License(event, eventYr, provider, longname, eventToBeSold.licenseFee);

        profits += eventToBeSold.licenseFee;
        eventsSold.put(currentMonth,license);
        
        return new Pair<>(license, eventToBeSold);
    }
    
    public List<License> licensesSold()
    {
        return new ArrayList<License>(eventsSold.values());
    } 
    
    public int calculateProfit()
    {
        int totalProfitsMade = 0;

        for(int x: profitsByMonth.values())
        {
            totalProfitsMade+=x;
        }

        return totalProfitsMade;
    }

    public Event produceEvent(Event x )
    {
        Event newEvent = new Event(x.type, x.name, x.year, x.duration,this.longname, x.licenseFee);
        String key = x.name+x.year;

        eventsProduced.put(key,newEvent);
        eventPrices.put(key, Integer.valueOf(x.licenseFee));
        order.add(key);
        return newEvent;
    }

    public void displayInfo()
    {
        String c = ",";
        System.out.println("studio"+c+shortname+c+longname);
        System.out.println("current_period"+c+profits);
        if(previousMonth!=null)
        {
            System.out.println("previous_period"+c+profitsByMonth.get(previousMonth));
            System.out.println("total"+c+calculateProfit());
        }
            
        else
        {
            System.out.println("previous_period"+c+"0");
            System.out.println("total"+c+"0");
        }
    

    }

    public void nextMonth()
    {
        profitsByMonth.put(currentMonth,profits);
        previousMonth = currentMonth;
        currentMonth = MiscMath.calculatenextMonth(currentMonth);
        profits = 0;

        //updates
        for (Event event: eventsProduced.values()) 
        {
        	event.setIsValidToUpdateEvent(true);
        }
    }
    
    // updates update_event,<name>,<year produced>,<duration>,<license fee>
    public void updateProduceEvent(Event x)
    {
        //Event newEvent = new Event(x.type, x.name, x.year, x.duration,this.longname, x.licenseFee);
        String key = x.name+x.year;

        eventsProduced.replace(key,x);
        eventPrices.replace(key, Integer.valueOf(x.licenseFee));

        //eventsProduced.replace(key,foundEvent);
        //eventPrices.replace(key, Integer.valueOf(foundEvent.licenseFee));
    }
}
