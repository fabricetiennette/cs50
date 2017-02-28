from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    
    tweets = helpers.get_user_timeline(screen_name)

    
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    
    analyzer = Analyzer(positives, negatives)
    
    
    score = 0
    
    
    total_score = 0
    positive, negative, neutral = 0.0, 0.0, 0.0
    
    
    if tweets != None:
        for i in range(100):
            if i >= len(tweets):
                break
            score = analyzer.analyze(tweets[i])
            total_score += 1
            if score > 0.0:
                positive += 1
            elif score < 0.0:
                negative += 1
            else:
                neutral += 1
                
                
    if total_score == 0:
        neutral = 100
    else:
        if positive != 0:
            positive = (1.0 * positive / total_score) * 100
        if negative != 0:
            negative = (1.0 * negative / total_score) * 100
        if neutral != 0:
            neutral = (1.0 * neutral / total_score) * 100
            
            
    chart = helpers.chart(positive, negative, neutral)
    
    
    return render_template("search.html", chart=chart, screen_name=screen_name)