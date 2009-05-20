# schedulebe (c) robipolli@gmail.com
# a postfix plugin for managing events in python
# License: GPL2
#
#
# this software manage mail meeting invitation, 
# notifying to  bedework  
# *  meeting request to bedework users
# *  meeting replies    
# takes a mail from stdin
# check if it's a meeting request/reply
# get header from mail
# use them to make a POST request to bedework RTSVC
#


import vobject
import email, httplib
import re
import pycurl

debug = True
rtsvcUrl = "http://rtsvc.example.org:28080/pubcaldav/rtsvc"
rtsvcUser = "pippo"
rtsvcPass = "pluto"

class Meeting():

    def __init__(self):
        self.ics = None
        self.method = None
        self.organizer = None
        self.attendees = []
        
        self.sender = None
        self.recipient = None
        
    def setMail(self, mailMessage):
        self.walkMail(mailMessage)
                               
    def getMethod(self):
        return self.ics.method.value
    
    def getOrganizer(self):
        # TODO check organizer ~= /mailto:/
        o =  cleanMailAddress(self.ics.vevent.organizer.value) 
        return o
    
    def getAttendees(self):
        if len(self.attendees) == 0:
            for a in self.ics.vevent.__getattr__("attendee_list"):
                self.attendees.append(cleanMailAddress(a.value))
                
        return self.attendees

    def validate(self):
        
        if self.getMethod() == "REQUEST":
            #mail recipient must be internal and in attendees
            # in a meeting request, organizer is the mail sender
            if self.getOrganizer() != self.sender:
                return False
            
        elif getMethod() == "REPLY":
            #the sender mail should be one of the attendees
            if not self.sender in self.getAttendees():
                return False
            
        else:
            return False 

        # check that organizer is valid
        if not __checkOrganizer(self.getOrganizer()):
            return False
   
    def walkMail(self, mailMessage):
        """walk thru the mail looking for calendar attachment"""
        """parse attachment and set meeting.ics"""
        
        self.recipient = cleanMailAddress(mailMessage['To'])
        self.sender = cleanMailAddress(mailMessage['From'])
    
        mailWalker = mailMessage.walk()
        #print "elements: %d" %  countEnum(mailMessage.walk())
        for i in mailWalker:
                if i.get_content_type() == "text/calendar": 
                    if self != None:  
                        icalendar = vobject.readOne(i.get_payload(decode=True))
                        self.ics = icalendar
                    else:
                        print "Test case: %s" % i.get_payload(decode=True)
#        try:
#            for i in mailWalker:
#                if i.get_content_type() == "text/calendar": 
#                    if meeting != None:  
#                        icalendar = vobject.readOne(i.get_payload(decode=True))
#                        self.ics = icalendar
#                    else:
#                        print "Test case: %s" % i.get_payload(decode=True)
#        except ParseError:
#            print "Error while parsing calendar"
#            raise           
        
         
#end class
        
        
def getMeetingInfo(meeting):
    """get meeting info """
    """ TODO http://docs.python.org/library/email.html#module-email"""
    meeting.method = meeting.ics.method.value
    meeting.organizer = meeting
    return meeting.method.value



def cleanMailAddress(mailaddress):
    """clean the mail address returning a string value (no unicode)"""
    s = re.compile('^.*<(.+)>.*',re.IGNORECASE).sub(r'\1', mailaddress)
    s = re.compile('mailto:',re.IGNORECASE).sub(r'', s)
    return str(s.lower())
    
def getRecipientsFromMail(mail):
    """get the TO Header from the email"""
    recipients = ["one@example.com","two@exmaple.com"]
    recipient = mail['To']
    return recipients

def sendRequestToBedework(meeting):        
    """send a POST request to RTSVC url, setting    """
    """    Header: originator: me@gmail.com         """
    """    Header: recipient:  one@example.com      """
    """    Header: recipient:  two@example.com      """
    """    Header: Content-type: text/calendar      """
    """    .ics as POST body                        """
    rtsvcHeader = [ 'Content-Type:text/calendar; charset=UTF-8' ]
    rtsvcHeader.append('originator: ' + meeting.getOrganizer())
    
    for a in meeting.getAttendees():
        rtsvcHeader.append('recipient: ' + a)    
                
    c = pycurl.Curl()
 
    if debug:
        print "debug" + meeting.ics.serialize()
        c.setopt(c.VERBOSE, 1)
        for a in rtsvcHeader: print a

    c.setopt(c.HTTPHEADER, rtsvcHeader)   
    c.setopt(c.POSTFIELDS, meeting.ics.serialize())
    c.setopt(c.URL, rtsvcUrl)
    c.setopt(c.HEADER, 1)
    c.setopt(c.POST, 1)
    c.perform()
    return True

def __notifyUpdate(isError):
    """notify the user that bedework has been nicely updated"""
    if isError:
        return False
    
    return True

def __checkOrganizer(organizer):
    """check if organizer is an user of the platform"""

    return True

def countEnum(i):
    tot=0
    for j in i:
        tot = tot+1
    return tot


        

def main():
    m = Meeting()
    m.setMail( email.message_from_string(open("invito.mbox").read()))
    
        
    organizer = m.getOrganizer()
    recipients = m.getAttendees()
    
    print """o:%s\na:%s""" , (organizer, recipients)
    
    if (__checkOrganizer(organizer)):
        if (sendRequestToBedework(organizer, recipients, meeting)):
            return True
        
    return False
    
        


    
    