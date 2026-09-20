import json


file = "history_demo.json"


with open(file,"r") as f:
    data = json.load(f)



for item in data:

    if item.get("recomandare") == "Promovare":
        item["recomandare"] = "Promotion Recommended"

    elif item.get("recomandare") == "Evaluare suplimentara":
        item["recomandare"] = "Additional Evaluation Required"

    elif item.get("recomandare") == "Nu este pregatit":
        item["recomandare"] = "Not Ready for Promotion"



    if item.get("trend") == "Pozitiv":
        item["trend"] = "Positive"

    elif item.get("trend") == "Negativ":
        item["trend"] = "Negative"

    elif item.get("trend") == "Stabil":
        item["trend"] = "Stable"



with open(file,"w") as f:
    json.dump(data,f,indent=4)



print("History translated successfully")