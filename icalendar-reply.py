#!/usr/bin/python3
#   Copyright (C) 2023 Piotr Chmielnicki
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import sys
import os
import getopt

def usage():
    sys.stderr.write("Usage: icalendar-response.py -r {accept|tentative|decline} -s responder@email [-i input-file] [-o output-file]\n")
    status = -1
    if hasattr(os, "EX_USAGE"):
        status = os.EX_USAGE
    sys.exit(status)

def error(msg, fatal = False):
    if fatal:
        template = "Fatal error: {msg}.\n"
    else:
        template = "Error: {msg}.\n"
    sys.stderr.write(template.format(msg=msg))
    status = -1
    if hasattr(os, "EX_SOFTWARE"):
        status = os.EX_SOFTWARE
    if fatal:
        sys.exit(status)

def parseArgs():
    response = None
    sender = None
    infile = None
    outfile = None
    try:
        opts, unparsed = getopt.getopt(sys.argv[1:], "r:s:i:o:")
    except getopt.GetoptError:
        usage()
    if len(unparsed) != 0:
        usage()
    seenOptions = []
    for option, value in opts:
        if option in seenOptions:
            usage()
        seenOptions.append(option)
    for option, value in opts:
        if option == "-r":
            response = value
        if option == "-s":
            sender = value
        if option == "-i" and value != "-":
            infile = value
        if option == "-o" and value != '-':
            outfile = value
    if response is None or sender is None:
        usage()
    if response not in ["accept", "tentative", "decline"]:
        usage()
    return response, sender, infile, outfile

def readInput(infile = None):
    if infile is not None:
        f = open(infile, "r", encoding="utf-8")
    else:
        f = sys.stdin
    ret = ""
    while True:
        buff = f.read()
        if len(buff) == 0:
            break
        ret += buff
    if infile is not None:
        f.close()
    return ret

def writeOutput(output, outfile = None):
    if outfile is not None:
        f = open(outfile, "w", encoding="utf-8")
    else:
        f = sys.stdout
    if f.write(output) != len(output): # I d'ont know how this could happen
        error("unusual write error", fatal = True)
    if outfile is not None:
        f.close()

def generateResponse(invite, response, sender):
    template = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:piotrcki/icalendar-reply
METHOD:REPLY
BEGIN:VEVENT
{uid}
{dtstart}
{dtend}
ATTENDEE;PARTSTAT={status}:mailto:{sender}
END:VEVENT
END:VCALENDAR
""".replace("\n", "\r\n")
    status = {"accept" : "ACCEPTED",
                "tentative" : "TENTATIVE",
                "decline" : "DECLINED"}[response]
    lines = invite.splitlines()
    for prefix in ["UID:", "DTSTART;TZID=", "DTEND;TZID="]:
        count = 0
        for line in lines:
            if line.upper().find(prefix) == 0:
                count += 1
                if prefix == "UID:":
                    uid = line
                if prefix == "DTSTART;TZID=":
                    dtstart = line
                if prefix == "DTEND;TZID=":
                    dtend = line
        if count != 1:
            print("debug {} {}".format(prefix, count))
            error("unexepected inpur format", fatal = True)
    return template.format(uid = uid, dtstart = dtstart, dtend = dtend,
                           sender = sender, status = status)


if __name__ == "__main__":
    response, sender, infile, outfile = parseArgs()
    invite = readInput(infile)
    output = generateResponse(invite, response, sender)
    writeOutput(output, outfile)
