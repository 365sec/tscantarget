import netblock
import uuid
import os
import json

class TTarget():
    
    def __init__(self):
        self.ipranges=netblock.IPRanges()
        self.domains=[]
        self.ip_domain=[]
        
    
    def parse_dnsanswer(self,line):
        data=json.loads(line)
        iscname= False
        stat=data.get("status")
        domain = data.get("name")
        if stat == "NOERROR":
            for  answer in data.get("data",{}).get("answers",[]):
                if answer["type"] == "A" :
                    if iscname:
                        self.ip_domain.append((answer["answer"],domain ))
                        self.ipranges.addoddcidr(answer["answer"])
                        break 
                    self.ip_domain.append((answer["answer"],domain ))
                    self.ipranges.addoddcidr(answer["answer"])
                elif  answer["type"] == "CNAME" and domain == answer["name"]:
                    iscname=True
    
        
    def dns_parser(self):
        #./tdns  a  --timeout=25 --threads=1000 input-file=.tmp --output-file=  
        tmpinput="%s_input.tmp"%(uuid.uuid4())
        tmpoutput="%s_output.tmp"%(uuid.uuid4())
        cmdline="./tdns  a  --timeout=25 --threads=1000 --input-file=%s --output-file=%s"%(tmpinput,tmpoutput)
        finput=open(tmpinput,"wb")
        for domain in self.domains:
            finput.write("%s\n"%(domain))
        finput.close()
        #do dns parser
        os.system(cmdline)
        fdns=open(tmpoutput,"rb")
        for l in fdns:
            text =l.rstrip().lstrip()
            if text=="":
               continue
            else:
                self.parse_dnsanswer(text)
        fdns.close()
        
        #delete temp file
        os.remove(tmpinput)
        os.remove(tmpoutput)    
          
        
        
    def parser(self,target):
        try:
           f=open(target,"rb")
        except Exception as e:
            print "file %s not exit"%(target)
            return 
        for line in f :
          try:
            self.ipranges.addoddcidr(line.lstrip().rstrip())
          except Exception as e:
            self.domains.append(line.lstrip().rstrip())
        f.close()
       
        if len(self.domains) > 0 :
           self.dns_parser()
              
        tmpip="%s_ip.tmp"%(uuid.uuid4())
        tmpipdomain="%s_ipdomain.tmp"%(uuid.uuid4())
        
        lenip=len(self.ipranges)
        lenipdomain=len(self.ip_domain)
        
        fip=open(tmpip,"wb")
        fipdomain=open(tmpipdomain,"wb")
        
        for ips in self.ipranges.tocidr():
            fip.write("%s\n"%ips)
        fip.close()
        
        for ipdomain in self.ip_domain:
            fipdomain.write("%s,%s\n"%ipdomain)
        fipdomain.close()
        print "#[%d,%d,%s,%s]"%(lenip,lenipdomain,tmpip,tmpipdomain)
        
        
if __name__=="__main__":
    tt = TTarget()
    tt.parser("target.cvs")