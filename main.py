import argparse
import os
import json
import pandas as pd


def judge_paper(keywords, dict):
    for keyword in keywords:
        keyword = keyword.lower()
        if dict['abstract'] and keyword in dict['abstract']:
            dict['abstract'] = dict['abstract'].replace('\n', ' ')
            return True
        if dict['title'] and keyword in dict['title']:
            return True
    return False


def get_paper(keywords):
    root_dir = './literature'
    ret = []
    for c_name in os.listdir(root_dir):
        c_dir = os.path.join(root_dir, c_name)
        for json_name in os.listdir(c_dir):
            json_path = os.path.join(c_dir, json_name)
            reader = json.load(open(json_path))
            for paper_dict in reader:
                if judge_paper(keywords, paper_dict):
                    paper_dict['year'] = json_name[:4]
                    paper_dict['conference'] = c_name
                    ret.append(paper_dict)
    return ret

def main():

    keywords = ['sentiment analysis', 'aspect based sentiment analysis']
    ret = get_paper(keywords)
    df = pd.DataFrame(ret)
    df = df.sort_values(by=['year', 'conference'], ascending=False)
    df.to_csv('./results.csv', index=False, columns=['year', 'conference', 'title', 'url', 'abstract'])

if __name__ == '__main__':

    main()