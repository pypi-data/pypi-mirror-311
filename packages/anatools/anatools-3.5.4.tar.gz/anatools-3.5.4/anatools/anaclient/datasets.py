"""
Dataset Functions
"""
import os
from anatools.anaclient.helpers import multipart_upload_file
from anatools.lib.download import download_file


def get_datasets(self, datasetId=None, name=None, email=None, workspaceId=None):
    """Queries the workspace datasets based off provided parameters. Checks on datasetId, name, owner in this respective order within the specified workspace.
    If only workspace ID is provided, this will return all the datasets in a workspace. 
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to filter.
    name : str 
        Dataset name.   
    email: str
        Owner of the dataset.
    workspaceId : str
        Workspace ID of the dataset's workspace. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Information about the dataset based off the query parameters provided or a failure message. 
    """
    if self.check_logout(): return
    if datasetId is None: datasetId = ''
    if name is None: name = ''
    if email is None: email = ''
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getDatasets(workspaceId=workspaceId, datasetId=datasetId, name=name, email=email)


def create_dataset(self, name, graphId, description='', runs=1, priority=1, seed=1, workspaceId=None):
    """Create a new dataset based off an existing staged graph. This will start a new job.
    
    Parameters
    ----------
    name: str
        Name for dataset. 
    graphId : str
        ID of the staged graph to create dataset from.
    description : str 
        Description for new dataset.
    runs : int
        Number of times a channel will run within a single job. This is also how many different images will get created within the dataset. 
    priority : int
        Job priority.
    seed : int
        Seed number.
    workspaceId : str
        Workspace ID of the staged graph's workspace. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset creation.
    """
    if self.check_logout(): return
    if name is None or graphId is None: return
    if description is None: description = ''
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createDataset(workspaceId=workspaceId, graphId=graphId, name=name, description=description, runs=runs, seed=seed, priority=priority)


def edit_dataset(self, datasetId, description=None, name=None, workspaceId=None):
    """Update dataset description.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to update description for.
    description : str 
        New description.
    name: str
        New name for dataset.
    workspaceId : str
        Workspace ID of the dataset to get updated. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset update.
    """
    if self.check_logout(): return
    if datasetId is None: return
    if workspaceId is None: workspaceId = self.workspace
    if name is None and description is None: return
    return self.ana_api.editDataset(workspaceId=workspaceId, datasetId=datasetId, name=name, description=description)
    

def delete_dataset(self, datasetId, workspaceId=None):
    """Delete an existing dataset.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID of dataset to delete.
    workspaceId : str
        Workspace ID that the dataset is in. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        Success or failure message about dataset deletion.
    """
    if self.check_logout(): return
    if datasetId is None: return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteDataset(workspaceId=workspaceId, datasetId=datasetId)
    

def download_dataset(self, datasetId, workspaceId=None, localDir=None):
    """Download a dataset.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID of dataset to download.
    workspaceId : str
        Workspace ID that the dataset is in. If none is provided, the default workspace will get used. 
    localDir : str
        Path for where to download the dataset. If none is provided, current working directory will be used.
        
    Returns
    -------
    str
        Success or failure message about dataset download.
    """
    if self.check_logout(): return
    if datasetId is None: datasetId
    if workspaceId is None: workspaceId = self.workspace    
    url = self.ana_api.downloadDataset(workspaceId=workspaceId, datasetId=datasetId)        
    fname = self.ana_api.getDatasets(workspaceId=workspaceId, datasetId=datasetId)[0]['name'] + '.zip'
    return download_file(url=url, fname=fname, localDir=localDir) 


def cancel_dataset(self, datasetId, workspaceId=None):
    """Stop a running job.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID of the running job to stop.
    workspaceId: str
        Workspace ID of the running job. If none is provided, the default workspace will get used. 
    
    Returns
    -------
    str
        Success or error message about stopping the job execution.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.cancelDataset(workspaceId=workspaceId, datasetId=datasetId)


def upload_dataset(self, filename, description=None, workspaceId=None):
    """Uploads user dataset using multipart upload with 8 threads.
    
    Parameters
    ----------
    filename: str
        Path to the dataset folder or file for uploading. Must be zip or tar file types.
    workspaceId : str
        WorkspaceId to upload dataset to. Defaults to current.
    description : str
        Description for new dataset.
    
    Returns
    -------
    datasetId : str
        The unique identifier for this dataset.
    """
    if self.check_logout(): return
    if filename is None: raise ValueError("Filename must be defined.")
    if description is None: description = ''
    if workspaceId is None: workspaceId = self.workspace
    if os.path.splitext(filename)[1] not in ['.zip', '.tar', '.gz']: raise Exception('Dataset Upload is only supported for zip, tar, and tar.gz files.')
    if not os.path.exists(filename): raise Exception(f'Could not find file: {filename}')
    self.refresh_token()

    filesize = os.path.getsize(filename)
    fileinfo = self.ana_api.datasetUpload(workspaceId=workspaceId, filename=filename, filesize=filesize, description=description)
    datasetId = fileinfo['datasetId']

    parts = multipart_upload_file(filename, fileinfo["partSize"], fileinfo["urls"], f"Uploading dataset {filename}")
    self.refresh_token()
    finalize_success = self.ana_api.datasetUploadFinalizer(workspaceId, fileinfo['uploadId'], fileinfo['key'], parts)
    if not finalize_success:
        raise Exception(f"Failed to upload dataset {filename}.")
    else:
        print(f"\x1b[1K\rUpload completed successfully!", flush=True)
        return datasetId


def get_dataset_runs(self, datasetId, state=None, workspaceId=None):
    """Shows all dataset run information to the user. Can filter by state.
    
    Parameters
    ----------
    datasetId: str
        The dataset to retrieve logs for.
    state: str
        Filter run list by status.
    workspaceId : str
        The workspace the dataset is in.
    
    Returns
    -------
    list[dict]
        List of run associated with datasetId.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    runs = self.ana_api.getDatasetRuns(workspaceId=workspaceId, datasetId=datasetId, state=state)
    if runs: return runs
    else: return None
                

def get_dataset_log(self, datasetId, runId, saveLogFile=False, workspaceId=None):
    """Shows dataset log information to the user.
    
    Parameters
    ----------
    datasetId: str
        The dataset the run belongs to.
    runId: str
        The run to retrieve the log for.
    saveLogFile: bool
        If True, saves log file to current working directory.
    workspaceId: str
        The workspace the run belongs to.
    
    Returns
    -------
    list[dict]
        Get log information by runId
    """
    import json 

    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    log = self.ana_api.getDatasetLog(workspaceId=workspaceId, datasetId=datasetId, runId=runId)
    if log['log']: 
        if saveLogFile:
            with open (f"{datasetId}-{log['run']}.log",'w+') as logfile:
                for line in json.loads(log['log']): logfile.write(f"{line['message']}\n")
            print(f"Saved log to {datasetId}-{log['run']}.log")
        else: return log['log']
    else: return None