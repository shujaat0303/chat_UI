from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from helper.deepinfra_llama3_2 import query_bot
import os
import base64

app = Flask(__name__, static_folder='./build')
CORS(app)

# Endpoint to prompt the chatbot with text or multimodal input
@app.route('/api/prompt_bot', methods=['POST'])
def prompt_bot():
    data = request.json
    messages = data.get('messages', [])
    prompt = data.get('prompt', '')
    
    # Check if there's an image in the request (base64 or image file path)
    image_base64 = data.get('image_base64')
    
    if image_base64:
        # Save the image temporarily if it's sent as base64
        image_data = base64.b64decode(image_base64)
        image_path = 'temp_image.png'
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        
        # Call query_bot with the image path
        response = query_bot(messages, prompt, image_path=image_path)
        
        # Optionally, delete the image after processing
        os.remove(image_path)
    else:
        # Regular text prompt (no image)
        response = query_bot(messages, prompt)

    return jsonify({'messages': response, 'status': 'Prompt processed'}), 200
  
#react apps route handler
@app.route('/', defaults={'path1': '', 'path2': '','path3': ''})
@app.route('/<path:path1>', defaults={'path2': '','path3': ''})
@app.route('/<path:path1>/<path:path2>',defaults={'path3': ''})
@app.route('/<path:path1>/<path:path2>/<path:path3>')
def serve(path1,path2,path3):
     path = f'/{path1}/{path2}/{path3}'.rstrip('/')
     path_dir = os.path.abspath("./build") #path react build
    #  path_dir = '/home/shujaat/Work/ClouxiPlexi/Training/8_UI_framework_React/flask_react_auth/backend/build'
     full_path=os.path.join(path_dir,path1,path2,path3).rstrip('/')
     full_path_dir=os.path.join(path_dir,path1,path2).rstrip('/')
     if path != "" and os.path.exists(full_path):
         if '.' in full_path_dir.split('/')[-1]:
             path3=full_path_dir.split('/')[-1]
             full_path_dir=full_path_dir.replace(full_path_dir.split('/')[-1],'').rstrip('/')
         return send_from_directory(full_path_dir, path3)
     else:
         return send_from_directory(os.path.join(path_dir),'index.html')


if __name__ == "__main__":
    app.run(debug=True)