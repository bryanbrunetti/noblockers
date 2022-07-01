import os
import redis as r
import random
import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
redis = r.StrictRedis.from_url(os.environ.get("REDIS_URL", "redis://localhost"))


def get_participants():
    participants = redis.smembers("participants")
    participants = participants if participants else []
    return list(participants)


@app.route('/')
def good_morning():
    participants = get_participants()
    # TODO: Allow the date to be passed in as an argument to allow seeing what future ordering will look like
    now = datetime.datetime.now()
    dt = now.strftime('%-j')

    random.seed(int(dt) + 1)
    random.shuffle(participants)

    return render_template("standup.html", participants=participants, today=now.strftime("%A %B %-d %Y"))


@app.route("/update", methods=['GET'])
def get_update():
    participants = get_participants()
    return render_template("update.html", participants=participants)


@app.route("/add", methods=["POST"])
def add_participant():
    redis.sadd("participants", request.form['participant'])

    return redirect("/update")


@app.route("/remove")
def remove_participant():
    redis.srem("participants", request.args['name'])

    return redirect("/update")


if __name__ == '__main__':
    app.run()
