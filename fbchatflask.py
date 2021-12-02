import requests
import json
import os
from flask import Flask


app = Flask(__name__)

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEzMzc5NzAwNSwidWlkIjoyNTcwNTgwMSwiaWFkIjoiMjAyMS0xMS0xOVQwNTo1MzozMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTAzMjgyNTQsInJnbiI6InVzZTEifQ.-8q9zCVz8ndYtBMdFK95vYxxPIf_6BIre3cMNs6jaIY"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

query = """
        {
            items_by_column_values ( 
                board_id: 1946804760, 
                column_id: \"text\", 
                column_value: \"%s\") {
                        name
                        id
                        column_values (ids:[\"message\"]){
                            text
                        }
                }
        }
        """ %str('5051764778186636')
        
data = {'query' : query}
r = requests.post(url=apiUrl, json=data, headers=headers)
x = json.dumps(r.text)

print(x)



@app.route('/')
def hello():
    return x

if __name__ == '__main__':
    app.run()