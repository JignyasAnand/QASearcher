# import p_utils
#
# def gets():
#     res=p_utils.getconts()
#     dct={}
#     for i in enumerate(res):
#         dct[i[0]+1]=i[1]
#     print(dct)
#
# gets()
# import pickle
#
# # data={1:"Hello this is a test"}
import pickle
from collections import defaultdict
f=open("qanda.txt", "wb")
pickle.dump(defaultdict(str), f)

# t=pickle.load(f)
# print(t)
# # pickle.dump(data, f)


# stri="Key Differences Between JDBC and ODBC The most basic difference between JDBC and ODBC is that JDBC is language and platform dependent. On the other hand, the ODBC is language and platform independent. Java Database Connectivity is an acronym for JDBC, and on the other hand, Open Database Connectivity is an acronym for ODBC. The code for ODBC is complex and is hard to learn. However, the code for JDBC is simpler and easy to run. https://www.geeksforgeeks.org/difference-odbc-jdbc/,   http://www.google.com"
# import re
#
# def getURLs(string):
#     # findall() has been used
#     # with valid conditions for urls in string
#     regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
#     url = re.findall(regex, string)
#     if len(url)==0:
#         return ["No URLS found"]
#     return [x[0] for x in url]
# print(getURLs(stri))