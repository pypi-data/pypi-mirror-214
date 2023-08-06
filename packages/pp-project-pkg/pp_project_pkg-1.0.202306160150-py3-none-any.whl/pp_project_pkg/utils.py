import wml.visionml as wv
import datetime
import mb.pandas as pd

__all__ = ['site_date_res','check_if_valid_date']


def site_date_res(site_id= 30607):
    """
    Get the site date report closure data
    Args:
        site_id : Site id for fetching the date wise result. Site_id : 30607 (Waldof)
    
    Returns:
        pd.DateFrame
    """
    q1 = """
    select s.start_date,s.id,s.meal_service_state, s.closed,s.updated from pp_meal_service.view_current_state cs
               join pp_meal_service.view_service s on s.view_current_state_id = cs.id
		       where cs.site_id = {} 
               """.format(site_id)
    return wv.read_sql(q1,wv.ml_engine)

def check_if_valid_date(site_res, date):
    """
    Check if the date (str) has closed the report.

    Args:
        site_res: complete report of the site_data_res
        date: string value of date. format : '2023-06-06'
    
    Output:
        Bool
    """

    k =datetime.datetime.strptime(date,'%Y-%m-%d').date()
    l = site_res[site_res['start_date']==k]
    
    l_d = l['closed'].iloc[0]
    
    if pd.isnull(l_d):
        return False
    
    if  (l_d).to_pydatetime().date() < k:
        return False
    
    return True

def create_date_table(start_date='2023-06-06', end_date='2023-12-31'):
    """
    Creates a date table with the start_date and end_date as the range.
    Args:
        start_date: start date of the date table. format : '2023-06-06'
        end_date: end date of the date table. format : '2023-06-06'
    Output:
        pd.DataFrame
    """    
    date_index = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame({'datetime': date_index.date,'closed':None})
    return df

def check_if_valid_dates(site_res,start_date='2023-06-06', end_date='2023-12-31'):
    """
    Check if the dates has closed the report.

    Args:
        site_res: complete report of the site_data_res
        date: string value of date. format : '2023-06-06'.
        today: string value of today's date. format : '2023-06-06'
    Output:
        df : pd.DataFrame
    """
    
    create_date_table_res = create_date_table(start_date=start_date,end_date=end_date)
    site_res_date = site_res[['start_date','closed','meal_service_state']]
    today = datetime.datetime.today().date()
    start_date =datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    site_res_date_new = site_res_date[(site_res_date['start_date']<=today) & (site_res_date['start_date']>=start_date) & 
                                      (site_res_date['meal_service_state']=='REPORT')]
    for i in range(len(site_res_date_new)):
        k = site_res_date_new.iloc[i]['start_date']
        l = site_res_date_new.iloc[i]['closed']
        if l is not None or l is not pd.NaT:
            l = l.to_pydatetime().date()
        else:
            l = None
        create_date_table_res.loc[create_date_table_res['datetime']==k,'closed']=l
    return create_date_table_res