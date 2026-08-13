customers_string = '''
id,first_name,last_name,email,gender,ip_address
1,Rania,Andrichuk,randrichuk0@sina.com.cn,Female,126.245.12.84
2,Leola,O'Carroll,locarroll1@yahoo.co.jp,Female,227.67.176.74
3,Libbi,Stanner,lstanner2@bing.com,Female,198.53.118.19
4,Tracey,Caldeiro,tcaldeiro3@loc.gov,Male,4.214.3.211
5,Marnia,Beesley,mbeesley4@google.com,Female,2.52.219.173
6,Norry,Dalzell,ndalzell5@goo.ne.jp,Female,131.35.31.168
7,Clementius,Shipway,cshipway6@baidu.com,Male,51.143.228.172
8,Diena,Dymoke,ddymoke7@nature.com,Female,132.80.141.247
9,Maribelle,Hedworth,mhedworth8@qq.com,Female,229.72.101.234
10,Lindsy,Sire,lsire9@nifty.com,Female,25.235.88.187
'''

#convert to List[List[Str]]

def convert_str_list(string):
    result_list = [line.strip().split(',') for line in string.strip().split('\n')]
    print(type(result_list))
    return result_list

list1 = convert_str_list(customers_string)
print(list1)

#list2 = customers_dict -> List[dict]
def convert_list_dict(string):
    result_list = []
    headers = None
    for i, line in enumerate(string.strip().split('\n')):
        values = line.strip().split(',')
        if i == 0:
            headers = values 
        else:
            row_dict = {}
            for j in range(len(headers)):
                row_dict[headers[j]] = values[j]
            result_list.append(row_dict)
    print(type(result_list))
    return result_list

list2 = convert_list_dict(customers_string)
print(list2)

#list3 = customers_dict -> dict[dict]
def convert_list_dict_to_dict(list_of_dicts):
    result_dict = {}
    for item in list_of_dicts:
        result_dict[item['id']] = item
    print(type(result_dict))    
    return result_dict

list3 = convert_list_dict_to_dict(list2)
print(list3)
