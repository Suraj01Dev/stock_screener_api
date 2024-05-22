from flask import Flask, request
import json
import subprocess
import os
script_path=os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)

@app.route("/")
def welcome():
    return {"msg":"welcome"}

@app.route("/stock_data")
def stock_data():
    s_name=request.args.get('s_name')
    process(s_name)
    with open(f"{script_path}/stock.json", "r") as f:
            data=f.read()
    if data=="":
         return {f"{s_name}":"Not Found"}
    data=json.loads(data)[0]
    data=json.dumps(data)
 
    return data


def process(stock_name):
    result=subprocess.run(["python3","stock_scraper.py","--stock_name",stock_name], stderr=subprocess.PIPE)
    print("return_code"+str(result.returncode))
    return result.returncode
    #aavasfinanciers
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


    
