import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restx import Resource, Api, reqparse, inputs
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)


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

        response = {
            'contains': args['contains'],
            'limit': args['limit'],
            'from_date': from_date_str,
            'to_date': to_date_str,
            'results': generate_sample_results(args['limit'])
        }
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
