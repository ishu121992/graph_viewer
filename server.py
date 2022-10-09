from flask import Flask, send_file, request
from graphplot import GraphVisualizer

app = Flask(__name__)

@app.route('/plot', methods=['GET'])

def plot():
    data = request.json

    if request.args is not None:
        params = {}
        for i in request.args.keys():
            if i == 'fig_size':
                params[i] = (int(request.args[i]),int(request.args[i]))
            elif i == 'node_size':
                params[i] = int(request.args[i])
            else:
                params[i] = request.args[i]
        print(params)
        file = GraphVisualizer(data, params).weighted_graph_show()
        return send_file(file, mimetype='image/png')
    else:
        file = GraphVisualizer(data).weighted_graph_show()
        return send_file(file, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)