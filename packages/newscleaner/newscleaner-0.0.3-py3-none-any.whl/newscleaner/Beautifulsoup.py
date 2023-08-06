#!/usr/bin/env python
# coding: utf-8

# In[2]:


# importing all the important libraries
import re
import json
import html
import unicodedata
import pkg_resources
from bs4 import BeautifulSoup


# In[3]:


def cln(text):

    clean_text = re.sub('http[s]?://\S+', ' ', text) # removing all urls
    clean_text = re.sub('\S*@\S*\s?', '',clean_text) #removing all links
    clean_text = re.sub('\|*Advertisement\|*','',clean_text) #removing Advertisement keyword
    clean_text = re.sub('\|*(Getty Images)\|*','',clean_text) #removing getty images keyword
    clean_text = re.sub('\n|\t|\r','',clean_text) # removing tabs, nextline characters 
    clean_text = re.sub(r"\s+", " ",clean_text) # removing extra spaces
    clean_text = re.sub(r"\\" ,"",clean_text) #removing backslashes
    clean_text = re.sub("\(.*?\)|\[.*?\]","",clean_text)
    
    
    # Removing Pattern from independent.uk.co
    clean_text = re.sub(".*" + "r {{ /verifyErrors }}", '', clean_text)
    clean_text = re.sub(".*" + "Washington email" , '', clean_text)
    clean_text = re.sub(".*" + "breaking news emails", '', clean_text) 
    clean_text = re.sub(".*" + "for all the latest news", '', clean_text)
    clean_text = re.sub(".*" + "This email for free", '', clean_text)
    clean_text = re.sub(".*" + "Check email", '', clean_text)
    clean_text = re.sub(".*" + "Headlines email", '', clean_text)
    
    # msnbc pattern removal
    clean_text = re.sub("Tweet us " + ".*",'',clean_text)
    clean_text = re.sub("You can read more" + ".*",'', clean_text)
    
    #greenwich & ourmidland time pattern removal
    clean_text = re.sub("This is a carousel. Use Next and Previous buttons to navigate",'',clean_text)
    clean_text = re.sub("Show More",'',clean_text)
    clean_text = re.sub("Show Less",'',clean_text)
    
    #NJ.com 
    clean_text = re.sub("Our journalism needs your support" + ".*",'',clean_text)
    clean_text = re.sub("For NJ Advance",'',clean_text)
    clean_text = re.sub("COPYRIGHT 2023 CREATORS.COM",'',clean_text)
    clean_text = re.sub("Thank you for relying on us to provide" + ".*",'',clean_text)
    clean_text = re.sub("RELATED STORIES " + ".*",'',clean_text)
    clean_text = re.sub("The N.J. High School Sports newsletter" + ".*",'',clean_text)
    
    #nbcsports
    clean_text = re.sub("Subscribe to and rate" + ".*",'',clean_text)
    clean_text = re.sub(" Click here to follow the " + ".*",'',clean_text)
    clean_text = re.sub(" Download and follow the" + ".*",'',clean_text)

    #newsweek
    clean_text = re.sub("(}[\s]*Getty[\s]*{)",'}{',clean_text)
    clean_text = re.sub("Newsweek reached out to" + ".*",'',clean_text)
    clean_text = re.sub("Newsweek has reached out to" + ".*",'',clean_text)
    
    #click2houston
    #pattern_c2 = "___" + ".*"
    #clean_text = re.sub(pattern_c2,'',clean_text)
    
    #clickorlando
    clean_text = re.sub("Get today’s headlines in minutes with",'',clean_text)
    clean_text = re.sub("Your Florida Daily",'',clean_text)
    clean_text = re.sub("Click here for more information about" + ".*",'',clean_text)
    clean_text = re.sub("FILE - ",'',clean_text)
    
    #cleveland.com
    clean_text = re.sub(" See video of the play here ",'',clean_text)
    clean_text = re.sub("Get police blotters by email every weekday for free with our new Police Blotter newsletter."  + ".*",'',clean_text)
    clean_text = re.sub("Ad not displaying properly?" + ".*",'',clean_text)
    clean_text = re.sub("Get a jumpstart on the weekend. Sign up for Cleveland.com ’s" + ".*",'',clean_text)
    clean_text = re.sub("Read more of her work" + ".*",'',clean_text)
    
    #nbcboston
    clean_text = re.sub("Get Boston local news, weather forecasts, lifestyle and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub("’s newsletters.","",clean_text)
    clean_text = re.sub("Read the full story on NBCNews.com here.","",clean_text)
    clean_text = re.sub("(}[\s]*PHOTOS[\s]*{)","}{",clean_text)
    clean_text = re.sub("Get Boston local news, weather forecasts, lifestyle and entertainment stories to your inbox. ’s newsletters.",'',clean_text)
    
    #nbcchicago
    clean_text = re.sub("Get Chicago local news, weather forecasts, sports and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub("Read the full story on NBCNews.com here.","",clean_text)
    clean_text = re.sub("PHOTOS:","",clean_text)
    clean_text = re.sub("Download MyTeams Today!","",clean_text)
    clean_text = re.sub("""(}[\s]*Click here to)+[a-zA-Z=".\s\d&#-;,|<>:_'’]*({)""","",clean_text)
    clean_text = re.sub("Be sure to download the NBC Chicago app on your Apple or Android devices , or you can tune into the NBC 5 newscasts throughout the afternoon for the latest weather information.","",clean_text)
    clean_text = re.sub("For all the latest information, stay tuned to the NBC"+".*",'',clean_text)
    
    #nbcdfw
    clean_text = re.sub("Read the full story at NBCNews.com","",clean_text)
    clean_text = re.sub("Editor's note: All odds are provided by our partner, PointsBet ."+".*","",clean_text)
    clean_text = re.sub(" This story first appeared on TODAY.com . More from TODAY: ","",clean_text)
    
    #cnbc 
    clean_text = re.sub("Subscribe\xa0 here \xa0to get this report sent directly to your inbox each morning before markets open. ","",clean_text)
    clean_text = re.sub("watch now","",clean_text)
    clean_text = re.sub("Getty Images Entertainment | Getty Images","",clean_text)
    
    #wgntv
    clean_text = re.sub("Suggest a Correction","",clean_text)
    clean_text = re.sub("This is a developing story, follow"+".*","",clean_text)
    
    #fox2news
    clean_text = re.sub("You can find out more at"+".*","",clean_text)
    clean_text = re.sub("Photo: ","",clean_text)
    clean_text = re.sub("This story will be updated throughout the day.","",clean_text)
    clean_text = re.sub(r"The Conversation","",clean_text)
    clean_text = re.sub(r'(-)+', r'\1',clean_text)
    
    #nbcmiami
    clean_text = re.sub("Get South Florida local news, weather forecasts and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub(" More information on how to apply can be found here .","",clean_text)
    clean_text = re.sub("This story first appeared on TODAY.com."+".*","",clean_text)
    
    #india.com
    clean_text = re.sub("For breaking news and live news updates, like us on Facebook or follow us on Twitter and Instagram ."+".*","",clean_text)
    clean_text = re.sub("More Stories","",clean_text)
    
    clean_text = re.sub('\|*(Image source, )\|*','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Image caption, )\|*','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(More on this story)\|*.+','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Sign up for )\|*[a-z\sA-Z]+','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Sign up to )\|*[a-z\sA-Z]+','',clean_text) #removing bbc errors
    
    clean_text = re.sub('\|*(This content is created and maintained by a third party, )\|*.+','',clean_text) #removing cosmopliton error
    clean_text = re.sub('\|*(Download it for )\|*[a-z\sA-Z]+','',clean_text) #removing cosmopliton error
    clean_text = re.sub('({Android})','{}',clean_text) #removing cosmopliton error
    #clean_text = re.sub('(Follow )+\S+( on ).+','',clean_text) #removing cosmopliton error
    #clean_text = re.sub('(>Instagram<)','><',clean_text) #removing Advertisement keyword
    
    clean_text = re.sub('\|*(A version of this story appeared in the )\|*[a-z\sA-Z0-9.]+','',clean_text) #removing hollywood error
    clean_text = re.sub('\|*(Click here to subscribe.)\|*','',clean_text) #removing hollywood error
    
    clean_text = re.sub('\|*(For weekly email updates on\nresidential real estate news, )\|*.+','',clean_text) #removing nytimes error
    
    clean_text = re.sub("\|*(More News)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub("\|*(More Entertainment)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub("\|*(UP NEXT)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub("\|*(___)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub('\|*(This is a carousel. Use Next and Previous buttons to navigate)\|*','',clean_text) #removing stamfordadvocate error
    
    #clean_text = re.sub("\|*(Top news)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing thegurdian error
                     
    clean_text = re.sub('\|*(Required reading)\|*','',clean_text) #removing theatheletic error
    clean_text = re.sub("\|*(GO DEEPER{)\|*[/}a-zA-Z\s,'0-9:]+",'',clean_text) #removing theatheletic error
    
    clean_text = re.sub("\|*([A-Z])\|*[A-Z0-9\s',:.-]{20,}",'',clean_text) #removing foxnews error
    clean_text = re.sub("(NEW{)+[/a-zA-Z\s}!]+",'',clean_text) #removing foxnews error
    clean_text = re.sub('(}[\s]*Advertising[\s]*{)','}{',clean_text) #removing "Advertising" keyword
    
    clean_text = re.sub('(}[\s]*Advertising[\s]*{)','}{',clean_text) #removing "Advertising" keyword
    clean_text = re.sub("""([\s]*Also read[\s]*{/p})+[a-zA-Z{}=".\s\d&#-;,|<>:_'].+({/p})""",'',clean_text) #removing one para after "Also read" keyword
    clean_text = re.sub('(For more lifestyle news).+','',clean_text) #removing text after "For more lifestyle news" keyword
    clean_text = re.sub('(}[\s]*\(With inputs from agencies\)[\s]*{)','}{',clean_text) #removing "(With inputs from agencies)" keywords
    clean_text = re.sub('(({p}[\s]*Read)+[a-zA-Z{}=".\s\d&#-;,<>]+(on The Eastern Herald.))+[a-zA-Z{}=".\s\d&#-;,<>]+','',clean_text) #removing Last Lines in Eastern Herald keyword
    clean_text = re.sub("""(\{p\}\{strong\}[\s]*Also Read \|)+[a-zA-Z{}=".\s\d&#-;,<>:'?|@!~`$%^&*()_=+\[\]]+(\{/strong\}\{/p\})""",'',clean_text) #removing one para after "Also Read" keyword
    clean_text = re.sub("""({p}[\s]*SHARE THIS ARTICLE ON[\s]*{/p})+[a-zA-Z{}=".\s\d&#-;,*^@$!()+\[\]~`<>:_'\n?%]+""",'',clean_text) #removing text after "SHARE THIS ARTICLE ON" keyword
    clean_text = re.sub("""(\([\s]*Also read \|)+[a-zA-Z{}=".\s\d&#-;,<>:_']+(\))""",'',clean_text) #removing one para after "Also read |" keyword
    clean_text = re.sub("""(}[\s]*Also read:)+[a-zA-Z{}=".\s\d&#-;,<>:_']+({/a}{/p})""",'}',clean_text) #removing one para after "Also read:" keyword
    clean_text = re.sub("""(}[\s]*ALSO READ:)+[a-zA-Z{}=".\s\d&#-;,<>:_']+({/a}{/p})""",'}',clean_text) #removing one para after "ALSO READ: " keyword
    clean_text = re.sub("""(}[\s]*Also Read:)+[a-zA-Z{}=".\s\d&#-;,<>:_']+{/a}{/p}""",'}',clean_text) #removing one para after "ALSO READ: " keyword
    clean_text = re.sub("""(Also read \|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?]+({/a})""",'',clean_text) #removing one para after "Also read |" keyword
    clean_text = re.sub("""([\s]*Source:)+[\sA-Za-z.]+""",'',clean_text) #removing "Source:" keyword
    clean_text = re.sub("""(}[\s]*top videos[\s]*{)""",'}{',clean_text) #removing "top videos" keyword
    clean_text = re.sub("""(ALSO READ\|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?]+({/a})""",'',clean_text) #removing one para after "ALSO READ|" keyword
    clean_text = re.sub("""(}[\s]*Read all the)+[a-zA-Z{}=".\s\d&#-;,<>:()_]+(here[\s]*{/p})+[a-zA-Z{}=".\s\d&#-;,<>:()_]+""",'}',clean_text) #removing text after "Read all the ... here" keyword
    
    clean_text = re.sub("""(\{strong\}[\s]*ALSO READ \|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+\{/strong\}""",'',clean_text) #removing one para after "ALSO READ |" keyword
    clean_text = re.sub("""(\{strong\}\{b\}[\s]*ALSO READ[\s]*\{/b\})+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+\{/strong\}""",'',clean_text) #removing one para after "ALSO READ |" keyword
    clean_text = re.sub('(}[\s]*advertisement[\s]*{)','}{',clean_text) #removing "advertisement" keyword
    clean_text = re.sub("""(}--- ENDS ---{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "--- ENDS ---" keyword
    clean_text = re.sub("""(}[\s]*Read here:)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+{/a}{/p}""",'}',clean_text) #removing "Read here:" keyword
    clean_text = re.sub("""(}[\s]*\(With inputs from ANI\)[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With inputs from ANI)" keyword
    clean_text = re.sub("""(}[\s]*\(With PTI inputs\)[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With PTI inputs)" keyword
    clean_text = re.sub("""(}[\s]*ABOUT THE AUTHOR[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(ABOUT THE AUTHOR)" keyword
    clean_text = re.sub("""(\{strong\}[\s]*Also Read \|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+\{/strong\}\{/a\}""",'',clean_text) #removing one para after "Also Read |" keyword
    clean_text = re.sub("""(}[\s]*\(With inputs from PTI, ANI\)[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With PTI inputs)" keyword
    clean_text = re.sub("""(\{p\}\{strong\}[\s]*WATCH \|[\s]*\{/strong\}\{/p\})""",'',clean_text) #removing "WATCH |" keyword
    clean_text = re.sub("""(\{p\}\{strong\}[\s]*ALSO WATCH \|[\s]*\{/strong\}\{/p\})""",'',clean_text) #removing "WATCH |" keyword
    clean_text = re.sub("""(}[\s]*ADVERTISEMENT[\s]*{)""",'}{',clean_text) #removing "ADVERTISEMENT" keyword
    clean_text = re.sub("""(}[\s]*Express News Service[\s]*{)""",'}{',clean_text) #removing "Express News Service" keyword
    clean_text = re.sub("""(}[\s]*Online Desk[\s]*{)""",'}{',clean_text) #removing "Online Desk" keyword
    clean_text = re.sub(""".+([\s]*By[\s]*{)""",'{',clean_text) #removing text before "By" keyword
    clean_text = re.sub("""(}[\s]*AFP[\s]*{)""",'}{',clean_text) #removing "AFP" keyword
    clean_text = re.sub("""(}[\s]*PTI[\s]*{)""",'}{',clean_text) #removing "PTI" keyword
    clean_text = re.sub("""(}[\s]*ANI[\s]*{)""",'}{',clean_text) #removing "ANI" keyword
    clean_text = re.sub("""(}[\s]*IANS[\s]*{)""",'}{',clean_text) #removing "IANS" keyword
    clean_text = re.sub("""(}[\s]*View this post on Instagram[\s]*{)""",'}{',clean_text) #removing text "View this post on Instagram" keyword
    clean_text = re.sub("""(}[\s]*Latest Entertainment News[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With PTI inputs)" keyword
    clean_text = re.sub("""([\s]*Follow us on Image Source INSTAGRAM[\s]*{)""",'{',clean_text) #removing text "Follow us on Image Source INSTAGRAM" keyword
    clean_text = re.sub("""([\s]*Follow us on Image Source TWITTER[\s]*{)""",'{',clean_text) #removing text "Follow us on Image Source TWITTER" keyword
    clean_text = re.sub("""(}[\s]*Read More Trending News[\s]*{)""",'}{',clean_text) #removing text "Read More Trending News" keyword
    clean_text = re.sub("""(}[\s]*Here's how they reacted.[\s]*{)""",'}{',clean_text) #removing text "Here's how they reacted." keyword
    clean_text = re.sub("""(}[\s]*Check out the photos here-[\s]*{)""",'}{',clean_text) #removing text "Check out the photos here-" keyword
    clean_text = re.sub("""(}[\s]*Unsplash[\s]*{)""",'}{',clean_text) #removing "Unsplash" keyword
    clean_text = re.sub("""(}[\s]*Screenshot[\s]*{)""",'}{',clean_text) #removing "Screenshot" keyword
    clean_text = re.sub("""(}[\s]*screenshot[\s]*{)""",'}{',clean_text) #removing "screenshot" keyword
    clean_text = re.sub("""(}[\s]*Agencies[\s]*{)""",'}{',clean_text) #removing "Agencies" keyword
    clean_text = re.sub("""(}[\s]*Twitter[\s]*{)""",'}{',clean_text) #removing "Twitter" keyword
    clean_text = re.sub("""(}[\s]*TWITTER[\s]*{)""",'}{',clean_text) #removing "TWITTER" keyword
    clean_text = re.sub("""(}[\s]*Reddit[\s]*{)""",'}{',clean_text) #removing "Reddit" keyword
    clean_text = re.sub("""(}[\s]*Instagram[\s]*{)""",'}{',clean_text) #removing "Instagram" keyword
    clean_text = re.sub("""(}[\s]*INSTAGRAM[\s]*{)""",'}{',clean_text) #removing "INSTAGRAM" keyword
    clean_text = re.sub("""(}[\s]*Facebook[\s]*{)""",'}{',clean_text) #removing "Facebook" keyword
    clean_text = re.sub("""(}[\s]*FACEBOOK[\s]*{)""",'}{',clean_text) #removing "FACEBOOK" keyword
    clean_text = re.sub("""(}[\s]*Telegram[\s]*{)""",'}{',clean_text) #removing "Telegram" keyword
    clean_text = re.sub("""(}[\s]*TELEGRAM[\s]*{)""",'}{',clean_text) #removing "TELEGRAM" keyword
    clean_text = re.sub("""(}[\s]*web screen grab[\s]*{)""",'}{',clean_text) #removing "web screen grab" keyword
    clean_text = re.sub("""(}[\s]*Reuters[\s]*{)""",'}{',clean_text) #removing "Reuters" keyword
    clean_text = re.sub("""(}[\s]*What do you think about it? Do let us know in the comments.[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "What do you think about it? Do let us know in the comments." keyword
    clean_text = re.sub("""(}[\s]*Click here .[\s]*{)""",'}{',clean_text) #removing "Click here ." keyword
    
    clean_text = re.sub("""(}[\s]*Poll[\s]*{)+[{}a-z/\s]+(}[\s]*0 votes[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "Poll 0 votes" keyword
    clean_text = re.sub("""([\s]*Leave your thoughts in the comments section below.[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'',clean_text) #removing text after "Leave your thoughts in the comments section below." keyword
    clean_text = re.sub("""(}[\s]*Check out the full video below[\s]*{)""",'}{',clean_text) #removing "Check out the full video below" keyword
    clean_text = re.sub("""(\}[\s]*Read all the \{strong\} Latest News \{/strong\}, \{strong\} Trending News \{/strong\}, \{strong\} Cricket News \{/strong\}, \{strong\} Bollywood News \{/strong\}, \{strong\} India News \{/strong\} and \{strong\} Entertainment News \{/strong\} here. Follow us on Facebook , Twitter and Instagram .\{/p\})""",'}',clean_text) #removing "Read all the Latest News , Trending News , Cricket News , Bollywood News , India News and Entertainment News here. Follow us on Facebook , Twitter and Instagram ." keyword
    clean_text = re.sub("""(}[\s]*Related[\s]*{)""",'}{',clean_text) #removing "Related" keyword
    clean_text = re.sub("""({b}IPL 2023{/b} {b} . {/b} {b}Dream11 Prediction{/b} {b} . {/b} {b}Fantasy Cricket Tips{/b} {b} . {/b} {b}Cricket Match Prediction Today{/b} {b} . {/b} {b}Cricket News{/b} {b} . {/b} {b}Cricket Live Score{/b})""",'',clean_text) #removing "IPL 2023 . Dream11 Prediction . Fantasy Cricket Tips . Cricket Match Prediction Today . Cricket News . Cricket Live Score" keyword
    clean_text = re.sub("""({b}IPL 2023{/b} {b} .{/b} {b}India National Cricket Team{/b} {b}. {/b} {b}Chennai Super Kings {/b} {b} . {/b} {b}Delhi Capitals {/b} {b} . {/b} {b}Gujarat Titans {/b} {b} . {/b} {b}Kolkata Knight Riders {/b} {b} . {/b} {b}Lucknow Supergiants {/b} {b} . {/b} {b}Mumbai Indians {/b} {b} . {/b} {b}Punjab Kings {/b} {b} . {/b} {b}Rajasthan Royals {/b} {b} . {/b} {b}Royal Challengers Bangalore {/b} {b} . {/b} {b}SunRisers Hyderabad {/b})""",'',clean_text) #removing "IPL 2023 . India National Cricket Team . Chennai Super Kings . Delhi Capitals . Gujarat Titans . Kolkata Knight Riders . Lucknow Supergiants . Mumbai Indians . Punjab Kings . Rajasthan Royals . Royal Challengers Bangalore . SunRisers Hyderabad" keyword
    clean_text = re.sub("""({b}Virat Kohli{/b} {b} . {/b} {b}Rohit Sharma{/b} {b} . {/b} {b}Rishabh Pant{/b} {b} . {/b} {b}KL Rahul{/b} {b} . {/b} {b}Suryakumar Yadav{/b} {b} . {/b} {b}Sanju Samson{/b} {b} . {/b} {b}Shreyas Iyer{/b} {b} . {/b} {b}Yuzvendra Chahal{/b} {b} . {/b} {b}Jasprit Bumrah{/b})""",'',clean_text) #removing "Virat Kohli . Rohit Sharma . Rishabh Pant . KL Rahul . Suryakumar Yadav . Sanju Samson . Shreyas Iyer . Yuzvendra Chahal . Jasprit Bumrah" keyword
    clean_text = re.sub("""(}[\s]*Follow InsideSport on GOOGLE NEWS[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "Follow InsideSport on GOOGLE NEWS" keyword
    clean_text = re.sub("""(}[\s]*Here’s the video[\s]*{)""",'}{',clean_text) #removing "Here’s the video" keyword
    clean_text = re.sub("""(}[\s]*Here is the video[\s]*{)""",'}{',clean_text) #removing "Here is the video" keyword
    clean_text = re.sub("""(}[\s]*Stay tuned to BollywoodLife for the latest scoops and updates from Bollywood , Hollywood , South , TV and Web-Series .[\s]*{)""",'}{',clean_text) #removing "Stay tuned to BollywoodLife for the latest scoops and updates from Bollywood , Hollywood , South , TV and Web-Series ." keyword
    clean_text = re.sub("""(}[\s]*Click to join us on Facebook , Twitter , Youtube and Instagram .[\s]*{)""",'}{',clean_text) #removing "Click to join us on Facebook , Twitter , Youtube and Instagram ." keyword
    clean_text = re.sub("""(}[\s]*Also follow us on Facebook Messenger for latest updates.[\s]*{)""",'}{',clean_text) #removing "Also follow us on Facebook Messenger for latest updates." keyword
    clean_text = re.sub("""(}[\s]*Click Here To Read/Download Order[\s]*{)""",'}{',clean_text) #removing "Click Here To Read/Download Order" keyword
    clean_text = re.sub("""(}[\s]*Click Here To Read/Download Judgement[\s]*{)""",'}{',clean_text) #removing "Click Here To Read/Download Judgement" keyword
    
    clean_text = re.sub("""(}[\s]*View this post on Instagram[\s]*{)""",'}{',clean_text) #removing text "View this post on Instagram" keyword
    clean_text = re.sub("""(}[\s]*SHARE[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "SHARE" keyword
    clean_text = re.sub("""(}[\s]*Also read)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]‘’]+({)""",'}{',clean_text) #removing text "Also read" keyword
    clean_text = re.sub("""(}[\s]*READ NOW[\s]*{)""",'}{',clean_text) #removing before "READ NOW" keyword
    clean_text = re.sub("""(}[\s]*Also read)""",'}',clean_text) #removing before "READ NOW" keyword    
    
    
    clean_text = re.sub('(\n)','',clean_text) #removing new line character
    clean_text = re.sub('({p}{br}{/p})','',clean_text) # removing line break
    clean_text = re.sub('({p}[\s]*{/p})','',clean_text) #removing empty p-tag keyword
    clean_text = re.sub('(\{strong\}[\s]*\{/strong\})','',clean_text) #removing empty strong-tag keyword
    clean_text = re.sub('({/a}[\s]*{/a})','',clean_text) #removing empty a-tag keyword


    clean_text = html.unescape(clean_text) #decoding unicode entities using html parser
    #clean_text = replace_all1(clean_text,tags) 
    
    # cleaning emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    
    clean_text = emoji_pattern.sub(r'', clean_text)
    clean_text = unicodedata.normalize("NFKD",clean_text) #decoding utf-8 unicode data which is producing spacing
    
    soup = BeautifulSoup(clean_text,'html.parser')
    for e in soup.find_all():
        if e.name not in ['p','br','img','span','b','h1','h2','h3','h4','h5','h6','i','u','strong','ul','ol','td','tr']:
            e.unwrap()

    return soup


# In[ ]:




