from flask import Flask, render_template, url_for, request, redirect
import data_handler
import data_manager
from collections import OrderedDict
import time

app = Flask(__name__)


@app.route("/list")
@app.route("/")
def get_question_list():
    all_questions = data_manager.get_questions()
    all_questions_reversed = data_handler.sorting(all_questions, sortkey='id', rev=True)
    return render_template("list.html", all_data_reversed=all_questions_reversed)


@app.route("/list/<question_id>", methods=['GET', 'POST'])
def q_id(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        message = question['message']
        title = question['title']
        answers = data_manager.get_answer_by_question_id(question_id)
        return render_template("question_id.html", message=message, title=title, answers=answers)
    elif request.method == 'POST':
        if request.form["btn"] == "Send comment":
            answer = OrderedDict()
            answer['submission_time'] = str(int(time.time()))
            answer['vote_number'] =	None
            answer['question_id'] = question_id
            answer['message'] = request.form.get('comment')
            answer['image'] = None
            data_manager.add_answer(answer)
            return redirect(url_for('get_question_list'))
        elif request.form['btn'] == "Delete question":
            data_manager.delete_question(question_id)
            data_manager.delete_answer(question_id)
            return redirect(url_for('get_question_list'))
        elif request.form['btn'] == "Edit question":
            return redirect(url_for('edit', question_id=question_id))


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    question_id = request.form.get('question_id')
    data_manager.delete_answer_by_id(answer_id)
    return redirect(url_for('q_id', question_id=question_id))


@app.route('/<question_id>/edit', methods=['GET', 'POST'])
def edit(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        message = question['message']
        title = question['title']
        return render_template('edit.html', message=message, title=title)
    elif request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        data_manager.update_question(question_id, message, title)
        return redirect(url_for('get_question_list'))


@app.route("/add_question",  methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    if request.method == 'POST':
        question = {'submission_time': int(time.time()), 'view_number': None, 'vote_number': None,
                    'title': request.form.get('title'), 'message': request.form.get('message'), 'image': None}
        data_manager.insert_question(question)
        return redirect(url_for('get_question_list'))


if __name__ == "__main__":
    app.run(debug=True)
