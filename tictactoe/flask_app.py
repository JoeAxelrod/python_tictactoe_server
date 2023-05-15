from flask import Flask, request, jsonify
import sqlite3

from tictactoe.game import main, string2board


def init_db():
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        phone TEXT NOT NULL,
        board_string TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


init_db()

app = Flask(__name__)

empty_board = """  |   |  
---------
  |   |  
---------
  |   |  """


@app.route('/api/tictactoe', methods=['POST'])
def python_endpoint():
    req_data = request.get_json()
    phone = req_data.get('phone', "")
    action = req_data.get('action', "")

    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    if not phone:
        return jsonify({"error": "Phone number is required."}), 400

    cursor.execute("SELECT board_string FROM games WHERE phone = ?", (phone,))
    result = cursor.fetchone()

    if result:
        board_string = result[0]
    else:
        cursor.execute("INSERT INTO games (phone, board_string) VALUES (?, ?)", (phone, empty_board))
        conn.commit()
        conn.close()
        return jsonify({
            "board_json": string2board(empty_board),
            "board_string": empty_board,
            "result": None,
            "winner": None,
        })

    board_string, board, result, winner = main(board_string, action)

    if winner:
        cursor.execute("DELETE FROM games WHERE phone = ?", (phone,))
        conn.commit()
    else:
        cursor.execute("UPDATE games SET board_string = ? WHERE phone = ?", (board_string, phone))
        conn.commit()

    conn.close()

    return jsonify({
        "board_json": board,
        "board_string": board_string,
        "result": result,
        "winner": winner,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
