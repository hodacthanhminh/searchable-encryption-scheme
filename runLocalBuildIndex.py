# libs
import pandas as pd
import json
# se scheme
from genkey import genkey
from buildindex import BuildIndex


def genSearhFile(df):
    count = 0
    while len(df) > 0:
        export_df = df[:10]
        df = df[10:]
        count += 1
        data = {'id': 'search{}'.format(count), 'Data': export_df.to_json(orient='records')}
        with open('./local/search/search-{}.json'.format(count), 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))


def genDocFile(df):
    for i in df.index:
        df.loc[i].to_json("./local/email/{}.json".format(df.loc[i]['ID']))


if __name__ == "__main__":
    emails_df = pd.read_json("./export_json.json")
    buildindex = BuildIndex(genkey.readFile())
    number_of_file = int(input("Enter number of file:"))
    random_df = emails_df.sample(n=number_of_file)
    genDocFile(random_df)
    random_df['encrypt_index'] = list(map(buildindex.main, random_df['keyword']))
    total_export_df = pd.concat([random_df["ID"], random_df["encrypt_index"]],
                                keys=['file', 'encrypt_index'], axis=1)
    genSearhFile(total_export_df)
