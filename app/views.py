from app import app
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template, make_response, Response
import requests
from os import environ  
import datetime
from schedule import today_sch, tomorrow_sch, week_sch
import sys

sys.path.append('..')
from schedule_parser.main import parse_schedule

####
@app.route('/api/schedule/<string:group>/today', methods=["GET"])
def today(group):
    """Today's schedule for requested group
    ---
    parameters:
      - name: group
        in: path
        type: string
        required: true
      
    definitions:
      Lesson:
        type: object
        nullable: true
        properties:
          lesson:
            type: object
            properties:
              classRoom: 
                type: string
              name: 
                type: string
              teacher: 
                type: string
              type: 
                type: string
            
          time:
            type: object
            properties:
              start: 
                type: string
              end: 
                type: string
    responses:
      200:
        description: Return today\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/Lesson'
          minItems: 8
          maxItems: 8
            
      503:
          description: Retry-After:100
    """

    sch = today_sch(group)
    if sch:
      response = jsonify(sch)
      # return "today for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':80}, status=503)
    return res 

#############
@app.route('/api/schedule/<string:group>/tomorrow', methods=["GET"])
def tomorrow(group):
    """Today's schedule for requested group
    ---
    parameters:
      - name: group
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return tomorrow\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/Lesson'
          minItems: 8
          maxItems: 8
            
      503:
          description: Retry-After:100
    """
    res = tomorrow_sch(group)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':80}, status=503)
    return res 
    
@app.route('/api/schedule/<string:group>/week', methods=["GET"])
def week(group):
    """Today's schedule for requested group
    ---
    parameters:
      - name: group
        in: path
        type: string
        required: true
      
    responses:
      200:
        description: Return tomorrow\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          type: object
          properties:
            monday:
              items:
                $ref: '#/definitions/Lesson'
              minItems: 8
              maxItems: 8
            
      503:
          description: Retry-After:100
    """
    res =  week_sch(group)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':100}, status=503)
    return res 

@app.route('/refresh', methods=["POST"])
def refresh():
    """Refresh shedule
    ---

    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    parse_schedule()
    return make_response({"status": 'ok'})