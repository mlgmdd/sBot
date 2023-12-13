from flask import Flask, request, jsonify

post_server_app = Flask(__name__)
data = {}


@post_server_app.route('/post', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        global data
        data = request.json
        return jsonify({'message': 'POST request received successfully'})


@post_server_app.route('/get_data', methods=['GET'])
def get():
    global data
    rsp = data
    data = {}
    return rsp


if __name__ == '__main__':
    # 启动 Flask 应用
    post_server_app.run(debug=True)
