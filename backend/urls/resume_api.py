import os
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from database_models.models import User
from database_models.resume_model import Resume
import os
from datetime import datetime
import requests
from database.database import db
from parsers.doc_parser import documentParser
from parsers.pypdf2_parser import pdfParser
from parsers.image_parser2 import imageParser
from parsers.text_parser import textParser
from models.chatgpt_response import chatGPTResponse
#from parsers.another_imp_parsers import UniversalDocParser


resume_api_bp = Blueprint('resume_api',__name__)


ALLOWED_EXT = {'txt', 'pdf','docx','doc','jpg','png','rtf','md','odt','jpeg'}


def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT
    
@resume_api_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    
    print("IDENTITY TYPE:", type(get_jwt_identity()))
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False,'message': 'Invalid User'}), 401
        
        
    files = request.files.getlist('files')    
    if len(files) ==0 :
        return jsonify({'sucess':False, 'message': 'NO file receivied'}), 400
        
    resume_id = []
    resume_filenames = []
    resume_engines = []
    resume_json = []
    
    
    for file in files:


        try: 
            if file.filename =='':
                return jsonify({'success': False,'message':'file is empty'}), 400
                
            if not allowed(file.filename) :
                return jsonify({'success': False, 'message':'unsupported file'}), 400
                
            filename = secure_filename(file.filename)
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f'user_{user_id}')
            os.makedirs(user_folder, exist_ok=True)
            filepath = os.path.join(user_folder, f"{int(datetime.utcnow().timestamp())}_{filename}")
            file.save(filepath)
            
            
            resume = Resume(user_id = user_id,
                filename = filename,
                file_path = filepath,
                status = 'Processing'
                )
                
            db.session.add(resume)
            db.session.commit()
            
            ext = filename.rsplit('.',1)[1].lower()
            
            OCR_engine = None
            extracted_text = ''
            print(ext)
            
            try:
                if ext == 'pdf':
                    text = pdfParser(filepath)
                    extracted_text = str(text.extract_all_text()) or ""
                    OCR_engine = 'pdf_parser'
                    
                elif ext in ('docx'):
                    text = documentParser(filepath)
                    extracted_text = str(text.extract_all_text()) or ""
                    OCR_engine = 'doc_parser'
                    
                elif ext in ('doc','odt','rtf'):
                    #text = UniversalDocParser(filepath)
                    text = 'NOT yet implemented for doc, odt and rtf files'
                    #extracted_text = str(text.extract_all_text()) or ""
                    extracted_text = "upload suitable file"
                    OCR_engine = 'doc_otf_rft_parser'
                    
                elif ext in ('jpg','jpeg','png'):
                    text = imageParser(filepath)
                    extracted_text = str(text.extract_all_text()) or ""
                    OCR_engine = 'image_parser'
                    
                elif ext == 'txt' or ext == 'md':
                    text = textParser(filepath)
                    extracted_text = str(text.extract_all_text()) or ""
                    OCR_engine = "text_parser"
                    
                else:
                    extracted_text = ""
                    OCR_engine = "unknown"
                    
            except Exception as e:
                resume.status = "Failed"
                db.session.commit()
                return jsonify({'success':False,'message': f'Failed to parse file: {str(e)}'}), 500
                
            if not extracted_text:
                resume.status = 'Failed'
                db.session.commit()
                return jsonify({'success': False,'message':'unable to extracte text'}), 422
                
            try:
                #response = chatGPTResponse(extracted_text)
                #gpt_result = response.get_response()
                gpt_result = extracted_text
            except Exception as e:
                resume.status = 'Failed'
                db.session.commit()
                return jsonify({'success': False, 'message': 'No gpt Result, rude gpt{str(e)}'}), 500
                
            resume.extracted_text = extracted_text
            resume.extracted_json = f"{file.filename}" + str(gpt_result)
            resume.ocr_engine = OCR_engine
            resume.status = "Completed"
            
            db.session.commit()
            
            resume_id.append(resume.id)
            resume_filenames.append(resume.filename)
            resume_engines.append(resume.ocr_engine)
            resume_json.append(resume.extracted_json)
        except:
            return jsonify({'success':False, 'message':f'error {e}'})
            
    return jsonify({
        'success': True,
        'resume_id': resume_id,
        'filename': resume_filenames,
        'ocr_engine': resume_engines,
        'extracted_json': resume_json
    }), 201
        
            
@resume_api_bp.route('/list',methods=['GET'])
@jwt_required()
def list():
    user_id = get_jwt_identity()
    items = Resume.query.filter_by(user_id = user_id).order_by(Resume.created_at.desc()).all()
    result = [{'id':r.id,
            'filename':r.filename,
            'extracted_json':r.extracted_json,
            'OCR_engine':r.ocr_engine,
            'status':r.status}
            for r in items]
    return jsonify({'success':True,'result': result}), 200
    
@resume_api_bp.route('/<int:resume_id>',methods=['GET'])
@jwt_required()
def view_resume(resume_id):
    user_id = get_jwt_identity()
    items = Resume.query.filter_by(id = resume_id, user_id = user_id).first_or_404()
    return jsonify({
        'success': True,
        'id': items.id,
        'filename': items.filename,
        'extracted_text': items.extracted_text,
        'extracted_json': items.extracted_json,
        'ocr_engine': items.ocr_engine,
        'status': items.status
    }), 200

@resume_api_bp.route('/<int:resume_id>',methods=['DELETE'])
@jwt_required()
def delete_resume(resume_id):
    user_id = get_jwt_identity()
    r = Resume.query.filter_by(id = resume_id, user_id = user_id).first_or_404()
    try:
        if os.path.exists(r.file_path):
            os.remove(r.file_path)
    except Exception as e:
        pass
        
    db.session.delete(r)
    db.session.commit()
    
    return jsonify({'success': True,'message':'deleted data'})


    
            
        