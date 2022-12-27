
import requests
import json
SYNONYMS_URL = "https://synonymord.se/api/?q={word}"

def set_up_list():
    output_file = "words.txt"
    input_file = "svenska-ord.txt"
    with open(input_file, "r") as input:
        with open(output_file, "w") as output:
            for line in input:
                word = line.strip()
                if word != "":
                    r = requests.get(SYNONYMS_URL.format(word=word))
                    res_json = json.loads((r.text.strip())[1:])
                    if res_json["synonyms"]:
                        print(word)
                        output.write(word + "\n")
    print("Done")
                    
            
set_up_list()