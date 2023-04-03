from flask import Flask, render_template, request, redirect, url_for
import p_utils
import webbrowser
import pickle
import re
import os
from collections import defaultdict
from pdfcon import text_to_pdf
import s3b
import urllib.parse

p_util_obj=None
fileoc="qanda.txt"
qfile=""
qafile=""

def getURLs(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    if len(url)==0:
        return ["No URLS found"]
    return [x[0] for x in url]


app=Flask(__name__, template_folder=r"templates")
app.secret_key="secret key"


def emp():
    return render_template("test.html")

@app.route('/open_all')
def open_tabs():
    arr=p_util_obj.getlinks()
    for i in arr:
        webbrowser.open(i)
    return "none"

# @app.route("/", methods=["POST", "GET"])
# def temp():
#     if request.method=="GET":
#         return render_template("test.html")
#     else:
#         f=request.files["file"]
#         f.save(f.filename)
#         return "success"

@app.route("/", methods=["POST", "GET"])
def chooser():
    if request.method=="GET":
        files=s3b.getconts("QASFiles")
        conts=[files[1:]]
        return render_template("chooser.html", conts=conts)
    else:
        global fileoc, qfile,qafile,p_util_obj

        f=request.files.get("file")
        # f.save(f.filename)
        if f:
            qfile=f.filename
            print("Uploaded")
            f.save(f.filename)
        else:
            qfile = request.form["qfile"]
            s3b.download_file(qfile)

        qfile=qfile.split("QASFiles/")[-1]
        qafile = f"{qfile[:-4]}anda.txt"
        # qafile+="anda.txt"
        files2=s3b.getconts("QASF2")

        if "QASF2/"+qafile not in files2:
            f1 = open(qafile, "wb")
            pickle.dump(defaultdict(str), f1)
            f1.close()
        else:
            s3b.download_file(f"QASF2/{qafile}")

        fileoc=os.path.basename(qafile)
        p_util_obj = p_utils.UtilObj(os.path.basename(qfile))

        # p_util_obj.change_fname(os.path.basename(qfile))
        return redirect(url_for("home"))


@app.route("/home")
def home():
    res=p_util_obj.getconts()
    ltemp=[i for i in range(1 ,len(res)+1)]
    links=p_util_obj.getlinks()
    f = open(fileoc, "rb")
    try:
        t = pickle.load(f)
    except:
        f.close()
        f=open(fileoc, "wb")
        pickle.dump(defaultdict(str), f)
        f.close()
        f=open(fileoc, "rb")
        t=pickle.load(f)
    # print(t)
    nansd=[]
    # nansd=[i for i in ltemp if i not in t]
    for i in ltemp:
        if (i not in t):
            nansd.append(i)
        elif t[i]=='' or t[i]==" " or list(set(t[i]))==" ":
            del t[i]
            nansd.append(i)
    # print(nansd)
    temp=list(zip(ltemp, res, links))
    final=[]
    q=[i for i in t]

    final.append(temp)
    final.append(q)
    final.append(nansd)

    # print(final[1])
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
            link = p_util_obj.getlinks()[num1-1]
            print(link)
            pack=[num1, dct[num1], t, len(p_util_obj.getconts()), urls, link]
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
    res=p_util_obj.getconts()
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
        ans="A) \n"+t[i]+"\n\n"
        nf.write(q)
        nf.write(ans)
    nf.close()

    input_filename = 'FINqa.txt'
    output_filename = 'FinalAnswers.pdf'
    file = open(input_filename)
    text = file.read()
    file.close()
    # file:///C:/Users/jigny/PycharmProjects/QASF/FinalAnswers.pdf
    x=os.getcwd()
    x=x.replace("\\", "/")
    pdfp=f"file:///{x}/{output_filename}"
    print(pdfp)
    text_to_pdf(text, output_filename)
    return "Succesfully generated the files. Check your directory."

try:
    from .secret import BUCKET
except:
    from secret import BUCKET

@app.route("/update")
def update():
    global qafile, qfile

    if "QASFiles" not in qfile:
        qfile=f"QASFiles/{qfile}"
    if "QASF2" not in qafile:
        qafile=f"QASF2/{qafile}"
    s3b.upload_file(fileoc, BUCKET, qafile)
    s3b.upload_file(os.path.basename(qfile), BUCKET, qfile)
    return "Updated successfully"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)