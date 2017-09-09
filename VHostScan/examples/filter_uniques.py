import pandas as pd


# fake dataset for testing
results=[
'v3.id.au, 9134060d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11',
'v3, 9134060d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11',
'alpha, 9134060d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11',
'alpha.id.au, 9134060d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11',
'bull, BBB60d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11',
'cow, BBB60d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11',
'mouse, AAA60d56ae7533205eda46c59f7372af81e92921fa7ad3d569cbdddb6b3e11']

def show_uniques(count,results):
    #key=[]
    #val=[]
    #uniq=[]
    d={}
    for item in results:
        r=item.split(",")
        d[r[0]]=r[1]
    df= pd.DataFrame([[key, value] for key, value in d.items()], columns=["key_col", "val_col"])
    #print(df)
    d=df.groupby("val_col").filter(lambda x: len(x) <= count)
    #print(d)
    res=((d["key_col"].values).tolist())

    return res


#returns a list with values matching the condition of static count (intended flag in application)
e=show_uniques(3,results)
print(e)