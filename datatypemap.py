# datatypemap.py
#import random
#import rando as r

primaryCustomerColumns = ['customer_id','name_prefix','name_first','name_last','gender','email',
'account_status','addr_ln_1_txt','city','state','postal_code','birth_dt','employment','job_title','phone','dtUpdateDate']

secondaryCustomerColumns = [
['customer_id','name_prefix','name_first','name_last','gender','email','account_status',
'addr_ln_1_txt','city','state','postal_code','birth_dt','employment','job_title','phone','dtUpdateDate']
]

transColumnData = ['customer_id','orderid','purchasedate','transactiontotal','pointsearned','numberofitems',
'avgitemprice','productcode','productcategory','storeorwebid']

lmsColumns = ['lm_id','name_first','name_last','email','gender','address1','city','state',
'postal_code', 'birthdate','created','phone','points','current_tier','lmProgramName','dtUpdateDate']

emailColumns = ['EVENT_ID','EVENT_TYPE_ID', 'ACCOUNT_ID', 'LIST_ID', 'CUSTOMER_ID', 'EVENT_CAPTURED_DT', 
'EVENT_STORED_DT', 'CAMPAIGN_ID', 'LAUNCH_ID', 'EMAIL', 'EMAIL_FORMAT', 'MESSAGE_SIZE', 'LAUNCH_DATE','dtUpdateDate']

clickstreamColumns = ['cust_visid','daily_visitor','hit_time_gmt','page_url','campaign','ip','first_hit_time_gmt','last_hit_time_gmt',
'evar1','evar11','user_agent','referrer','product_list','uuid','dtUpdateDate']

mobileColumns = ['email','time_on_page','page','client_ip','login_time','sha','device_uuid','dtUpdateDate']

wifiColumns = ['email', 'fname', 'lname', 'roomOrStoreID', 'postal_code', 'client_ip',
'login_time','sha','device_uuid','dtUpdateDate']

safetyReportColumns = ['customer_id','ReportTimestamp', 'ReportType', 'ReportPriority', 'Description']

tiledataReportColumns = ['customer_id','TileTimestamp', 'TileType', 'TileLocation']