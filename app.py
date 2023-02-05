from flask import Flask, render_template, flash, request, redirect, url_for
import p_utils
import webbrowser
import pickle


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
def empty():
    res=p_utils.getconts()
    ltemp=[i for i in range(1 ,len(res)+1)]
    links=p_utils.getlinks()
    ql=""
    final=list(zip(ltemp, res, links))

    return render_template("index.html", conts=final, temps=request.remote_addr)

@app.route("/<num1>", methods=["POST", "GET"])
def ind(num1):
    if request.method=="GET":
        try:
            num1=int(num1)
            dct=gets()
            f = open("qanda.txt", "rb")
            t = pickle.load(f)

            try:
                t=t[num1].strip()
                print(t)
            except:
                t=""

            pack=[num1, dct[num1], t, len(p_utils.getconts())]
            return render_template("dispq.html", conts=pack)
        except:
            return "Error. Try Again"
    else:
        qid=request.form.get("qid")
        ans=request.form.get("tarea").strip()
        f = open("qanda.txt", "rb")
        t = pickle.load(f)
        t[int(qid)]=ans
        f.close()
        f = open("qanda.txt", "wb")
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
    f = open("qanda.txt", "rb")
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