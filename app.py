import sqlite3
import flask

app = flask.Flask(__name__)

def addSynonyms(conn, word1, word2):
    #conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", ())
    print(word2)
    cur = conn.execute("SELECT word2 FROM word WHERE word1 = ?", (word2,))
    w2syns = []
    for row in cur:
        w2syns.append(row[0])
    print(w2syns)

    cur = conn.execute("SELECT word2 FROM word WHERE word1 = ?", (word1,))
    w1syns = []
    for row in cur:
        w1syns.append(row[0])
    print(w1syns)

    #word1 ~ word2's syns
    for w2 in w2syns:
        try:
            conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (word1, w2))
            conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (w2, word1))
        except:
            pass

    #word2 ~ word1's syns
    for w1 in w1syns:
        try:
            conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (word2, w1))
            conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (w1, word2))
        except:
            pass

    #word1 ~ word2
    try:
        conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (word1, word2))
        conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (word2, word1))
    except:
        pass

    #word1's syns ~ word2's syns
    for w1 in w1syns:
        for w2 in w2syns:
            try:
                conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (w1, w2))
                conn.execute("INSERT INTO word(word1, word2) VALUES(?, ?)", (w2, w1))
            except:
                pass

@app.route('/')
def home():
    return flask.render_template("home.html")

@app.route('/input', methods=["GET", "POST"])
def input_page():
    if flask.request.method == "POST":
        conn = sqlite3.connect("words.db")  
        word1 = flask.request.form["word1"]
        word2 = flask.request.form["word2"]
        addSynonyms(conn, word1, word2)

        conn.commit()
        conn.close()

    return flask.render_template("input.html")

@app.route('/wordlist')
def wordlist():
    conn = sqlite3.connect("words.db")
    cur = conn.execute("SELECT word1, word2 FROM word ORDER BY word1 ASC")
    content = []
    for row in cur:
        content.append(row)
    synDict = {}
    for tup in content:
        if not tup[0] in synDict:
            synDict[tup[0]] = tup[1]
        else:
            synDict[tup[0]] += ", " + tup[1]

    return flask.render_template("wordlist.html", synDict=synDict)

if __name__ == "__main__":
    app.run()