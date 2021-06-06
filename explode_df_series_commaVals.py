### SOURCE == https://stackoverflow.com/questions/12680754/split-explode-pandas-dataframe-string-entry-to-separate-rows


import pandas as pd 
import numpy as np

#df_explode = pd.read_csv("explode_df.csv",index_col = [0]) 
# if we want the ID Column to be the INDEX COL 
df_explode = pd.read_csv("explode_df.csv") 
print(df_explode)

def explode(df, lst_cols, fill_value='', preserve_index=False):
    # make sure `lst_cols` is list-alike
    print(type(lst_cols))
    #
    if (lst_cols is not None
        and len(lst_cols) > 0
        and not isinstance(lst_cols, (list, tuple, np.ndarray, pd.Series))):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols) # Built in Method set.difference(another_set)
    print(idx_cols) ## all columns except `lst_cols`
    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()
    print("--lens--------\n",lens)
    lens_1 = df[lst_cols[1]].str.len()
    print("--lens_1--------\n",lens_1)
    # preserve original index values    
    idx = np.repeat(df.index.values, lens)
    print("--len(idx)--------\n",len(idx)) # 39 = 13+13+13
    print("--idx--------\n",idx)

    for col in idx_cols:
        test_col = np.repeat(df[col].values, lens)
        print("--test_col--------\n",test_col)

    # create "exploded" DF
    res = (pd.DataFrame({
                col:np.repeat(df[col].values, lens)
                for col in idx_cols},
                index=idx)
             .assign(**{col:np.concatenate(df.loc[lens>0, col].values)
                            for col in lst_cols}))
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = (res.append(df.loc[lens==0, idx_cols], sort=False)
                  .fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:        
        res = res.reset_index(drop=True)
    return res


lst_cols = ["int_col", "text_col"]
result_explode = explode(df_explode,lst_cols , fill_value='', preserve_index=False)  
print(result_explode)  