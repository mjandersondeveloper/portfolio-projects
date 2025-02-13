package calculator;


public class MiscMath {
    public static int percentOf(double percent, int num)
    {
        //percent of num is 
        return (int)((percent/100) * num);
    }

    public static String calculatenextMonth(String current)
    {
        String[] c = current.split(",");
        int month = Integer.parseInt(c[0]);
        int year = Integer.parseInt(c[1]);

        if(month < 12 )
        {
            month+=1;
        }
        else
        {
            month = 1;
            year++;
        }

        return month+","+year;
    }
  
   
}
