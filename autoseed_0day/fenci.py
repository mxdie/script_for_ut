import json
import re
with open('config.json','r') as f:
    config = json.load(f)
namerule = config['namerule']
compilerule = config['compile']
suportlist = list(namerule) 

class fenci():
    def __init__(self,filename: str):
        self.filename= filename
        self.res = {'msg':666}
        self.group = ''
        for group in suportlist:
            if group.lower() in filename.lower():
                self.group = group
                self.res['type'] = namerule[group][0]
                self.rule = namerule[group][1]
                break
        if not self.group:
            self.res['msg'] = 0
            return
        if namerule[group][0]==401: self.movie()

    def movie(self):
        n = 0
        dict = {}
        for i in list(compilerule):
            if i in self.rule:
                self.rule = self.rule.replace(i,compilerule[i])
                n+=1
                dict[i] = n
        if 'group' in self.rule:
            self.rule = self.rule.replace('group','('+self.group+')')
            n+=1
            dict[i] = n
        try:
            find = re.search(self.rule,self.filename,re.I)
        except:
            self.res['msg'] = 1
            return
        for canshu in list(dict):
            dict[canshu] = find.group(dict[canshu])
        self.res.update(dict)

info = fenci('Herstory.2018.1080p.BluRay.x264.DTS-WiKi')
print(info.res)