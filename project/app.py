import os

import sqlite3
import datetime
import random
import numpy as np
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

conn = sqlite3.connect('asmr-survey.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS question1
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

# commit the changes to db
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question2
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question3
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question4
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question5
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question6
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question7
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS question8
            (ques_id INTEGER PRIMARY KEY NOT NULL, sub_id int NOT NULL, answer TEXT NOT NULL, FOREIGN KEY (sub_id) REFERENCES submissions(submission_id))''')

conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/videos", methods=["GET", "POST"])
def videos():
    return render_template("videos.html")


@app.route("/sounds", methods=["GET", "POST"])
def sounds():
    return render_template("sounds.html")


@app.route("/sights", methods=["GET", "POST"])
def sights():
    return render_template("sights.html")


@app.route("/misc", methods=["GET", "POST"])
def misc():
    return render_template("misc.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":

        ques1 = request.form.get("survey-q1")
        ques2 = request.form.get("survey-q2")
        ques3 = request.form.get("survey-q3")
        ques4 = request.form.get("survey-q4")
        ques5 = request.form.get("survey-q5")
        ques6 = request.form.get("survey-q6")
        ques7 = request.form.get("survey-q7")
        ques8 = request.form.get("survey-q8")
        name = request.form.get("name")
        name2 = request.form.get("name2")
        cName = name.capitalize()
        cName2 = name2.capitalize()

        user_number = random.randint(1, 90000000000000)
        str_number = str(user_number)
        user_name = name + name2 + str_number
        userName = cName + " " + cName2

        c.execute(
            "INSERT INTO submissions (name, date) VALUES (?, DATE('now'))", [user_name])
        conn.commit()
        sub_data = c.fetchone()

        c.execute(
            "SELECT submission_id FROM submissions WHERE name = ?", [user_name])
        conn.commit()
        data = c.fetchone()

        c.execute(
            "INSERT INTO question1 (answer, sub_id) VALUES (?, ?)", (ques1, data[0]))
        conn.commit()
        data_1 = c.fetchone()

        c.execute(
            "INSERT INTO question2 (answer, sub_id) VALUES (?, ?)", (ques2, data[0]))
        conn.commit()
        data_2 = c.fetchone()

        c.execute(
            "INSERT INTO question3 (answer, sub_id) VALUES (?, ?)", (ques3, data[0]))
        conn.commit()
        data_3 = c.fetchone()

        c.execute(
            "INSERT INTO question4 (answer, sub_id) VALUES (?, ?)", (ques4, data[0]))
        conn.commit()
        data_4 = c.fetchone()

        c.execute(
            "INSERT INTO question5 (answer, sub_id) VALUES (?, ?)", (ques5, data[0]))
        conn.commit()
        data_5 = c.fetchone()

        c.execute(
            "INSERT INTO question6 (answer, sub_id) VALUES (?, ?)", (ques6, data[0]))
        conn.commit()
        data_6 = c.fetchone()

        c.execute(
            "INSERT INTO question7 (answer, sub_id) VALUES (?, ?)", (ques7, data[0]))
        conn.commit()
        data_7 = c.fetchone()

        c.execute(
            "INSERT INTO question8 (answer, sub_id) VALUES (?, ?)", (ques8, data[0]))
        conn.commit()
        data_8 = c.fetchone()

        num_of_answers = c.execute("SELECT COUNT(answer) FROM question1")
        conn.commit()
        number_of_answers = c.fetchone()


        part_1 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question1 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part1 = c.fetchall()

        part_2 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question2 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part2 = c.fetchall()

        part_3 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question3 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part3 = c.fetchall()

        part_4 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question4 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part4 = c.fetchall()

        part_5 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question5 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part5 = c.fetchall()

        part_6 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question6 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part6 = c.fetchall()

        part_7 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question7 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part7 = c.fetchall()

        part_8 = c.execute(
            "SELECT answer, COUNT(answer) as times_answered FROM question8 GROUP BY answer ORDER BY times_answered DESC")
        conn.commit()
        part8 = c.fetchall()

        def percent(part, whole):
            percent = int(100 * float(part)/float(whole))
            return str(percent) + "%"

        percent1 = percent(part1[0][1], number_of_answers[0])
        percent2 = percent(part2[0][1], number_of_answers[0])
        percent3 = percent(part3[0][1], number_of_answers[0])
        percent4 = percent(part4[0][1], number_of_answers[0])
        percent5 = percent(part5[0][1], number_of_answers[0])
        percent6 = percent(part6[0][1], number_of_answers[0])
        percent7 = percent(part7[0][1], number_of_answers[0])
        percent8 = percent(part8[0][1], number_of_answers[0])

        return render_template("results.html", ques1=ques1, ques2=ques2, ques3=ques3, ques4=ques4, ques5=ques5, ques6=ques6,
                               ques7=ques7, ques8=ques8, number_of_answers=number_of_answers, part1=part1, part2=part2, part3=part3,
                               part4=part4, part5=part5, part6=part6, part7=part7, part8=part8, percent1=percent1, percent2=percent2,
                               percent3=percent3, percent4=percent4, percent5=percent5, percent6=percent6, percent7=percent7,
                               percent8=percent8, userName=userName)

    else:

        words1 = ["big", "little", "gigantic", "tiny", "small", "immense", "sizable", "boundless", "colossal",
                  "mammoth", "limitless", "cosmic", "sturdy", "mini", "teeny", "endless", "epic", "towering", "petite",
                  "grand", "unlimited", "vast", "miniscule", "gargantuan", "compact", "meager", "expansive", "whopping"]

        words2 = ["tingle", "stars", "moon", "waves", "glow", "smile", "grin", "wink", "sunset", "kitten",
                  "puppy", "owl", "joy", "suprise", "trust", "feather", "flower", "knowledge", "kindness", "love",
                  "sunshine", "pleasure", "music", "violin", "piano", "choir", "laughter", "crinkle", "paper",
                  "ocean", ]

        return render_template("survey.html", words1=words1, words2=words2)
