import pandas as pd
import os 

def MaASLin2_filtered_features(data_path):
    data = pd.read_csv(data_path, sep='\t')
    results = pd.DataFrame()
    significant_features = data['feature'].tolist()
    results['Feature'] = [format_feature(feature) for feature in significant_features]
    results['Rank'] = range(1, len(significant_features) + 1)
    return results

def ANCOM_filtered_features(data_path):
    data = pd.read_csv(data_path, sep=',')
    results = pd.DataFrame()
    significant_features = data.loc[1:,'Percentile'].tolist()
    results['Feature'] = significant_features
    results['Rank'] = range(1, len(significant_features) + 1)
    return results  

def intersecate_MaAsLin_ANCOM(data_frame_MaAsLin, data_frame_ANCOM, path_output):
    # Compute intersection and union
    intersection = set(data_frame_MaAsLin['Feature']) & set(data_frame_ANCOM['Feature'])
    union = set(data_frame_MaAsLin['Feature']) | set(data_frame_ANCOM['Feature'])
    missing_rank_placeholder = max(len(union), 99999)
    # Prepare the results dataframe
    results = pd.DataFrame(list(union), columns=['Union'])
    # results['ANCOM'] = results['Union'].apply(lambda x: x if x in data_frame_ANCOM['Feature'].values else '-')
    results['ANCOM rank'] = results['Union'].apply(lambda x: data_frame_ANCOM[data_frame_ANCOM['Feature'] == x]['Rank'].values[0] if x in data_frame_ANCOM['Feature'].values else missing_rank_placeholder)
    # results['MaAsLin'] = results['Union'].apply(lambda x: x if x in data_frame_MaAsLin['Feature'].values else '-')
    results['MaAsLin rank'] = results['Union'].apply(lambda x: data_frame_MaAsLin[data_frame_MaAsLin['Feature'] == x]['Rank'].values[0] if x in data_frame_MaAsLin['Feature'].values else '-')
    results['Intersection'] = results['Union'].apply(lambda x: 'True' if x in intersection else 'False')
    print(results.head())
    results = results.sort_values(by=['ANCOM rank'], ascending=True)
    results['ANCOM rank'] = results['ANCOM rank'].replace(missing_rank_placeholder, '-')
    os.makedirs(os.path.dirname(path_output), exist_ok=True)
    results.to_csv(path_output, sep=',', index=False)

def format_feature(feature):
    new = feature.replace('.',';').replace(';;', '];').replace('_;','_[')
    if new.endswith(';'):
        new = new[:-1] + ']'
    return new
    