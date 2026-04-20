## Welcome to Jason Monitoring
Jason Monitroing was born on my first job: At Clara Resorts Hotel, in Ibiuna São Paulo ( Brazil ). When i was working as kid monitor on Clara we had a task tha consume much time and people resource: List all the kids that've made the checkin.
### The older process
Imagine this: a family of guests arrives at the hotel and begins the check-in process at reception, receiving a paper form with fields where they must fill in all the information about their children; So, they start filling in all the information on the form; no problem? Okay, now the problems start to appear.

#### Whats the problem?
At the 9am and 7pm, all the monitoring team should make a list, containing the info about ALL the childrens that was registered at the reception. Sometimes, we had more than 200 kids in the hotel ( at weekend we easily surpass this mark ) and this isn't the worst. A lot of the infos are unreadable, missing or just incomplete. That process wasn't just inefficient and with a lot possible mistakes, leading me to improve it with my own solution.

### The New Process
So, i was lead to see what i could do: 
- A lot of paper forms and at least 600 registers that are made all the weeks;
- A Monitoring Team ( wich i am a part ) that uses whatsapp for every comunication.
- And a process that make us to consume much time.

I decided to make the most simple way: 
- Remove the entire paper process, making a digital form, acessible by any QRcode on the hotel. No the guests should scan with their smartphones, this solve almost all the mistakes, blank fields or incomplete infos, and gave us much more control about the infos;
- This data was validated and stored at a postgresql, and later, was used by my API;
- Now, our team could easily consult the data by our main way of comunication on the hotel: Whatsapp. With Twilio API and my API comunication, i've made a bot that list all the childrens wich was returned from PostgresDB based on one simple command that you type for the bot.

## The Result
Now, we dont need more 3 of our team to just make the list: The bot make it for us; We dont need to constantly check if some data was updated at the reception, just check at the bot, and he will send the real time information about the kids; Now, with that data, we could see more than just the parents infos and room number, we can see the allergies that the kids have, some restrictions ( Like, don't know how to swim properly ), or even more infos and make graphics ( Like, how many kids stay at the hotel until the thursday ).

# The current state of that project...
Now, im working on a complete rewrite of this project, because it was made in a poor ( but efficient way ) you could see the older repo [here](https://github.com/Jason21tod/jason-wpp-bot). Stay tunned to see what im building and star this repo if you like it.
