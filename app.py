from flask import Flask, render_template, flash, request, redirect, url_for
import p_utils
import webbrowser
import pickle
import re

fileoc="qanda.txt"

def getURLs(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    if len(url)==0:
        return ["No URLS found"]
    return [x[0] for x in url]


app=Flask(__name__, template_folder=r"/Users/jignyas/PycharmProjects/flaskProject3/templates")
app.secret_key="secret key"

def emp():
    return render_template("test.html")

@app.route('/open_all')
def open_tabs():
    arr=p_utils.getlinks()
    for i in arr:
        webbrowser.open(i)
    return "none"

@app.route("/")
def home():
    res=p_utils.getconts()
    ltemp=[i for i in range(1 ,len(res)+1)]
    links=p_utils.getlinks()
    f = open(fileoc, "rb")
    t = pickle.load(f)
    print(t)
    nansd=[]
    # nansd=[i for i in ltemp if i not in t]
    for i in ltemp:
        if (i not in t):
            nansd.append(i)
        elif t[i]=='' or t[i]==" " or list(set(t[i]))==" ":
            del t[i]
            nansd.append(i)
    print(nansd)
    temp=list(zip(ltemp, res, links))
    final=[]
    q=[i for i in t]

    final.append(temp)
    final.append(q)
    final.append(nansd)

    print(final[1])
    return render_template("index.html", conts=final, temps=request.remote_addr)

@app.route("/<num1>", methods=["POST", "GET"])
def ind(num1):
    if request.method=="GET":
        try:
            num1=int(num1)
            dct=gets()
            f = open(fileoc, "rb")
            t = pickle.load(f)

            try:
                t=t[num1].strip()
                # print(t)
            except:
                t=""
            urls=getURLs(t)

            pack=[num1, dct[num1], t, len(p_utils.getconts()), urls]
            return render_template("dispq.html", conts=pack)
        except:
            return redirect(url_for("home"))
    else:
        qid=request.form.get("qid")
        ans=request.form.get("tarea").strip()
        f = open(fileoc, "rb")
        t = pickle.load(f)
        t[int(qid)]=ans
        f.close()
        f = open(fileoc, "wb")
        pickle.dump(t, f)
        f.close()
        return redirect(url_for("ind", num1=qid))
# @app.route("/genlinks")
def gets():
    res=p_utils.getconts()
    dct={}
    for i in enumerate(res):
        dct[i[0]+1]=i[1]
    return dct
    # print(dct)
    # return render_template("test.html")



@app.route("/rets", methods=["POST"])
def rets():
    # print(request.form.get("tarea"))
    return redirect(url_for("ind", num1=request.form.get("qid")), code=307)



@app.route("/generate")
def gens():
    f = open(fileoc, "rb")
    t = pickle.load(f)
    ques=gets()
    nf=open("FINqa.txt" ,"w")
    for i in t:
        q="Q) "+ques[i]+"\n"
        ans="A) "+t[i]+"\n\n"
        nf.write(q)
        nf.write(ans)
    nf.close()
    return "Succesfully generated the text file. Check your directory."



if __name__ == '__main__':
    app.run(host="0.0.0.0")