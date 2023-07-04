import sys
import os
import sqlite3
from flask import Flask, request, abort, make_response, render_template
from database import search

app = Flask(__name__, static_folder='static', static_url_path='/static',
        template_folder='./templates')
#-----------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/search_non_url', methods=['GET', 'POST'])
def search_non_url():
    label = request.args.get('l')
    classifier = request.args.get('c')
    agent = request.args.get('a')
    department = request.args.get('d')

    if label is None:
        label = ''
    if classifier is None:
        classifier = ''
    if agent is None:
        agent = ''
    if department is None:
        department = ''

    if ((label is None) or (label.strip() == '')) and ((classifier is None) or (classifier.strip() == '')) and ((agent is None) or (agent.strip() == '')) and ((department is None) or (department.strip() == '')):
        response = make_response('')
        return response

    inputs = [label, agent, department, classifier]
    try:
        results_table = search(inputs)
    except sqlite3.OperationalError as ex:
        print(ex, file=sys.stderr)
        os._exit(1)

    html='''
    <table>
        <tr>
            <th>Label</th>
            <th>Date</th>
            <th>Agents</th>
            <th>Classified As</th>
        </tr>
    '''

    for row in results_table:
        html += '''
        <tr>
            <td><a href=/obj/%s target="_blank"> %s </a></td>
            <td>%s</td>
            <td>
        ''' % tuple(row[:3])

        agent_list = row[3].split(',')
        for item in agent_list:
            html += '%s' % item
            if item != agent_list[-1]:
                html += '<br/>'

        html += '''
        </td>
        <td>
        '''
        classifier_list = row[4].split(',')
        for item in classifier_list:
            html += '%s' % item
            if item != classifier_list[-1]:
                html += '<br/>'

    html += '''
            </td>
        </tr>
    </table>
    '''

    response = make_response(html)
    # response.set_cookie('prev_label', label)
    # response.set_cookie('prev_classifier', classifier)
    # response.set_cookie('prev_agent', agent)
    # response.set_cookie('prev_department', department)
    return response

@app.route('/search', methods=['GET', 'POST'])
def search_results():
    label = request.args.get('l')
    classifier = request.args.get('c')
    agent = request.args.get('a')
    department = request.args.get('d')

    if label is None:
        label = ''
    if classifier is None:
        classifier = ''
    if agent is None:
        agent = ''
    if department is None:
        department = ''

    if ((label is None) or (label.strip() == '')) and ((classifier is None) or (classifier.strip() == '')) and ((agent is None) or (agent.strip() == '')) and ((department is None) or (department.strip() == '')):
        response = make_response('')
        return response

    inputs = [label, agent, department, classifier]
    try:
        results_table = search(inputs)
    except sqlite3.OperationalError as ex:
        print(ex, file=sys.stderr)
        os._exit(1)

    html = '''
        <!DOCTYPE html>
    <html>
        <head>
            <title>YUAG Collection Search</title>
            <link rel="stylesheet" href="/static/styles.css"/>
        </head>
        <body>
            <h1>YUAG Collection Search</h1>
            <form method="get" action="/search">
            <br>
            <br>
        '''
    html += '''
    <table>
        <tr>
            <th>Label</th>
            <th>Date</th>
            <th>Agents</th>
            <th>Classified As</th>
        </tr>
    '''

    for row in results_table:
        html += '''
        <tr>
            <td><a href=/obj/%s target="_blank"> %s </a></td>
            <td>%s</td>
            <td>
        ''' % tuple(row[:3])

        agent_list = row[3].split(',')
        for item in agent_list:
            html += '%s' % item
            if item != agent_list[-1]:
                html += '<br/>'

        html += '''
            </td>
            <td>
        '''
        classifier_list = row[4].split(',')
        for item in classifier_list:
            html += '%s' % item
            if item != classifier_list[-1]:
                html += '<br/>'

    html += '''
            </td>
        </tr>
    </table>
    '''
    response = make_response(html)

    # response.set_cookie('prev_label', label)
    # response.set_cookie('prev_classifier', classifier)
    # response.set_cookie('prev_agent', agent)
    # response.set_cookie('prev_department', department)

    return response

@app.route('/obj/<obj_id>', methods=['GET'])
def objects(obj_id):
    results = search([obj_id])

    if results == [[], None, [], [(None,)], []]:
        html = render_template('404.html',
                               message=f"no object with id {obj_id} exists."), 404
        response = make_response(html)
        return response

    summary_results = results[0][0]
    label = results[1][0]
    prod_by_results = results[2]
    classifiers_results = results[3][0][0]
    classifiers_results = classifiers_results.split(',')
    information_results = results[4]

    print(prod_by_results)

    # prev_label = request.cookies.get('prev_label')
    # prev_classifier = request.cookies.get('prev_classifier')
    # prev_agent = request.cookies.get('prev_agent')
    # prev_department = request.cookies.get('prev_department')

    html = render_template('object.html',
                obj_id=obj_id,
                acc_no=summary_results[0],
                date=summary_results[1],
                place=summary_results[2],
                label=label,
                # part=prod_by_results[0],
                # name=prod_by_results[1],
                # nationalities=prod_by_results[2],
                # timespan=prod_by_results[3],
                agents=prod_by_results,
                classifiers=classifiers_results,
                references=information_results)

    response = make_response(html)
    return response

@app.route('/obj', methods=['GET'])
def no_object():
    abort(404)

@app.errorhandler(404)
def error(error):
    return render_template('404.html',
                           message="missing object id."), 404
