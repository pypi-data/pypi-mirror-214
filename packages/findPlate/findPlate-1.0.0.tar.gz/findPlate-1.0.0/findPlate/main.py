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


