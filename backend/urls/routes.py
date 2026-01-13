from flask import redirect, render_template, request, Blueprint, current_app, Response, url_for
from werkzeug.utils import secure_filename
from parsers.pypdf2_parser import pdfParser
from parsers.doc_parser import documentParser
from parsers.image_parser2 import imageParser
from parsers.another_imp_parsers import UniversalDocParser
from parsers.text_parser import textParser
from models.chatgpt_response import chatGPTResponse
from models.groq_response import GroqResumeParser
from database_models.models import User
from models.deepseek_response import call_render
from urls.save_to_database import Save
from flask_login import current_user
from database_models.posts import Post
from database_models.resume_details import ResumeDetails
from database_models.resume_model import Resume
import os
from database.database import db
from datetime import datetime
from flask_login import login_required

upload_bp = Blueprint('urls', __name__)

ALLOWED_EXT = {'txt', 'pdf','docx','doc','jpg','png','rtf','md','odt','jpeg'}


def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT
    
    
@upload_bp.route('/parser', methods=['POST'])
@login_required
def parser():
    if not current_user.id:
        return 'no user'
        
    files = request.files.getlist('files')
    
    print(len(files))
    if len(files) == 0:
        return "No file Uploaded, Or technical error occur"
        
    filenames = []
    texts = []
    resume_jsons = []
    print("Logged User:", current_user.is_authenticated, current_user.id)

        
    for file in files:
        
        if file.filename == '':
            return "empty file, or No file name"
        
        if not allowed(file.filename):
            return "extension not allowed"
            
        try: 
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f'user_{current_user.id}')
            os.makedirs(user_folder, exist_ok=True)
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.',1)[1].lower()
            filepath = os.path.join(user_folder, f'{filename}_{int(datetime.utcnow().timestamp())}.{ext}')
            file.save(filepath)
            
            post = Post(
                filename = filename,
                filepath = filepath,
                status = 'processing',
                user_id = current_user.id
            )
            
            db.session.add(post)
            db.session.commit()
            
            
            text = ''
            resume_json = ''
            ocr_engine = ''
            
            try:
                if ext == 'pdf':
                    only_text = pdfParser(filepath)
                    text = str(only_text.extract_all_text()) or ''
                    # gpt = chatGPTResponse(text)
                    # resume_json = gpt.get_response()
                    ocr_engine = 'PDF_PARSER'
                
                elif ext == 'docx':
                    only_text = documentParser(filepath)
                    text = str(only_text.extract_all_text()) or ''
                    # gpt = chatGPTResponse(text)
                    # resume_json = gpt.get_response()
                    ocr_engine = 'DOC_PARSER'
                elif ext  in ('doc','odt','rtf'):
                    only_text = UniversalDocParser(filepath)
                    text = str(only_text.extract_all_text()) or ''
                    # gpt = chatGPTResponse(text)
                    # resume_json = gpt.get_response()
                    ocr_engine = 'UNIVERSAL PARSER'
                elif ext in ('jpg','jpeg','png'):
                    only_text = imageParser(filepath)
                    text = str(only_text.extract_all_text()) or ''
                    # gpt = chatGPTResponse(text)
                    # resume_json = gpt.get_response()
                    ocr_engine = 'Image Parser'
                
                elif ext in ('md', 'txt'):
                    only_text = textParser(filepath)
                    text = str(only_text.extract_all_text()) or ''
                    # gpt = chatGPTResponse(text)
                    # resume_json = gpt.get_response()
                    ocr_engine = 'Text Parser'
                else:
                    text = ''
                    ocr_engine = ''
                    resume_json = ''
            except Exception as e:
                post.status = 'failed'
                db.session.commit()
                return f'error {e}'
                
            if not text.strip():
                post.status = 'failed'
                db.session.commit()
                return f'faile to exxtract the text'
                
            post.text = text
            post.resume_json = resume_json
            post.status = 'remaining_json'
            post.ocr_engine = ocr_engine
            
            db.session.commit()
            texts.append(text)
            filenames.append(filename)
            resume_jsons.append(resume_json)
            
            
                
                
        except Exception as e:
            return f'failed and error occur {e}'
            
                                       
    return render_template('result.html', texts= texts, filenames = filenames)

def check_data(data):
    for value in data.values():
        if value == "" or value is None or value == []:
            return True
        return False

    
@upload_bp.route('/generate_result/<int:id>/<int:model>')
def generate_result(id, model):
    if model >= 3:
        return "All models failed or limit reached", 400
    print(model)    
    post = Post.query.get_or_404(id)
    models = ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"]
    #['openai/gpt-oss-20b:free', "deepseek/deepseek-r1-0528:free", "google/gemma-3n-e2b-it:free"]
    
    if not post.text:
        return 'No extractoin text alvailable', 400 

    # gpt = chatGPTResponse(post.text, models[model])
    response = GroqResumeParser(post.text, models[model])
    print(models[model])
    resume_json = response.get_response()
    print(resume_json)
    
    if 'error' in resume_json:
        return redirect(url_for('upload_bp.generate_result', id=id, models=model + 1))
        
    if not isinstance(resume_json, dict) or not resume_json:
        return "sorry unable to extract data", 400
    
    
    resume_details = ResumeDetails(
        extracted_text_id = post.id,
        user_id = current_user.id
    )
    print('after inin details')
      
    
    if check_data(resume_json):
        resume_details.name = resume_json.get('name')
        resume_details.email = resume_json.get('email')
        resume_details.phone = str(resume_json.get('phone'))
        resume_details.skillset = resume_json.get('skills')
        resume_details.education = resume_json.get('education')
        resume_details.experience = resume_json.get('experience')
        resume_details.status = 'Failed'
        
    try:
        
        resume_details.name = resume_json.get('name')
        resume_details.email = resume_json.get('email')
        resume_details.phone = str(resume_json.get('phone'))
        resume_details.skillset = resume_json.get('skills')
        resume_details.education = resume_json.get('education')
        resume_details.experience = resume_json.get('experience')
        resume_details.status = 'completed'
    except Exception as e:
        print('inside except')
        resume_details.raw_json = resume_json
        resume_details.status = f'Error {e}'
    db.session.add(resume_details)
    
    post.resume_json = resume_json
    post.status = 'Completed'
    
    db.session.commit()
    return redirect(url_for('urls.view_file', id = post.id))
    

@upload_bp.route('/view/<int:id>')
def view_file(id):
    posts = Post.query.filter_by(id = id, user_id = current_user.id , is_deleted = False).first_or_404()
    texts = [posts.text]
    filenames = [posts.filename]
    try:
        resumedetails = ResumeDetails.query.filter_by(
            extracted_text_id=id
        ).first_or_404()
    except Exception as e:
        resumedetails = None
    
    return render_template('result.html', texts = texts, filenames = filenames, resume = resumedetails, json = posts.resume_json)
   
 