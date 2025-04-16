import os
import logging
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
import secrets

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", secrets.token_hex(16))
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}

# Initialize database with app
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Import models and components after Flask app and DB initialization
from models import User, Document, Feedback
from forms import LoginForm, SignupForm, UploadForm, FeedbackForm
import document_processor
import legal_chatbot

# Load user for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create DB tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = SignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('signup.html', form=form)
        
        # Create new user
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password,
            gender=form.gender.data,
            age=form.age.data,
            mobile=form.mobile.data
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    # Get user's recent documents
    recent_docs = Document.query.filter_by(user_id=current_user.id).order_by(Document.timestamp.desc()).limit(5).all()
    # Pass the current datetime for footer copyright
    now = datetime.utcnow()
    return render_template('home.html', user=current_user, recent_docs=recent_docs, now=now)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if 'document' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['document']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create document record in DB
            new_doc = Document(
                filename=filename,
                file_path=file_path,
                user_id=current_user.id
            )
            db.session.add(new_doc)
            db.session.commit()
            
            # Process the document
            try:
                # Extract text from document
                extracted_text = document_processor.extract_text(file_path)
                
                if extracted_text:
                    # Clean the text
                    cleaned_text = document_processor.clean_text(extracted_text)
                    
                    # Generate summary
                    summary = document_processor.generate_summary(cleaned_text)
                    
                    # Update document with summary
                    new_doc.content = cleaned_text[:1000]  # Store only first 1000 chars
                    new_doc.summary = summary
                    db.session.commit()
                    
                    # Redirect to result page with document ID
                    return redirect(url_for('document_result', doc_id=new_doc.id))
                else:
                    flash('Could not extract text from the document', 'danger')
            except Exception as e:
                app.logger.error(f"Error processing document: {e}")
                flash(f'Error processing document: {str(e)}', 'danger')
                
            return redirect(url_for('home'))
        else:
            flash('File type not allowed. Please upload PDF, DOCX, or TXT files only.', 'danger')
    
    return render_template('upload.html', form=form)

@app.route('/document/<int:doc_id>')
@login_required
def document_result(doc_id):
    # Get document from DB
    document = Document.query.get_or_404(doc_id)
    
    # Security check: ensure document belongs to current user
    if document.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('home'))
    
    return render_template('document_result.html', document=document)

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        # Convert 'yes'/'no' to boolean
        is_satisfied = form.satisfied.data == 'yes'
        new_feedback = Feedback(
            user_id=current_user.id,
            satisfied=is_satisfied,
            message=form.message.data
        )
        db.session.add(new_feedback)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('home'))
    
    return render_template('feedback.html', form=form)

# Chatbot API endpoint
@app.route('/api/chatbot', methods=['POST'])
@login_required
def chatbot_api():
    try:
        user_input = request.json.get('message', '')
        if not user_input.strip():
            return jsonify({
                'response': 'Please enter a legal question.',
                'resources': []
            })
        
        # Get response from chatbot
        result = legal_chatbot.find_response(user_input)
        
        if result:
            return jsonify({
                'response': result['info'],
                'resources': result.get('resources', [])
            })
        else:
            return jsonify({
                'response': "I couldn't find specific info. Try using different keywords like 'contract', 'divorce', 'property', 'tax', etc.",
                'resources': []
            })
    except Exception as e:
        app.logger.error(f"Chatbot error: {str(e)}")
        return jsonify({
            'response': 'Sorry, there was an error processing your request.',
            'resources': []
        })

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
