from flask import Flask , jsonify
from flask import render_template
import requests
from flask import request
app = Flask(__name__)


def Query(user_name , repo_name) :
    commit_url = "https://api.github.com/repos/"+user_name+"/"+repo_name+"/commits?per_page=1"
    response = requests.get(commit_url)
    return response.json()

@app.route('/input', methods=['GET'])
def index():
    query =  request.args.get('query')
    commit_dict = {}
    url = "https://api.github.com/search/repositories?q="+query+"&per_page=5&sort=created&order=desc"
    response = requests.get(url)
    text = (response.json())
    sz = len(text["items"])
    for i in range(sz) :
        author = text["items"][i]["owner"]["login"]
        rep_name = text["items"][i]["name"]
        result = (Query(author,rep_name))
        commit_dict[i] = {}
        for item in result:
            commit_dict[i]["sha"] = item["sha"]
            commit_dict[i]["message"] = item["commit"]["message"]
            commit_dict[i]["author_name"] = item["commit"]["author"]["name"]
    return render_template('template.html',query=query, text=text,sz = sz  ,commit_dict = commit_dict )

if __name__ == '__main__':
    app.run(debug=True)
