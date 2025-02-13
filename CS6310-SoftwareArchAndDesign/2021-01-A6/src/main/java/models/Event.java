package models;
import java.util.*;

//todo: figure out licenses stuff

public class Event 
{
     public String name;
     public int duration;
     public String type;
     public List<String> genres;
     public String year;
     public String eventDeveloper;
     public License license = null;
     public int licenseFee;
     public int streamViewerPrice = 0;
     // updates
     boolean isValidToUpdateEvent = true;     

    public Event(String type, String name, String yearPrd, 
    int duration,String evdev,int licensefee)
    {
        this.name = name;
        this.duration = duration;
        this.eventDeveloper = evdev;
        this.type = type;
        this.year = yearPrd;
        this.licenseFee = licensefee;

    }

    public License getLicense()
    {
        return this.license;
    }

    public void displayEvent()
    {
        String c = ",";
        
        System.out.println(type+c+name+c+year+c+duration+c+eventDeveloper+c+licenseFee);

    }
    
    // updates
    public void updateEvent(int duration, int licensefee)
    {
        this.duration = duration;
        this.licenseFee = licensefee;   	

    }
    

    public void setIsValidToUpdateEvent(boolean value)
    {
    	this.isValidToUpdateEvent = value;
    }

    public boolean getIsValidToUpdateEvent()
    {
    	return this.isValidToUpdateEvent;
    }

}
