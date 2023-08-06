import os
from helpers import getCaller, getCurrentDateTime, getFileSize, generateRandomId


class Logger:
    
    def __init__(self, fileName=None):

        log_dir = os.path.join(os.getcwd(), 'logs')
        
        #check if there is no logs directory
        os.makedirs(log_dir, exist_ok=True)
            
        if fileName is not None:
            if self._checkString(fileName):
                self.fileName = fileName
            else:
                raise TypeError("Invalid type for a fileName, it can only be a string")
            
        else:
            self.fileName = 'logs.log'
        
        self.log_path = os.path.join(log_dir, self.fileName)
        
    
    def log(self, message):
        
        ctime = getCurrentDateTime()
        caller = getCaller()
        genId = generateRandomId(16)
        
        try:
            with open(self.log_path, 'a+') as f:
                f.write(f"{genId}\t{ctime}\t{caller}:\t\t{message}\n")

        except IOError as e:
            print(f"Error opening file: {e}")
            raise
        
        return genId
        
    
    def read_all_logs(self):
        if getFileSize(self.log_path) > 0:
            
            try:
                with open(self.log_path, 'r') as f:
                    logs = f.read()
                
                return logs
            
            except IOError as e:
                print(f"Error opening file: {e}")
                raise
            
        else:
            print("log file is empty")
            return None
    
    
    def getLogWithId(self, id):
        if getFileSize(self.log_path) > 0:
            try:
                with open(self.log_path, 'r') as f:
                    for line in f:
                        if line.startswith(id):
                            return line
                
                print(f"No log found with id {id}")
                return None
                
            except IOError as e:
                print(f"Error opening file: {e}")
                raise
            
        else:
            print("log file is empty")
            return None
   
   
    def clear_all_logs(self):
        try:
            with open(self.log_path, 'w') as f:
                pass
            
        except IOError as e:
            print(f"Error opening file: {e}")
            raise        
    
    
    def _checkString(self, value):
        return isinstance(value, str)
    
    
    
    
    
    