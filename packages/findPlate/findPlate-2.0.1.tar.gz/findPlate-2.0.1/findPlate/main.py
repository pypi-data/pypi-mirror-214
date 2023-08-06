import pandas as pd

def gjej_shoferin(path):
    tagra = input("Vendosni targen:")
    df = pd.read_excel(path)
    df = df[(df.targa == tagra)]
    if len(df) > 0:
        mgs = f"""
Targa {tagra} i perket personit {df.iloc[0]['emri']} {df.iloc[0]['mbiemri']} me NID {df.iloc[0]['id']}
        """
    else:
        mgs = "Traga nuk ekziston ne listen e targave"
    print(mgs)

def gjej_shoferin_by_name(path):
    emri = input("Vendosni emrin:")
    mbiemri = input("Vendosni mbiemrin:")
    df = pd.read_excel(path)
    df = df[(df.emri == emri) & (df.mbiemri == mbiemri)]
    if len(df) > 0:
        mgs = f"""
Personit {df.iloc[0]['emri']} {df.iloc[0]['mbiemri']} me NID {df.iloc[0]['id']} zoteron targen {df.iloc[0]['targa']}
        """
    else:
        mgs = "Personi nuk ekziston ne listen e targave"
    print(mgs)

