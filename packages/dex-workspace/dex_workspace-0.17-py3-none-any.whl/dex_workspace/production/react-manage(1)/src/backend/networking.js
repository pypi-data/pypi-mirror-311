import { appIP } from "./otherInfo";
import { getPwd } from "./security";

const API_LINK = `http://${appIP}:5678`

async function makePostRequest(url, data1) {
    var data = {
        ...data1,
        pwd_hash: getPwd()
    };
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        const responseData = await response.json();
        console.log('Success:', responseData);
        return responseData;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

var api_url = `http://${appIP}:5678/ask`;

async function getProjects() {
    var data = {
        'route': 'get_projects',
    };
    return makePostRequest(api_url, data)
}

async function getScripts() {
    var data = {
        'route': 'get_scripts',
    };
    return makePostRequest(api_url, data)
}

async function getDatasets() {
    var data = {
        'route': 'get_datasets',
    };
    return makePostRequest(api_url, data)
}

async function getSharings() {
    var data = {
        'route': 'get_sharings',
    };
    return makePostRequest(api_url, data)
}

async function getShare(accessKey) {
    var data = {
        'route': 'get_share',
        'access_key': accessKey,
    };
    return makePostRequest(api_url, data)
}

async function renameData(name, dataID) {
    var data = {
        'route': 'rename_data',
        'name': name, 
        'data_id': dataID, 
    };
    return makePostRequest(api_url, data)
}

async function describeData(description, dataID) {
    var data = {
        'route': 'describe_data',
        'description': description, 
        'data_id': dataID, 
    };
    return makePostRequest(api_url, data)
}

async function addData2Share(dataID, accessKey) {
    var data = {
        'route': 'add_data_to_share',
        'access_key': accessKey, 
        'data_id': dataID, 
    };
    return makePostRequest(api_url, data)
}

async function removeDataAccess(dataID, accessKey) {
    var data = {
        'route': 'remove_data_access',
        'access_key': accessKey, 
        'data_id': dataID, 
    };
    return makePostRequest(api_url, data)
}


async function loadProjectInfo(projectID, ) {
    var data = {
        'route': 'load_project_info',
        'project_id': projectID, 
    };
    return makePostRequest(api_url, data)
}

async function loadProjectEnvs(projectID, ) {
    var data = {
        'route': 'load_project_envs',
        'project_id': projectID, 
    };
    return makePostRequest(api_url, data)
}

async function setProjectName(projectID, name) {
    var data = {
        'route': 'set_project_name',
        'project_id': projectID, 
        'name': name
    };
    return makePostRequest(api_url, data)
}

async function addProcess(projectID,) {
    var data = {
        'route': 'add_process',
        'project_id': projectID, 
    };
    return makePostRequest(api_url, data)
}

async function getEnvOptions() {
    var data = {
        'route': 'load_env_options',
    };
    return makePostRequest(api_url, data)
}

async function setProcessEnv(projectEnvID, envID) {
    var data = {
        'route': 'set_process_env',
        'project_env_id': projectEnvID, 
        'env_id': envID, 
    };
    return makePostRequest(api_url, data)
}

async function setProcessScript(projectEnvID, scriptID) {
    var data = {
        'route': 'set_process_script',
        'project_env_id': projectEnvID, 
        'script_id': scriptID, 
    };
    return makePostRequest(api_url, data)
}


async function getObjects(projectID, ) {
    var data = {
        'route': 'get_objects',
        'project_id': projectID, 
    };
    return makePostRequest(api_url, data)
}

async function deleteProcess(projectEnvID,) {
    var data = {
        'route': 'delete_process',
        'project_env_id': projectEnvID, 
    };
    return makePostRequest(api_url, data)
}

async function getEnvironments() {
    var data = {
        'route': 'get_environments',
    };
    return makePostRequest(api_url, data)
}

async function getRemoteEnv(accessKey) {
    var data = {
        'route': 'get_remote_env',
        'access_key': accessKey, 
    };
    return makePostRequest(api_url, data)
}


async function share(ipAddress, envName, dataIDs) {
    var data = {
        'route': 'share',
        ip_address: ipAddress, 
        env_name: envName, 
        data_ids: dataIDs,
    };
    return makePostRequest(api_url, data)
}


const handleDataFileUpload = async (event) => {
    console.log('do thing');
    const file = event.target.files[0];
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(`http://${appIP}:5678/upload_data`, { // Update with your FastAPI URL
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          return {status:1};
        } else {
          console.error("File upload failed");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
  };


async function getLogs(projectID) {
    var data = {
        'route': 'get_logs',
        'project_id': projectID
    };
    return makePostRequest(api_url, data)
}


async function streamLogs(projectID, numLogs) {
    var data = {
        'route': 'stream_logs',
        'project_id': projectID,
        'num_logs': numLogs, 
    };
    return makePostRequest(api_url, data)
}


const handleScriptUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    
    try {
        const response = await fetch( `${API_LINK}/upload_script`, { // Update with your FastAPI URL
            method: "POST",
            body: formData,
        });
        if (response.ok) {
            return {status:1};
        } else {
            console.error("File upload failed");
        }
    } catch (error) {
    console.error("Error uploading file:", error);
    }
};


async function renameScript(scriptID, name) {
    var data = {
        route: 'set_script_name',
        script_id: scriptID,
        name: name, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function deleteScript(scriptID,) {
    var data = {
        route: 'delete_script',
        script_id: scriptID,
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function removeObj(objectID,) {
    var data = {
        route: 'remove_obj',
        object_id: objectID,
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

const downloadObject = async (objectId) => {
    try {
      const response = await fetch(`${API_LINK}/download-object?object_id=${objectId}&_=${new Date().getTime()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
  
      if (!response.ok) {
        throw new Error('Download failed');
      }
      
      
      console.log(response);

      
      // Get the filename from the Content-Disposition header
      const contentDisposition = response.headers.get('Content-Disposition');
      if (!contentDisposition) {
        throw new Error('Filename not found in headers');
      }

      
      const filename = contentDisposition.split('filename=')[1].replace(/['"]/g, ''); // Remove quotes if any
  
      // Create blob from response
      const blob = await response.blob();
      
      // Create a download link and trigger the click to start the download
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename; // Use the filename from Content-Disposition
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };
  

  
async function runProject(projectID,) {
    var data = {
        route: 'run',
        project_id: projectID, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function terminateRun(projectID,) {
    var data = {
        route: 'terminate_run',
        project_id: projectID, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function newProject() {
    var data = {
        route: 'new_project',
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function removeSharing(accessKey) {
    var data = {
        route: 'remove_sharing',
        access_key: accessKey
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function setMainScriptDB(projectID, scriptID) {
    var data = {
        route: 'set_main_script',
        project_id: projectID, 
        script_id: scriptID, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}


async function updateScript(content, scriptID) {
    var data = {
        route: 'update_script',
        content: content, 
        script_id: scriptID, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}


async function deleteProjects(projectIDs) {
    var data = {
        route: 'delete_projects',
        project_ids: projectIDs, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}

async function checkPwd(pwd) {
    var data = {
        route: 'check_pwd',
        pwd: pwd, 
    };
    console.log(data);
    return makePostRequest(api_url, data)
}


export {
    getProjects, 
    getScripts,
    getDatasets, 
    getSharings, 
    getShare, 
    renameData, 
    describeData,
    addData2Share, 
    removeDataAccess, 
    loadProjectInfo, 
    loadProjectEnvs, 
    setProjectName, 
    addProcess,
    getEnvOptions, 
    setProcessEnv,
    setProcessScript,
    getObjects, 
    deleteProcess, 
    getEnvironments, 
    getRemoteEnv, 
    share, 
    handleDataFileUpload, 
    getLogs, 
    streamLogs,
    handleScriptUpload, 
    renameScript, 
    deleteScript, 
    removeObj, 
    downloadObject, 
    runProject, 
    terminateRun, 
    newProject,
    removeSharing, 
    setMainScriptDB, 
    updateScript, 
    deleteProjects, 
    checkPwd, 
}




