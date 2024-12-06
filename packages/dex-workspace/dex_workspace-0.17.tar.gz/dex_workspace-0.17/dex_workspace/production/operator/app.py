import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)))



from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from operations import projects, data, sharing, environments, running, scripts, security
from tools.database import lite_client
from tools.storage import get_path
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--app_ip')
app_args = parser.parse_args()

app_ip = app_args.app_ip


port = 5678

os.environ['PORT'] = str(port)

cmd = "PORT=5678 /usr/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 5678"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length", "Content-Type"],
)

tasks = { 
    'get_projects': projects.get_projects,
    'get_scripts': projects.get_scripts, 
    'get_datasets': data.get_datasets,
    'get_sharings': sharing.get_shares,
    'get_share': sharing.get_share, 
    'rename_data': data.set_data_name, 
    'describe_data': data.describe_data, 
    'add_data_to_share': data.add_data_to_share, 
    'remove_data_access': data.remove_data_access, 
    'load_project_info': projects.load_project_info, 
    'load_project_envs': projects.load_project_envs, 
    'set_project_name': projects.set_project_name, 
    'add_process': projects.add_process,
    'load_env_options': projects.load_env_options, 
    'set_process_env': projects.set_process_env, 
    'set_process_script': projects.set_process_script, 
    'get_objects': projects.get_objects,
    "delete_process": projects.delete_process, 
    'get_environments': environments.get_environments, 
    'get_remote_env': sharing.get_remote_env,
    'receive_invite': sharing.receive_invite,
    'share': sharing.share, 
    'run': running.run, 
    'get_logs': running.get_logs, 
    'run_request': running.run_request, 
    'terminate_run':running.terminate_run, 
    'terminate_request':running.terminate_request,
    'stream_logs':running.stream_logs,
    'set_script_name': scripts.set_script_name, 
    'delete_script': scripts.delete_script, 
    'delete_data': data.delete_data, 
    'remove_obj': environments.remove_object, 
    'new_project': projects.create_new_project, 
    'remove_sharing': sharing.remove_sharing, 
    'set_main_script': scripts.set_main_script, 
    'update_script': scripts.update_script, 
    'delete_projects': projects.delete_projects,
    'check_pwd': security.check_pwd, 
}

@app.post('/ask')
async def get_projects(request: Request):
    try:
        data = await request.json()
        #print(data)
        if not security.match_pwd(data['pwd_hash']) or data['pwd_hash'] is None:
            if data['route'] != 'check_pwd':
                return JSONResponse({'status': 0})

        response = tasks[data['route']](data)
        return JSONResponse(response)
    except:
        raise HTTPException(404, detail='error')
    


@app.get('/get')
async def get():
    return JSONResponse({'message': 'works perfectly'})

app.post('/upload_data')(data.upload_file)
app.post('/upload_script')(scripts.upload_script)




@app.get("/download-object")
async def download_file(object_id: str):
    # Retrieve filename from the database using object_id
    try:
        cmd = "SELECT name FROM objects WHERE object_id = ?"
        result = lite_client.select(cmd, (object_id,))
        
        if not result:
            raise HTTPException(status_code=404, detail="File not found")
        
        filename = result[0]['name']
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error") from e

    # Generate file path and check if it exists
    file_path = get_path(filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Return file with Content-Disposition header
    r =  FileResponse(
        path=file_path,
        filename=filename,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
        media_type="application/octet-stream"
    )


    return r

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host=app_ip, port=port, reload=True)
