import urllib.parse

class UtilObj:
    def __init__(self, name):
        self.fname=name
    def change_fname(self, name):
        self.fname=name

    def getconts(self):
        arr=[]
        with open(f"{self.fname}", "r") as f:
            temp=f.readline()
            while temp:
                if temp=="\n":
                    temp=f.readline()
                    continue
                temp=temp.replace("\n","")
                arr.append(temp)
                temp=f.readline()
        return arr

    def getlinks(self):
        arr=self.getconts()
        link="https://www.google.com/search?q="
        for i in range(len(arr)):
            arr[i]=link+urllib.parse.quote(arr[i])
        return arr
        # print(urllib.parse.quote(arr[0]))

# getlinks()