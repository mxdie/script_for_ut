import json
import re


class fenci():
    def __init__(self,filename: str, NameRuleConf: dict, CompileConf: dict):
        self.filename= filename
        self.res = {'msg':666}
        self.group = ''
        self.res['upname'] = filename
        self.compilerule = CompileConf
        suportlist = list(NameRuleConf) 
        for group in suportlist:
            if group.lower() in filename.lower():
                self.group = group
                self.res['type'] = NameRuleConf[group][0]
                self.rule = NameRuleConf[group][1]
                break
        if not self.group:
            self.res['msg'] = 'suport error'
            return
        self.uprule = ''
        if isinstance(NameRuleConf[group][0],int):
            self.res['type'] = NameRuleConf[group][0]
            self.rule = NameRuleConf[group][1]
            if len(NameRuleConf[group]) ==3: self.uprule =NameRuleConf[group][2]
            self.fenci_()
        else:
            for i in NameRuleConf[group]:
                self.res['type'] = i[0]
                self.rule = i[1]
                if len(i) ==3: self.uprule =i[2]
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
        try:
            find = re.search(self.rule,self.filename,re.I)
            for canshu in list(dict):
                dict[canshu] = find.group(dict[canshu])
        except:
            self.res['msg'] = 'match error'
            return
        if  self.res['msg'] == 'match error':self.res['msg'] = 666
        self.res.update(dict)
        if self.uprule:
            dict['name'] = dict['name'].replace(' ','.')
            self.res['upname'] = self.uprule.format(**dict)
if __name__ == "__main__":
    pass
        

