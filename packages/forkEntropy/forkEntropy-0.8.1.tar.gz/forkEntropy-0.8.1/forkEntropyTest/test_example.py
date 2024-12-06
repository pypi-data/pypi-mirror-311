'''
  导包区
'''
from functools import reduce
import glob
import pandas as pd
from forkEntropy.ForkEntropy import load_commitInfo_to_json, _calculate_process

def main():
    root_path = "test/testData\downloaded_PRrawdata\*.json"
    repos_json = glob.glob(root_path)
    replenishedCon = "test/testData\commitChanges\*.json"
    replenishedCon =  glob.glob(replenishedCon)

    results = []
    for k, repo_json in enumerate(repos_json):
        print(repo_json)
        rpCommitInfo = load_commitInfo_to_json(replenishedCon[k])
        df = pd.read_json(repo_json)
        df['created_at'] = pd.to_datetime(df['created_at'])
        monthly_groups = df.groupby(pd.Grouper(key='created_at', freq='M')).agg({
            'id': lambda x: list(x),
            'state': lambda x: list(x),
            'author': lambda x: list(x),
            'commits': lambda x: list(x)
        }).reset_index()

        repo_id = repo_json.split(".")[0].split(f"\\")[-1]
        for _, monthly_data in monthly_groups.iterrows():
            fileNum, forkNum, fork_div = _calculate_process(monthly_data, rpCommitInfo)
            # 将变量补充到字典中
            results.append({
                'repo_id': repo_id,
                'fileNum': fileNum,
                'forkNum': forkNum,
                'fork_div': fork_div,
            })

    results_df = pd.DataFrame(results)
    print(results_df)
    results_df.to_csv('./testResult/output_.csv', index=False)