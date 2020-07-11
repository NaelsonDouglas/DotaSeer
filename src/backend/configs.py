class Configs:    
    def __init__(self):
        import json        
        allConfigsProfiles = json.load(open('../configs.json'))
        selectedProfile = allConfigsProfiles['selected_profile']
        profiles = allConfigsProfiles['profiles']        
        self.selectedProfile = selectedProfile
        self.configs = profiles[selectedProfile]
    def get(self, field):        
        return  self.configs[field]