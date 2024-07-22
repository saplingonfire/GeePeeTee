from flask import Flask, request, jsonify
from flask_cors import CORS 
from flask_sslify import SSLify
from score_processing import score_company
from import_to_mongodb import store_or_update_esg_scores

app=Flask(__name__)
sslify=SSLify(app)
CORS(app)

@app.route("/api/receive_json",methods=['POST'])
def receive_json():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()  # Get the JSON data
        # Process the JSON data
        company=data.get('company')
        industry=data.get('industry')
        try:
            # Run the external script and capture the output
            output = score_company(company,industry)
            print(output)
            # return jsonify({"message": "JSON received and script executed!", "data": data, "script_output": output}), 200
            store_or_update_esg_scores(output)
            return output, 200
        except Exception as e:
            print(e)
            return jsonify({"message": f"Error executing script: {e}"}), 500
    else:
        return jsonify({"message": "Request does not contain JSON data"}), 400

@app.route('/', methods=['GET'])
def hello():
    return 'api server is up!'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)