#!/usr/bin/env python3
import sys
import os
import re
import dateparser


def fix_whatsapp(f):

    pattern = re.compile(r"IMG-([0-9]+)-WA[0-9]+")
    match = re.match(pattern, f)
    if match is None or match.group(1) is None:
        continue
    date = dateparser.parse(match.group(1), date_formats=["%Y%m%d"])
    print("Parsed date for file=%s date=%s" % (f, date))
    if date is None:
        print("Couldn't parse date for file=%s" % f)
        continue

    date = "{0}:{1}:{2} {3}:{4}:{5}".format(
        date.year, date.month, date.day, date.hour, date.minute, date.second
    )
    cmd = 'exiftool -overwrite_original "-AllDates={0}" "{1}"'.format(date, f)
    print("Fixing with command=%s" % cmd)
    os.system(cmd)

    date = "{0}/{1}/{2} {3}:{4}:{5}".format(
        date.year, date.month, date.day, date.hour, date.minute, date.second
    )
    cmd = 'SetFile -m  "{0}" "{1}"'.format(date, f)
    print("Fixing with command=%s" % cmd)
    os.system(cmd)


for root in sys.argv[1:]:
    for curr_dir, dirs, files in os.walk(root):
        for file in files:
            fix_whatsapp(os.path.basename(curr_dir + os.sep + file))
