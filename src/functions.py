import numpy as np

def get_pareto(df):
    df_pareto = df.copy()
    df_pareto["cumulative_revenue"]=df_pareto["revenue"].cumsum()
    df_pareto["cumulative_pct"]=df_pareto["cumulative_revenue"]/df_pareto["revenue"].sum()*100
    df_pareto["variable_pct"]=range(1,len(df_pareto)+1)
    df_pareto["variable_pct"]=df_pareto["variable_pct"]/len(df_pareto)*100

    pareto_point = df_pareto[df_pareto["cumulative_pct"]>=80].iloc[0]
    pareto_revenue = df_pareto[df_pareto["variable_pct"] <= pareto_point["variable_pct"]]["revenue"].min()
    pareto_variable_pct = pareto_point["variable_pct"]

    return(pareto_point,pareto_revenue, pareto_variable_pct)


def gini(array):
    array = np.sort(array)  
    n = len(array)
    index = np.arange(1, n + 1)
    return 2 * np.sum(index * array) / (n * np.sum(array)) - (n + 1) / n


def segment_customer(row):
    r, f, m = row['R_score'], row['F_score'], row['M_score']
    if r>=4 and f>=4 and m>=4:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'New Customers'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r <= 2 and f <= 2:
        return 'Lost'
    else:
        return 'Potential Loyalists'