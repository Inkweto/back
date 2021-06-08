import os
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

def generate_sample_results(limit):
    results = []
    for i in range(limit):
        results.append({'index': i, 'log': 'This is sample result ' + str(i)})
    return results

lsns = api.namespace('logs-search', description='Log search namespace')
search_parser = reqparse.RequestParser()
search_parser.add_argument('contains', type=str, help='Search phrase')
search_parser.add_argument('limit', type=int, default=20)
search_parser.add_argument('from_date', type=inputs.datetime_from_iso8601)
search_parser.add_argument('to_date', type=inputs.datetime_from_iso8601)


@lsns.route('/')
class LogsSearch(Resource):
    @lsns.expect(search_parser)
    def get(self):
        args = search_parser.parse_args()

        from_date_str = 'Not provided'
        to_date_str = 'Not provided'

        if args['from_date']:
            from_date_str = args['from_date'].strftime('%m/%d/%Y, %H:%M:%S')
        if args['to_date']:
            to_date_str = args['to_date'].strftime('%m/%d/%Y, %H:%M:%S')

        log_filename = 'generated.log'
        result_id = searchIn(log_filename)

        response = {
            'contains': args['contains'],
            'limit': args['limit'],
            'from_date': from_date_str,
            'to_date': to_date_str,
            'result_id': result_id
        }

        return response, 200, {"Access-Control-Allow-Origin": "*"}

log_result_api = api.namespace('result', description='Log result namespace')

log_result_post = reqparse.RequestParser()
log_result_post.add_argument('id', type=int)
log_result_post.add_argument('search_phrase', type=str)
log_result_post.add_argument('line', type=str)
log_result_post.add_argument('date', type=inputs.datetime_from_iso8601)
log_result_post.add_argument('content', type=str)

log_result_get = reqparse.RequestParser()
log_result_post.add_argument('id', type=int)

@log_result_api.response(400, 'Parameters not provided')
@log_result_api.route('/')
class Result(Resource):
    @log_result_api.response(201, 'Result added')
    
    @log_result_api.expect(log_result_post)
    def post(self): # for spark to send result
        args = log_result_post.parse_args()

        if args['id'] and args['search_phrase'] and args['line'] and args['date'] and args['content']:
            search_id = args['id']
            search_phrase = args['search_phrase']
            line = args['line'] 
            date = args['date'] 
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
            return {'msg': 'log_result(result can be in database or not yet)'}, 200
        return {'msg': 'Parameters not provided'}, 400

        

if __name__ == '__main__':
    app.run(host='0.0.0.0')
