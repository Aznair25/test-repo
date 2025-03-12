from tabulate import tabulate
import urllib,urllib.request
import xmltodict
import json
count=0
table=[]
user_input= input("Enter the topic name: ")
l=user_input.split(" ")
user_input="+".join(l)
url=f"http://export.arxiv.org/api/query?search_query=all:{user_input}&start=0&max_results=5"
paper_data=urllib.request.urlopen(url)
data=paper_data.read().decode("utf-8")
with open("data.xml","w",encoding="utf-8") as xml_data:
    xml_data.write(data)
with open("data.xml","r",encoding="utf-8") as xml_data:
    xml_content = xml_data.read()
dic_data=xmltodict.parse(xml_content)
with open("research.json" ,"w",encoding="utf-8") as json_file:
    json_data=json.dump(dic_data, json_file, indent=4)
with open("research.json","r") as json_file:
    data=json.load(json_file)
    in_table={}
    while count<len(data["feed"]["entry"]):
        title=data["feed"]["entry"][count]["title"]
        in_table["Title"]=title
        author=data["feed"]["entry"][count]["author"]
        if isinstance(author,list):
            for index in range(len(author)):
                name=author[index]["name"]
                if not "Author Name" in in_table.keys():
                    in_table["Author Name"]=[]
                    in_table["Author Name"].append(name)
                else:
                    in_table["Author Name"].append(name)
        else:
            name=author["name"]
            in_table["Author Name"]=name
        summary=data["feed"]["entry"][count]["summary"]
        in_table["Summary"]=summary
        table.extend([in_table])
        count+=1
        in_table={}
print(tabulate(table, headers="keys",tablefmt="fancy_grid",showindex="always"))