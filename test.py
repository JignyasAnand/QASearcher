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
import pickle

# data={1:"Hello this is a test"}
f=open("qanda.txt", "rb")
t=pickle.load(f)
print(t)
# pickle.dump(data, f)
