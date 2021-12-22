import pandas as pd
import numpy as np

def eliminate_provider(df_cap, df_conn , prov):
    """
    Eliminate a Provider from the problem. 

    """
    # Eliminate Provider in capacities data frame
    df_cap = df_cap[~df_cap['NodeName'].isin(prov)].copy(deep = True).reset_index(drop = True)

    # Eliminate Provider in connections data frame
    df_conn = df_conn[~((df_conn['StartNode'].isin(prov)) | (df_conn['EndNode'].isin(prov)))].copy(deep = True).reset_index(drop = True)

    return df_cap, df_conn

def adjust_umbalance_problem(df_cap, df_conn, cap_prov, cap_client ):
    """
    Add node to problem.
    """

    if cap_prov > cap_client:

        # Add additional demand client
        print(" Problem is imbalanced, the supply is higher than the demand")
        print(" Adding artifical Client that absorbs extra supply")

        node_name = 'Cliente Add'

        add_node = pd.DataFrame({'NodeIndex': [df_cap.index[-1] +1],
                            'NodeName': [node_name], 
                            'Capacity': [abs(cap_prov - cap_client) ]})

        #print(add_node)

        df_cap = pd.concat([df_cap,add_node ], ignore_index = True)

        
        # add additional connections
        df_conn_add = pd.DataFrame()
        df_conn_add['StartNode'] = df_conn['StartNode'].unique()
        df_conn_add['EndNode'] = node_name
        df_conn_add['Distance'] = 0
        df_conn_add['Cost'] = 0

        df_conn = pd.concat([df_conn, df_conn_add ], ignore_index = True)

    elif cap_prov < cap_client:

        # Add additional demand client
        print(" Problem is imbalanced the demand is higher than the supply")
        print(" Adding artifical Provider that delivers missing supply")

        node_name = 'Prov Add'

        add_node = pd.DataFrame({'NodeIndex': [df_cap.index[-1] +1],
                            'NodeName': [node_name], 
                            'Capacity': [abs(cap_prov - cap_client)] })

        df_cap = pd.concat([df_cap,add_node ], ignore_index = True)

        
        # add additional connections
        df_conn_add = pd.DataFrame()
        df_conn_add['EndNode'] = df_conn['EndNode'].unique()
        df_conn_add['StartNode'] = node_name
        df_conn_add['Distance'] = 0
        df_conn_add['Cost'] = 0

        df_conn = pd.concat([df_conn, df_conn_add ], ignore_index = True)
    
    else: 
        print(" Problem is balanced")



    return df_cap, df_conn


def strip_col(_df, cols):
    """
    Strip leading and trailing spaces in a 
    str column. 
    """

    for col in cols:
        _df.loc[:,col] = _df[col].str.strip()

    return _df

