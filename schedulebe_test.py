import random
import unittest

import schedulebe
from schedulebe import Meeting 
import email
import email.iterators
import pycurl
import vobject
from xml.parsers.expat import ExpatError

ATTENDEE = "attendee@mysite.edu"
ORGANIZER = "jdoe@example.com"
ORGANIZERI = "organizer@mysite.edu"

class TestScheduleBe(unittest.TestCase):

    def setUp(self):
        # load dummy data
        fp = open("inbound_meeting.mbox")
        self.meeting = Meeting()
        self.textmail = fp.read()
        self.msg = email.message_from_string(self.textmail)
        self.invalidMsg = email.message_from_string(open("invalid_meeting.mbox").read())
        self.msMsg = email.message_from_string(open("invito.outlook.mbox").read())
        #email.Iterators._structure(self.msg)
        #print self.msg

    def testWalkMail(self):
        for m in [ self.msg, self.msMsg ]:
            self.meeting.setMail(m)
        
    def testErrorOnInvalidMail(self):
        try:
            self.meeting.setMail(self.invalidMsg)
        except BaseException: 
            return True
        
        return False
        
    def testGetMeetingInfo(self):
        for m in [ self.msg, self.msMsg ]:
            self.meeting.setMail(m)
            method = self.meeting.getMethod()
            print "\nsender:%s\nrecipient: %s " % (self.meeting.sender, self.meeting.recipient)        
            try:
                assert method in ["REQUEST", "REPLY"]
                assert self.meeting.getOrganizer() == ORGANIZER
                assert ATTENDEE in  self.meeting.getAttendees()
            except AssertionError:
                print "organizer:", self.meeting.getOrganizer()
                print "attendees:", self.meeting.getAttendees()
                raise
            

    def testCleanMailAddress(self):
        """check that we can clean safely mail addresses"""
        for a in ["Pippo Pluyo<a@b.it>", 
                  "a@b.it", "'Aaa bbb'<a@b.it>", "<a@b.it>",
                  "mailto:a@b.it"]:
            assert schedulebe.cleanMailAddress(a) == "a@b.it"
                 
    def testPostToBedework(self):
        """try to make a post to bw"""
        
        self.meeting.setMail(self.msg)
        schedulebe.sendRequestToBedework(self.meeting)
       
    def testPostToBedeworkInternal(self):
        """try to make a post to bw"""
        mymsg = email.message_from_string(open("internal_meeting.mbox").read())

        self.meeting.setMail(mymsg)
        schedulebe.sendRequestToBedework(self.meeting) 
      
    def testIsLocalUser(self):
        """try to check if the user is local"""
	global ldapUrl
	global ldapCACertFile
	global ldapBaseDN
	global useLDAPs
	ldapUrl = "ldaps://hostname.domainname:636"
	ldapCACertFile = "/etc/ssl/ldap/cacert.pem"
	ldapBaseDN = "dc=yyy,dc=zz"
	useLDAPs = True
	for a in ["a@b.it","xxx@yyy.zz"]:
	    assert schedulebe.isLocalUser(a)

    def testParseResponse(self):
        response = """HTTP/1.1 100 Continue
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Content-Type: text/xml;charset=UTF-8
Content-Length: 365
Date: Mon, 25 May 2009 12:20:15 GMT

<?xml version="1.0" encoding="UTF-8" ?>

<ns1:schedule-response xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http://www.w3.org/2002/12/cal/ical#">
  <ns1:response>
    <ns1:recipient>
      <href>attendee@mysite.edu</href>
    </ns1:recipient>
    <ns1:request-status>2.0;Success</ns1:request-status>
  </ns1:response>
</ns1:schedule-response>"""
        

        responseMulti = """HTTP/1.1 100 Continue
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Content-Type: text/xml;charset=UTF-8
Content-Length: 365
Date: Mon, 25 May 2009 12:20:15 GMT

<?xml version="1.0" encoding="UTF-8" ?>

    <ns1:schedule-response xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http:
//www.w3.org/2002/12/cal/ical#">
  <ns1:response>
    <ns1:recipient>
      <href>aaa@example.com</href>
    </ns1:recipient>
    <ns1:request-status xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http
://www.w3.org/2002/12/cal/ical#">1.0;Deferred</ns1:request-status>
  </ns1:response>
  
  <ns1:response>
    <ns1:recipient>
      <href>bbb@mysite.edu</href>
    </ns1:recipient>
    <ns1:request-status xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http
://www.w3.org/2002/12/cal/ical#">2.0;Success</ns1:request-status>
  </ns1:response>
  
  <ns1:response>
    <ns1:recipient>
      <href>gmiatus@example.com</href>
    </ns1:recipient>
    <ns1:request-status xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http
://www.w3.org/2002/12/cal/ical#">1.0;Deferred</ns1:request-status>
  </ns1:response>
  
  <ns1:response>
    <ns1:recipient>
      <href>jdoe@example.com</href>
    </ns1:recipient>
    <ns1:request-status xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http
://www.w3.org/2002/12/cal/ical#">1.0;Deferred</ns1:request-status>
  </ns1:response>
  
  <ns1:response>
    <ns1:recipient>
      <href>rjannet@example.com</href>
    </ns1:recipient>
    <ns1:request-status xmlns="DAV:" xmlns:ns1="urn:ietf:params:xml:ns:caldav" xmlns:ns2="http
://www.w3.org/2002/12/cal/ical#">1.0;Deferred</ns1:request-status>
  </ns1:response>
</ns1:schedule-response>

"""

        assert schedulebe.parseResponse(response) == True
        assert schedulebe.parseResponse(responseMulti) == True

 
        
    def testScheduleRequestReply(self):
        mymsg = email.message_from_string(open("internal_meeting.mbox").read())
        self.meeting.setMail(mymsg)
        schedulebe.sendRequestToBedework(self.meeting)
        
        # create a reply:
        # - remove other attendees
        # - set rcpt to
        # - post
        self.meeting.sender = ATTENDEE
        self.meeting.ics.method.value = "REPLY" 
        self.meeting.ics.vevent.attendee = []
        attendee = self.meeting.ics.vevent.add("attendee")
        attendee.value = "mailto:" + ATTENDEE
        attendee.partstat_param="ACCEPTED"
        self.meeting.recipient.append(ORGANIZERI)
        print self.meeting.ics.serialize()
        schedulebe.sendRequestToBedework(self.meeting)
        
        
# main       
if __name__ == '__main__':
    unittest.main()
