This Python 3 script allows you to generate a reply to an iCalendar invitation, the most common way to invite people to events by email.

A lot of mail user agents handle this by showing buttons to accept or decline invitation. Unfortunately, some of them do not.

A user wishing to accept, decline on "tentatively accept" an event, without relying on features described above, would have to:

* download the invite file (usually `invite.ics`) ;
* generate a reply from this file, for example through `./icalendar-response -r accept -s replier-email@somedomain.com -i ~/Downloads/invite.ics -o ~/Downloads/invite.ics` ;
* attach the generated file to an email replying to the invitation.

This software is made to handle the most common cases. I chose to writing a short portable file with no external dependencies over comprehensive compatibility.

Testing status :

* [x] Proton Calendar ;
* [x] Google Calendar ;
* [ ] Microsoft365.


