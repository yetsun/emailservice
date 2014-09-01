class ConfUtil:
    """
    This is the helper class to get the configuration from file
    """
    def __init__(self, path):
        self._conf = None
        self._path = path
    
    
    def parseConf(self):
        """
        Parse the configuration file and return an dict object
        """
        confFile = file(self._path, 'rU')
        self._conf = {}
        for line in confFile:
            line = line.strip()
            if len(line)  == 0:
                continue
            
            if line[0] in ('!', '#'):
                continue
                
            index = line.find('=')
            if index > 0 and index < (len(line) - 1):
                key = line[:index]
                value = line[index+1:]
                self._conf[key] = value
        
        
        #print self._dict
    
    def get(self, key):
        """
        Get the value from the configuration by the key
        return None if the key is not there
        """
        if not self._conf:
            self.parseConf()
        
        if self._conf.has_key(key):            
            return self._conf[key]
        else:
            return None