from app import app
from flask import Flask, redirect, url_for, render_template


@app.route('/')
def index():
    return render_template('index.html');

@app.route('/Kun WANG')
def kun():
    return render_template('kun2.html', name="Kun WANG");

@app.route('/Shikun CHEN')
def shikun():
    return render_template('shikun2.html', name="Shikun CHEN");

@app.route('/Yu LOU')
def yu():
    return render_template('yu.html', name="Yu LOU");

@app.route('/Zhuoyu GUO')
def zhuoyu():
    return render_template('zhuoyu.html', name="Zhuoyu GUO");

@app.route('/daojishi')
def daojishi():
    return render_template('daojishi.html', name="Daojishi");


