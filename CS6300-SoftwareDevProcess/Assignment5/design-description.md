## Assignment 5: Software Design

### Design Description

Design Description

1.) _When the app is started, the user is presented with the main menu, which allows the user to (1) enter or edit current job details, (2) enter job offers, (3) adjust the comparison settings, or (4) compare job offers (disabled if no job offers were entered yet)._

This requirement was very straight-forward. I can see that the Main Menu screen will have a menu with four selections: _enter or edit current job details, enter job offers, adjust the comparison settings, and compare job offers_. To represent this, I&#39;ve made these four menu options into four separate classes respectfully, including a **MainMenu** class.

2.) _When choosing to enter current job details, a user will:_

For this requirement, I created a **CurrentJob** class to represent this menu option.

  a.) _Be shown a user interface to enter (if it is the first time) or edit all of the details of their current job, which consist of: 'jobDetails'_

From reading this requirement, I knew that the _\&lt;jobDetails\&gt;_ would be attributes in the **CurrentJob** class. However, in another requirement (3a), I saw that another screen also utilizes these attributes as well. To make the UML cleaner, I created another class called: **JobDetails** , which holds these attributes, and made an attribute: _details: JobDetails_ in the **CurrentJob** class. This reduces duplicate attributes between classes.

  b). _Be able to either save the job details or cancel and exit without saving, returning in both cases to the main menu._

The 'save job details' and 'cancel and exit without saving', called out to me as action verbs, so I converted both of these into operations(_saveDetails,_currentDetails_) in the **CurrentJob** class.

3.) _When choosing to enter job offers, a user will:_

For this requirement, I created a **JobOffers** class to represent this menu option.

  a.) _Be shown a user interface to enter all of the details of the offer, which are the same ones listed above for the current job._

Same explanation in 2a, the only difference is the class that _details: JobDetails_ is in **JobOffers** for this requirement.

  b.) _Be able to either save the job offer details or cancel._

Same explanation as 2b.

  c.) _Be able to (1) enter another offer, (2) return to the main menu, or (3) compare the offer (if they saved it) with the current job details (if present)._

This was not represented in the **JobOffers** class because these will be selections on the UI for this screen that is used for navigation. &#39;Enter another offer&#39; would save the details and refresh the current screen, &#39;return to main menu&#39; would navigate back to the menu screen, and &#39;compare the offer&#39; would navigate to the **CompareJobOffers** screen (explained in 5b)

4.) _When adjusting the comparison settings, the user can assign integer weights to: 'adjustmentWeights'. If no weights are assigned, all factors are considered equal._

Based on this requirement, I made an **AdjustComparison** class with the _'adjustmentWeights'_ as its attributes.

5.) _When choosing to compare job offers, a user will:_

For this requirement, I created a **CompareJobOffers** class to represent this menu option.

  a.) _Be shown a list of job offers, displayed as Title and Company, ranked from best to worst (see below for details), and including the current job (if present), clearly indicated._

Based on this requirement I&#39;ve added a _jobOffers: List\&lt;JobDetails\&gt;_ attribute within the **CompareJobOffers** class to represent the list of job offers that are needed to be compared. I&#39;ve added in a _rankJobs_ operation that will be used to rank each job from best to worst. This operation will use a **CalculateJobScore** utility class that will provide a weighted job score for each job offer in the system. The current job will also be indicated with a _isCurrentJob_flag in the **JobDetails** class.

  b.) _Select two jobs to compare and trigger the comparison._

This is represented by the _compareJobOffers_ operator within the **CompareJobOffers** class.

  c.) _Be shown a table comparing the two jobs, displaying, for each job: \&lt;details\&gt;_

This is not represented in my diagram because this requirement should be handled in the GUI as a table with the list of details already set in the **JobDetails** class.

  d.) _Be offered to perform another comparison or go back to the main menu._

This is also not represented in my diagram because it deals with the functionality in the GUI of the application.

6.) _When ranking jobs, a job&#39;s score is computed as the weighted sum of…._

This whole requirement is represented as a **CalculateJobScore** utility class with the _calculateScore_ operations. This operation uses the formula provided in the requirement, along with the weighted input from the respective attributes in the **AdjustComparison** and produces a score for each job offer provided from **JobDetails**.

7.) _The user interface must be intuitive and responsive._

This is not represented in my diagram because it will be handled in the implementation phase.

8.) _For simplicity, you may assume there is a single system running the app (no communication or saving between devices is necessary)._

This is also not represented in the diagram because it is related to implementation.

**Other Attributes**

_jobDetails_
title: String
company: String
city: String
state: String
livingCost: Money (represented with a **Money** utility class)
annualSalary: Money (represented with a **Money** utility class)
annualBonus: Money (represented with a **Money** utility class)
teleworkDays: Integer
leaveTime: Integer
companyShares: Integer
isCurrentJob: Boolean

_adjustmentWeights_
annualSalaryWeight: Integer
annualBonusWeight: Integer
teleworkDaysWeight: Integer
leaveTimeWeight: Integer
sharesOfferedWeight: Integer
