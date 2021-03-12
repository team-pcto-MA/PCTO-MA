from flask import Flask, Blueprint, request, render_template, jsonify


login = Blueprint('login', __name__)

@login.route('/')
def index():
    return "Home page"


