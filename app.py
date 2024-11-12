"""
ATAC Smartarts
Copyright (c) 2024 ksolheim
Licensed under the MIT License - see LICENSE file for details
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, send_file
import sqlite3
from flask_basicauth import BasicAuth
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)

DATABASE = 'database/raffle.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

####
# Public section 
####

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/')
def public():
    return render_template('public.html')

####
# Admin section 
####

@app.route('/admin', methods=['GET', 'POST'])
@basic_auth.required
def admin():
    conn = get_db_connection()
    if request.method == 'POST':
        art_id = request.form['art_id']
        winner_name = request.form['winner_name']
        conn.execute('INSERT INTO winners (art_id, winner_name) VALUES (?, ?)', (art_id, winner_name))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    artworks = conn.execute('''
        SELECT artworks.* 
        FROM artworks 
        LEFT JOIN winners ON artworks.art_id = winners.art_id 
        WHERE winners.art_id IS NULL
    ''').fetchall()
    recent_winners = api_recent_winners().get_json()
    conn.close()
    return render_template('admin/admin.html', artworks=artworks, recent_winners=recent_winners)

@app.route('/admin/winners')
@basic_auth.required
def admin_winners():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, w.winner_name, w.winner_id 
        FROM artworks a 
        LEFT JOIN winners w ON a.art_id = w.art_id 
        ORDER BY a.art_id
    ''')
    artworks = cursor.fetchall()
    
    conn.close()
    return render_template('admin/winners.html', artworks=artworks)

@app.route('/admin/export-winners')
@basic_auth.required
def export_winners():
    conn = get_db_connection()
    artworks = conn.execute('''
        SELECT a.*, w.winner_name, w.winner_id 
        FROM artworks a 
        LEFT JOIN winners w ON a.art_id = w.art_id 
        ORDER BY a.art_id
    ''').fetchall()
    
    # Create DataFrame
    df = pd.DataFrame([{
        'ID': artwork['art_id'],
        'Title': artwork['art_title'],
        'Artist': artwork['artist'],
        'Status': 'Awarded' if artwork['winner_name'] else 'Available',
        'Winner': artwork['winner_name'] or '-'
    } for artwork in artworks])
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Artworks')
    output.seek(0)
    
    conn.close()
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='artworks_list.xlsx'
    )

####
# API section 
####

@app.route('/api/latest_winner')
def api_latest_winner():
    conn = get_db_connection()
    latest_winner = conn.execute('''
        SELECT winners.*, artworks.artist, artworks.art_title
        FROM winners 
        JOIN artworks ON winners.art_id = artworks.art_id 
        ORDER BY winner_id DESC 
        LIMIT 1
    ''').fetchone()
    conn.close()
    
    if latest_winner is None: # Return empty object if no winners exist
        return jsonify({})  
    
    return jsonify(dict(latest_winner))

@app.route('/api/recent_winners')
def api_recent_winners():
    conn = get_db_connection()
    recent_winners = conn.execute('''
        SELECT winners.*, artworks.artist, artworks.art_title
        FROM winners 
        JOIN artworks ON winners.art_id = artworks.art_id 
        ORDER BY winner_id DESC 
        LIMIT 10
    ''').fetchall()
    conn.close()
    return jsonify([dict(winner) for winner in recent_winners])

@app.route('/api/delete_winner/<int:winner_id>', methods=['POST'])
@basic_auth.required
def delete_winner(winner_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM winners WHERE winner_id = ?', (winner_id,))
    conn.commit()
    conn.close()
    
    # Get the referring page and redirect back to it
    referrer = request.referrer
    if 'winners' in referrer:
        return redirect(url_for('admin_winners'))
    return redirect(url_for('admin'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
