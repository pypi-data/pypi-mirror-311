import csv

LOG_FILE='util-cli.log'
LOG_CATEGORY="UTILS_CLI"

def write_log(category:str,message:str,log_file:str=LOG_FILE)->None:
    with open(log_file,'a') as f:
        print("{}: {}".format(category,message),file=f, end='\n')

def write_csv_data(csv_file_path,data):
    with open(csv_file_path,'a') as f:
        csv_h=csv.writer(f,doublequote=False)
        csv_h.writerows(data)