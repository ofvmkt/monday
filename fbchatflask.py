from flask import Flask, request, abort, jsonify
from datetime import datetime
import requests
import json
global itmeid, message

app = Flask(__name__)

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEzMzc5NzAwNSwidWlkIjoyNTcwNTgwMSwiaWFkIjoiMjAyMS0xMS0xOVQwNTo1MzozMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTAzMjgyNTQsInJnbiI6InVzZTEifQ.-8q9zCVz8ndYtBMdFK95vYxxPIf_6BIre3cMNs6jaIY"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}
global itemid, message

def checkID(psid):
    global itemid, message
    query = 'query ($myColumnPsId: String!) { items_by_column_values (board_id:1946804760, column_id:"text",  column_value:$myColumnPsId ) { id name column_values (ids:["message"]){text} } }'
    vars = {'myColumnPsId' : psid}
    data = {'query' : query, 'variables' : vars}
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    j = r.json()
    n = len(j['data']['items_by_column_values'])
    if n > 0 :
        itemid = j['data']['items_by_column_values'][0]['id']
        message = j['data']['items_by_column_values'][0]['column_values'][0]['text']
        print("대화 검색 결과 >>> ", itemid)
    return n
    
def updateById(message2, time1):
    global itemid, message
    message21 = f"> {message2}\n{message}"
    time_obj = datetime.strptime(time1.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    time3 = time_obj.strftime('%Y-%m-%d')
    
    query = 'mutation ($myItemId: Int!, $columnVals: JSON!) { change_multiple_column_values (board_id:1946804760, item_id:$myItemId,  column_values:$columnVals ) { id } }'
    vars = {
             'myItemId' : int(itemid),
             'columnVals' : json.dumps({'message' : message21, '__' : {'label' : 'Talking'}, 'time'   : {'date' : time3}})
            }
        
    data = {'query' : query, 'variables' : vars}
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    j = r.json()
    print("업데이트 성공 >>> ", j['data']['change_multiple_column_values']['id'])
    return 'success', 100


def createNew(name, message1, psid, time1):
    message1 = f"> {message1}"
    time_obj = datetime.strptime(time1.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    time3 = time_obj.strftime('%Y-%m-%d')
    
    query = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id:1946804760, item_name:$myItemName, column_values:$columnVals) { id } }'
    vars = {
             'myItemName' : name,
             'columnVals' : json.dumps({'message' : message1, '__' : {'label' : 'Start'}, 'time' : {'date' : time3}, 'text': psid })
            }
    data = {'query' : query, 'variables' : vars}
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    j = r.json()
    print("신규 대화 오픈 >>> ", j['data']['create_item']['id'])
    return 'success', 100

@app.route("/webhook", methods=['POST'])
def webhook():    
    if request.method == 'POST':
        content = json.loads(request.get_data())
        fb_name = content['fb_name']
        fb_message = content['fb_message']
        fb_psid = content['fb_psid']        
        fb_time = content['fb_time']
        
        if checkID(fb_psid) == 0 :
            createNew(fb_name, fb_message, fb_psid, fb_time)
        elif checkID(fb_psid) == 1 :
            updateById(fb_message, fb_time)
        else:
            return 'fail', 300

        return 'success', 200
    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run(threaded=True, port=5000)