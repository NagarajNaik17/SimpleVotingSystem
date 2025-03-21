from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  #Mysql username
app.config['MYSQL_PASSWORD'] = ''   #mysql password
app.config['MYSQL_DB'] = 'voting_system'
app.config['UPLOAD_FOLDER'] = 'static/images'

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


OFFICER_ID = "12345"
OFFICER_PASSWORD = "password"

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/officer/login', methods=['GET', 'POST'])
def officer_login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        if user_id == OFFICER_ID and password == OFFICER_PASSWORD:
            session['user_type'] = 'officer'
            return redirect(url_for('officer_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('officer_login.html')


@app.route('/')
def home():
    return render_template('main.html')  



from flask import flash
import os
from werkzeug.utils import secure_filename


app.config['UPLOWD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/officer/dashboard', methods=['GET', 'POST'])
def officer_dashboard():
    if 'user_type' not in session or session['user_type'] != 'officer':
        return redirect(url_for('officer_login'))

    try:
       
        if request.method == 'POST':
            name = request.form['name']
            place = request.form['place']
            party_symbol = request.files['party_symbol']

          
            if party_symbol and allowed_file(party_symbol.filename):
                filename = secure_filename(party_symbol.filename)
                save_path = os.path.join(app.config['UPLOWD_FOLDER'], filename)
                party_symbol.save(save_path)
                symbol_path = f"images/{filename}"
            else:
                flash('Invalid file format. Allowed: PNG, JPG, JPEG, GIF')
                return redirect(url_for('officer_dashboard'))

          
            with mysql.connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO candidates (name, place, party_symbol) VALUES (%s, %s, %s)",
                    (name, place, symbol_path)
                )
                mysql.connection.commit()
                flash('Candidate added successfully')

      
        selected_place = request.args.get('place', '')
        
        with mysql.connection.cursor() as cur:
        
            cur.execute("SELECT DISTINCT place FROM candidates")
            all_places = [row['place'] for row in cur.fetchall()]

          
            query = "SELECT * FROM candidates"
            params = ()
            if selected_place:
                query += " WHERE place = %s"
                params = (selected_place,)
            
            cur.execute(query, params)
            candidates = cur.fetchall()

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {str(e)}')
        app.logger.error(f'Officer dashboard error: {str(e)}')

    return render_template('officer_dashboard.html',
                         all_places=all_places,
                         selected_place=selected_place,
                         candidates=candidates)

@app.route('/delete_candidate/<int:id>', methods=['POST'])
def delete_candidate(id):
    if 'user_type' not in session or session['user_type'] != 'officer':
        return redirect(url_for('officer_login'))
    
    try:
        with mysql.connection.cursor() as cur:
        
            cur.execute("SELECT party_symbol FROM candidates WHERE id = %s", (id,))
            result = cur.fetchone()
            
            if result:
              
                if result['party_symbol']:
                    file_path = os.path.join(app.root_path, 'static', result['party_symbol'])
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
            
                cur.execute("DELETE FROM candidates WHERE id = %s", (id,))
                mysql.connection.commit()
                flash('Candidate deleted successfully')
            else:
                flash('Candidate not found')

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error deleting candidate: {str(e)}')
        app.logger.error(f'Delete candidate error: {str(e)}')
    
    return redirect(url_for('officer_dashboard'))





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')

@app.route('/officer/logout')
def officer_logout():
    session.pop('user_type', None)
    return redirect(url_for('home'))


@app.route('/voter/signup', methods=['GET', 'POST'])
def voter_signup():
    if request.method == 'POST':
        name = request.form['name']
        voter_id = request.form['voter_id']
        password = generate_password_hash(request.form['password'])
        place = request.form['place']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO voters (name, voter_id, password_hash, place) VALUES (%s, %s, %s, %s)",
                (name, voter_id, password, place)
            )
            mysql.connection.commit()
            flash('Registration successful! Please login')
            return redirect(url_for('voter_login'))
        except:
            flash('Voter ID already exists')
        finally:
            cur.close()
    
    return render_template('voter_signup.html')

@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        password = request.form['password']
        place = request.form['place']
        
        cur = mysql.connection.cursor()
        try:
          
            cur.execute("""
                SELECT 
                    id,
                    name,
                    voter_id,
                    password_hash,
                    place,
                    voted 
                FROM voters 
                WHERE voter_id = %s AND place = %s
            """, (voter_id, place))
            voter = cur.fetchone()
            
            if voter:
             
                if check_password_hash(voter['password_hash'], password):
                    if voter['voted']:
                        flash('You have already voted')
                    else:
                      
                        session['user_type'] = 'voter'
                        session['voter_id'] = voter['id']
                        session['voter_name'] = voter['name'] 
                        session['place'] = voter['place']     
                        return redirect(url_for('voter_dashboard'))
                else:
                    flash('Invalid password')
            else:
                flash('Voter ID not found in this constituency')
                
        except Exception as e:
            print(f"Database error: {str(e)}")
            flash('Login error occurred')
        finally:
            cur.close()
    
    return render_template('voter_login.html')



@app.route('/voter/dashboard')
def voter_dashboard():
    if 'user_type' not in session or session['user_type'] != 'voter':
        return redirect(url_for('voter_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM candidates WHERE place = %s", (session['place'],))
    candidates = cur.fetchall()
    cur.close()
    
    return render_template('voter_dashboard.html', candidates=candidates)

@app.route('/vote', methods=['POST'])
def vote():
    if 'user_type' not in session or session['user_type'] != 'voter':
        return redirect(url_for('voter_login'))
    
    candidate_id = request.form['candidate']
    
    cur = mysql.connection.cursor()
    try:
    
        cur.execute(
            "UPDATE candidates SET votes = votes + 1 WHERE id = %s",
            (candidate_id,)
        )
        
      
        cur.execute(
            "UPDATE voters SET voted = TRUE WHERE id = %s",
            (session['voter_id'],)
        )
        
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
    finally:
        cur.close()
    
    session.pop('user_type', None)
    session.pop('voter_id', None)
    session.pop('place', None)
    return render_template('vote_success.html')

@app.route('/voter/logout')
def voter_logout():
    session.pop('user_type', None)
    session.pop('voter_id', None)
    session.pop('place', None)
    return redirect(url_for('voter_login'))

if __name__ == '__main__':
    app.run(debug=True)