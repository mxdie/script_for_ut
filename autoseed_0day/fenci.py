import json
import re


class fenci():
    def __init__(self,filename: str):
        self.filename= filename
        self.res = {'msg':666}
        self.group = ''
        try:
            with open('config.json','r') as f:
                config = json.load(f)
            namerule = config['namerule']
            self.compilerule = config['compile']
            suportlist = list(namerule) 
        except:
            self.res['msg'] = 'load config error'
        for group in suportlist:
            if group.lower() in filename.lower():
                self.group = group
                self.res['type'] = namerule[group][0]
                self.rule = namerule[group][1]
                break
        if not self.group:
            self.res['msg'] = 'suport error'
            return
        if isinstance(namerule[group][0],int):
            self.res['type'] = namerule[group][0]
            self.rule = namerule[group][1]
            self.fenci_()
        else:
            for i in namerule[group]:
                self.res['type'] = i[0]
                self.rule = i[1]
                self.fenci_()
                if self.res['msg'] == 666:break



    def fenci_(self):
        n = 0
        dict = {}
        self.rule = self.rule.replace('[',r'\[')
        self.rule = self.rule.replace(']',r'\]')
        for i in re.findall(r'(\w+)',self.rule):
            if i in list(self.compilerule):
                if i =='group':
                    self.rule = self.rule.replace(i,'('+self.group+')')
                else:
                    self.rule = self.rule.replace(i,self.compilerule[i])
                n+=1
                dict[i] = n
            else:
                self.res['msg'] = 'namerule error'
                return
        try:
            find = re.search(self.rule,self.filename,re.I)
            for canshu in list(dict):
                dict[canshu] = find.group(dict[canshu])
        except:
            self.res['msg'] = 'match error'
            return
        self.res.update(dict)

info = fenci('[DMG] 劇場版 夜は短し歩けよ乙女 [BDRip]')
print(info.res)