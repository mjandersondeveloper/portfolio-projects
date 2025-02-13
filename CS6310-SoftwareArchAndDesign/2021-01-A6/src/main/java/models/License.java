package models;

public class License {
    
    public String eventName;
    public String serviceProvider;
    public String eventDeveloper;
    public String yearEventPr;
    public int soldFor;
    
    
    public License(String eventName, String eventYr,String servPr, String eveDev, int soldFor)
    {
        this.eventName = eventName;
        this.serviceProvider = servPr;
        this.eventDeveloper = eveDev;
        this.yearEventPr = eventYr;
        this.soldFor = soldFor;
    }

    public void setServiceProvider(String buyer)
    {
        this.serviceProvider = buyer;
    }

}
