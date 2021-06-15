import os
import subprocess
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restx import Resource, Api, reqparse, inputs
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)

def searchIn(logFilename):
    pathToFile = os.getcwd() + "/logs/" + logFilename
    if os.path.isfile(pathToFile):
        logFile = open(pathToFile, "r")
        #apache.search(pathToFile) or some other way to start searching in apache
        result_id = 1
        return result_id
    return -1  

def run_script_with_args(contains, limit, result_id):
    spark_env = os.environ.copy()
    spark_env['SPARK_APPLICATION_PYTHON_LOCATION'] = '/flask/search.py'
    spark_env['SPARK_APPLICATION_ARGS'] = '"' + contains + '"' + ' ' + str(limit) + ' ' + str(result_id)
    subprocess.Popen('/submit.sh', env=spark_env)


def generate_sample_results(limit):
    results = []
    for i in range(limit):
        results.append({'index': i, 'log': 'This is sample result ' + str(i)})
    return results

lsns = api.namespace('logs-search', description='Log search namespace')
search_parser = reqparse.RequestParser()
search_parser.add_argument('contains', type=str, help='Search phrase')
search_parser.add_argument('limit', type=int, default=20)

@lsns.route('/')
class LogsSearch(Resource):
    @lsns.expect(search_parser)
    def post(self):
        args = search_parser.parse_args()

        log_filename = 'generated.log'
        result_id = searchIn(log_filename)
        run_script_with_args(args['contains'], args['limit'], result_id)

        response = {
            'msg': 'Script submited!',
            'result_id': result_id
        }

        return response, 200, {"Access-Control-Allow-Origin": "*"}

log_result_api = api.namespace('result', description='Log result namespace')

log_result_post = reqparse.RequestParser()
log_result_post.add_argument('id', type=int)
log_result_post.add_argument('content', type=str)

log_result_get = reqparse.RequestParser()
log_result_get.add_argument('id', type=int)

@log_result_api.response(400, 'Parameters not provided')
@log_result_api.route('/')
class Result(Resource):
    @log_result_api.response(201, 'Result added')
    
    @log_result_api.expect(log_result_post)
    def post(self): # for spark to send result
        args = log_result_post.parse_args()

        if args['id'] and args['content']:
            search_id = args['id']
            content = args['content']
            # created = update_element_with_id(search_id, search_phrase, line, date, content)

            response = {
                'msg': 'Result added'
                #'created': created
            }
            return response, 201

        return {'msg': 'Parameters not provided'}, 400 

    @log_result_api.response(201, 'log_result')
    @log_result_api.expect(log_result_get)    
    def get(self): # for front to gain result
        args = log_result_get.parse_args()

        if args['id']:

            #log_result = get_element_with_id(id)
            return {'msg': 'log_result(result can be in database or not yet)'}, 200, {"Access-Control-Allow-Origin": "*"}
        return {'msg': 'Parameters not provided'}, 400, {"Access-Control-Allow-Origin": "*"}


        

if __name__ == '__main__':
    app.run(host='0.0.0.0')
