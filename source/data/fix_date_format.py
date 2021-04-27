import datetime
import json 

def serial_date_to_string(srl_no):
    new_date = datetime.datetime(1900,1,1,0,0) + datetime.timedelta(srl_no - 2)
    return new_date.strftime("%d-%m-%Y")

def main():
    with open("./sat-data.json", "r", encoding="utf8") as json_file:
        satdata = json.load(json_file)
        for sat in satdata[1:]:
            if sat['T'] == '':
                continue
            sat['T'] = serial_date_to_string(int(sat['T']))
    with open('./sat-data.json', 'w', encoding='utf-8') as f:
        json.dump(satdata, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()