# schedulebe (c) robipolli@gmail.com
# a postfix plugin for managing events in python
# License: GPL2
#
#
# this software 
# takes a mail from stdin
# check if it's a meeting request/reply
# get header from mail
# use them to make a POST request to bedework RTSVC

import vobject
import email

    
def getMeetingMethodFromMail(mail):
    """return the ics from email"""
    """ TODO http://docs.python.org/library/email.html#module-email"""
    return meeting

def getOrganizerHeaderFromMail(mail):
    organizer = "me@gmail.com"
    return organizer

def getRecipientsFromMail(mail):
    recipients = ["one@example.com","two@exmaple.com"]
    return recipients

def sendRequestToBedework(organizer, recipients, meeting):        
    """send a POST request to RTSVC url, setting    """
    """    Header: originator: me@gmail.com         """
    """    Header: recipient:  one@example.com      """
    """    Header: recipient:  two@example.com      """
    """    Header: Content-type: text/calendar      """
    """    .ics as POST body                        """
    rtsvcUrl = "example.com:8080/pubcaldav/rtsvc"
    rtsvcUser = "pippo"
    rtsvcPass = "pluto"
    return True

def __notifyUpdate(isError):
    """notify the user that bedework has been nicely updated"""
    if isError:
        return False
    
    return True

def __checkOrganizer(organizer):
    """check if organizer is an user of the platform"""

    return True

def main():
    meeting = getMeetingMethodFromMail(mail)
    if (meeting == None):
        return False
        
    organizer = getOrganizerHeaderFromMail(mail)
    recipients = getRecipientsFromMail(mail)
    
    if (__checkOrganizer(organizer)):
        if (sendRequestToBedework(organizer, recipients, meeting)):
            return True
        
    return False
    
        
    
    
    