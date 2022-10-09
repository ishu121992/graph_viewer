# graph_viewer
API to send adjacency list as input and request plot of directed or undirected graphs

#### How to use the API ####
```python
import requests
from PIL import Image
import io

# Define an adjacency list like this

adjacency_list = {'A': [('B', 8), ('C', 2), ('D', 4)],
 'B': [('A', 8), ('C', 7), ('E', 2)], 
'C': [('A', 2), ('B', 7), ('E', 3), ('F', 9), ('D', 1)], 
'D': [('A', 4), ('C', 1), ('F', 5)], 
'E': [('B', 2), ('C', 3)], 
'F': [('C', 9), ('D', 5)]}

Create Parameters for API call
params = {
            'graph_layout':'draw_spring', 
            'node_color':'pink', 
            'fig_size':(5,5), 
            'node_size':200
}
"""
Possible Graph Layout Options:

"""

r = requests.get('http://127.0.0.1:5000/plot', params = params, json=adjacency_list)
image = Image.open(io.BytesIO(r.content))
```
