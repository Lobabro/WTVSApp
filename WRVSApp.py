from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
#test