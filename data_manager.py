from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT * FROM question WHERE id = %(qid)s;"""
    cursor.execute(query, {'qid': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer
        ORDER BY id;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT * FROM answer WHERE question_id = %(qid)s;"""
    cursor.execute(query, {'qid': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_answer(cursor: RealDictCursor, answer_details):
    query = """
        INSERT INTO answer  (submission_time, vote_number, question_id, message)
        VALUES(%(s_t)s, %(v_n)s, %(q_i)s, %(m_g)s);"""
    cursor.execute(query, {
        's_t': answer_details['submission_time'],
        'v_n': answer_details['vote_number'],
        'q_i': answer_details['question_id'],
        'm_g': answer_details['message']
    })
    return


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, qid: int):
    query = """
        DELETE FROM question WHERE id = %(qid)s;"""
    cursor.execute(query, {'qid': qid})
    return


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, question_id: int):
    query = """
        DELETE FROM answer WHERE question_id = %(q_id)s;"""
    cursor.execute(query, {'q_id': question_id})
    return


@database_common.connection_handler
def update_question(cursor: RealDictCursor, question_id: int, message: str, title: str):
    query = """
        UPDATE question 
        SET title = %(tt)s, message = %(msg)s
        WHERE id = %(qid)s;"""
    cursor.execute(query, {'tt': title, 'msg': message, 'qid': question_id})
    return


@database_common.connection_handler
def insert_question(cursor: RealDictCursor, question: dict):
    query = """
        INSERT INTO question (submission_time, title, message)
        VALUES (%(st)s, %(ttl)s, %(msg)s);"""
    cursor.execute(query, {
        'st': question['submission_time'],
        'msg': question['message'],
        'ttl': question['title']
    })
    return


@database_common.connection_handler
def delete_answer_by_id(cursor: RealDictCursor, answer_id: int):
    query = """
        DELETE FROM answer WHERE id = %(aid)s;"""
    cursor.execute(query, {'aid': answer_id})
    return
