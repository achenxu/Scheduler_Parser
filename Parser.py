from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    starts = []
    data = []
    toIgnore = ['CRN', 'Course #', 'Course Title', 'Units', 'Actv', 'Days', 'Time', 'Bldg/Rm', 'Start - End', 'Instructor', 'Max Enrl', 'Act Enrl', 'Seats Avail', 'Skip to top of page', 'Search Courses']
    passes = 0
    
    def handle_starttag(self, tag, attrs):
        self.starts.append(tag)
    
    def handle_endtag(self, tag):
        self.starts.pop()
    
    def handle_data(self, data):
        if len(self.starts) < 1:
            return
        if data in self.toIgnore:
            return

        if self.starts[len(self.starts) - 1] == 'h3':
            if data == "&":
                self.data[len(self.data)-1][0] = self.data[len(self.data)-1][0] + data
                self.passes = 1
            else:
                if self.passes == 0:
                    self.data.append(["startsubject", "separator"])
                    self.data.append([data, "subject"])
                else:
                    self.data[len(self.data)-1][0] = self.data[len(self.data)-1][0] + data
                    self.passes -= 1
        
        if self.starts[len(self.starts) - 1] == 'a':
            self.data.append(["startcourse", "separator"])
            self.data.append([data, "crn"])

        if self.starts[len(self.starts) - 1] == 'small':
            if data == "&":
                self.data[len(self.data)-1][0] = self.data[len(self.data)-1][0] + data
                self.passes = 1
            else:
                if self.passes == 0:
                    self.data.append([data, "info"])
                else:
                    self.data[len(self.data)-1][0] = self.data[len(self.data)-1][0] + data
                    self.passes -= 1

parser = MyHTMLParser()
from urllib import urlopen
s = urlopen("https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm=202210&openclasses=N%22").read() # Extract from html file
parser.feed(s)                                  # Parse it into data elements (subject, crn, or info)

r = open("testfiles/result.csv", "w")

r.write("CRN/Class, Course ID, Course Name, Units, Type, Days, Hours, Room, Dates, Instructor, Capacity, Enrolled, Available, Type2, Days2, Hours2, Room2, Dates2, Type3, Days3, Hours3, Room3, Dates3\n")


column = 0
for info in parser.data:
    
    if info[1] == 'subject':
        r.write("\n" + info[0])
    
    if info[1] == 'crn':
        r.write("\n" + info[0])
        column = 0

    if info[1] == 'info':
        if column == 2:
            if len(info[0]) > 1:
                continue
        if column == 0:
            info[0] = info[0].replace(" ", "")
        r.write("," + info[0].replace(",", ""))
        column += 1
        if info[0] == "TBD-TBD":
            r.write(",")
            column += 1
r.close()



