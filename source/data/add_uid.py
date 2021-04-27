import uuid
import json 

def main():
    with open("./sat-data.json", "r", encoding="utf8") as json_file:
        satdata = json.load(json_file)
        for sat in satdata[1:]:
            sat['uid'] = str(uuid.uuid4())
    with open('./sat-data.json', 'w', encoding='utf-8') as f:
        json.dump(satdata, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()