ScheduleBe process mail replies to meeting requests, using Bedework Caldav Server and its real-time service scheduler.

It will be made as a python plugin for Postfix.

> # Scope #

A plug-in for processing mail containing ics attachment with MEETING REQUEST / REPLY. In that case, mail should be POST ed on Bedework with RTSVC

> # Environment #

A bedework server with RealTime Service working. www.bedework.org

> # Flow #
    1. parse the email
    1. strip .ics attachment
    1. eventually decode .ics attachment if base64 encoded
    1. check that it is a MEETING:REQUEST/REPLY
    1. get Sender and Recipient to set HTTP REQUEST Header
    1. make a POST REQUEST to Bedework RTSVC using Headers above
    1. use an async library to perform the POST REQUEST
    1. parse bedework response to check that all is ok