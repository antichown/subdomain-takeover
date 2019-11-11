#!/usr/bin/env python
# -*- coding: utf-8 -*-
#SubDomain Takeover Scanner by 0x94

import threading
import sys
import optparse
import requests
from lib.TerminalSize import get_terminal_size
import platform
from thirdparty.colorama import *
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if platform.system() == 'Windows':
    from thirdparty.colorama.win32 import *
 
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue
    queue = Queue.Queue()
    
else:
    import queue as queue
    queue = queue.Queue()
    
        
progress=0
lastInLine = False

try:
    import dns.resolver
except:
    print("You need to install dnspython")
    sys.exit(1)




class hazirla:
    def __init__(self,domain,wordlist,thread,filem):
        self.domain=domain
        self.wordlist=wordlist
        self.thread=thread
        self.filem=filem
        
    def thbaslat(self,sublar,num_lines):
        
        lock    = threading.Lock()
        
        for subum in sublar:
            if subum.strip():
                if self.filem!="":
                    queue.put(subum.strip())
                else:
                    queue.put(subum.strip()+"."+self.domain)
                    
                
        threads = []
        exit = threading.Event()
                
        for i in range(self.thread):
            t = DnsSorgu(queue,lock,num_lines,exit,self.filem)
            t.setDaemon(True)
            threads.append(t)
            t.start()
            
        try:
            queue.join() 
        except KeyboardInterrupt:
            print("Exit")
            sys.exit(1)        

            
        
    def main(self):
        try:
            if self.filem!="":
                num_lines = sum(1 for line in open(self.filem))            
                dosya  = open(self.filem)                
            else:
                num_lines = sum(1 for line in open(self.wordlist))            
                dosya  = open(self.wordlist)
 
        except IOError:
            if self.filem!="":
                print("File not found %s" % (self.filem))
            else:
                print("File not found %s" % (self.wordlist))
            sys.exit(0)
        try:
            self.thbaslat(dosya.readlines(),num_lines) 
        except (KeyboardInterrupt,SystemExit):
            print("Cancelled")
            exit()
            
class DnsSorgu(threading.Thread):
    def __init__(self, queue,lock,num_lines,exit,filem):
        threading.Thread.__init__(self)
        self.queue      = queue
        self.lock       = lock
        self.num_lines = num_lines
        self.exit = exit
        self.filem=filem
                 
        self.response=["<strong>Trying to access your account",
                       "Use a personal domain name",
                        "The request could not be satisfied",
                        "Sorry, We Couldn't Find That Page",
                        "Fastly error: unknown domain",
                        "The feed has not been found",
                        "You can claim it now at",
                        "Publishing platform",                        
                        "<title>No such app</title>",                        
                        "No settings were found for this company",
                        "<title>No such app</title>",
                        "is not a registered InCloud YouTrack.",
                        "You've Discovered A Missing Link. Our Apologies!",
                        "Sorry, couldn&rsquo;t find the status page",                        
                        "NoSuchBucket",
                        "Sorry, this shop is currently unavailable",
                        "<title>Hosted Status Pages for Your Company</title>",
                        "data-html-name=\"Header Logo Link\"",                        
                        "<title>Oops - We didn't find your site.</title>",
                        "class=\"MarketplaceHeader__tictailLogo\"",                        
                        "Whatever you were looking for doesn't currently exist at this address",
                        "The page you have requested does not exist",
                        "This UserVoice subdomain is currently available!",
                        "but is not configured for an account on our platform",
                        "Looks like you've traveled too far into cyberspace.",
                        "The specified bucket does not exist",
                        "Bad Request: ERROR: The request could not be satisfied",
                        "Please try again or try Desk.com free for",
                        "We could not find what you're looking for",
                        "No Site For Domain",
                        "Project doesnt exist... yet!",
                        "project not found",
                        "Please renew your subscription",
                        "Double check the URL or <a href=\"mailto:help@createsend.com",
                        "There is no portal here",
                        "You may have mistyped the address or the page may have moved",
                        "Repository not found",
                        "<title>404 &mdash; File not found</title>",
                        "This page is reserved for artistic dogs",
                        "<h1>The page you were looking for doesn",
                        "<h1>https://www.wishpond.com/404?campaign=true",
                        '<p class="bc-gallery-error-code">Error Code: 404</p>',
                        "<h1>Oops! We couldn&#8217;t find that page.</h1>",
                        "Unrecognized domain <strong>",
                        "NoSuchKey",
                        "The specified key does not exist",
                        "<title>Help Center Closed | Zendesk</title>"]
        
        self.success = Fore.GREEN 
        self.error = Fore.RED 
        self.info = Fore.YELLOW  
    def run(self):
        try:
            while True:
                if self.exit.is_set():
                    break    
                with self.lock:
                    global progress
                    
                    if progress<self.num_lines:
                        progress+=1
                        
                    gelenq=self.queue.get()
                    
                    
                    percentage = lambda x, y: float(x) / float(y) * 100
                
                    x, y = get_terminal_size()
                
                    message = '{0:.2f}% - {aa}/{bb} '.format(percentage(progress, self.num_lines),aa=progress,bb=self.num_lines)
                
                
                    message += 'Scanning: {0}'.format(gelenq)
                
                    if len(message) > x:
                        message = message[:x]
                    
                    self.inLine(message) 
                    
                
                    
                    try:
                        answers = dns.resolver.query(gelenq, 'CNAME')
                        for rdata in answers:
                            
                            message = '[{0}] {1} - {2} -  Cname -> {3}'.format(
                                        time.strftime('%H:%M:%S'),
                                       gelenq,
                                        answers.qname,
                                        Fore.YELLOW+rdata.target.to_text()+Style.RESET_ALL
                                    )
                            
                        
                            self.newLine(message)
                            
                            self.domaindel(rdata.target.to_text())
                            self.takeover(rdata.target.to_text(),gelenq)                    
                    except:
                        hata ="hata"                
                        #answers.timeout = 0.5
                        #answers.lifetime = 0.10
                    
              
                      
                    self.queue.task_done() 
        except StopIteration:
            return        
        
    
    def domaindel(self,cname):
        try:
            dns.resolver.query(cname)
            return True
        except:
            yaz="Cname not  resolved "+cname
            print(Style.BRIGHT+self.error+yaz+Style.RESET_ALL)
            self.filewrite(yaz)
            return False
    
    
    def detect(self,subdomain):
        try:
            subrespon=requests.get("http://"+subdomain,verify=False).text      
            for finder in self.response:
                if finder in subrespon:
                    self.filewrite("--- TAKEOVER DETECTED !!! : "+subdomain)
                    print(self.error+"--- TAKEOVER DETECTED !!! : "+subdomain+ "\n Message="+finder+Style.RESET_ALL)
        except Exception as e:
            a="error"        
        
    def filewrite(self,veri):
        open("takeover.txt","a+").write(veri+"\n")
                
    def takeover(self,domain,subdomain):
        self.detect(subdomain)
                
    def erase(self):
        if platform.system() == 'Windows':
            csbi = GetConsoleScreenBufferInfo()
            line = "\b" * int(csbi.dwCursorPosition.X)
            sys.stdout.write(line)
            width = csbi.dwCursorPosition.X
            csbi.dwCursorPosition.X = 0
            FillConsoleOutputCharacter(STDOUT, ' ', width, csbi.dwCursorPosition)
            sys.stdout.write(line)
            sys.stdout.flush()
        else:
            sys.stdout.write('\033[1K')
            sys.stdout.write('\033[0G')
            
    def newLine(self,string):
        global lastInLine
        if lastInLine == True:
            self.erase()
            
            
        if platform.system() == 'Windows':
            sys.stdout.write(string)
            sys.stdout.flush()
            sys.stdout.write('\n')
            sys.stdout.flush()
    
        else:
            sys.stdout.write(string + '\n')
            
        sys.stdout.flush()
        lastInLine = False
        sys.stdout.flush()
        
    def inLine(self,string):
        global lastInLine
        self.erase()
        sys.stdout.write(string)
        sys.stdout.flush()
        lastInLine = True      
   
    

if __name__ == '__main__':
    try: 
        if platform.system() == 'Windows':
            init(autoreset=True) #windows icin        
        parser = optparse.OptionParser()
        parser.add_option('-d',
            action = "store", 
            dest   = "domain",
            type   = "string")
        parser.add_option('-w',
            action = "store", 
            dest   = "wordlist",
            type   = "string")  
        parser.add_option('-t',
            action = "store", 
            dest   = "thread",
            type   = "int")   
        
        parser.add_option('-f',
            action = "store", 
            dest   = "filem",
            type   = "string") 
        
        (option,args) = parser.parse_args()
        
        if not option.domain:
            print("example: ./takeover.py -d host.com -w wordlist.txt  -t 10 or | ./takeover.py -d host.com -f sublist.txt  -t 10 ")
            sys.exit(0)   
        
            
        if option.thread:
            threadsayisi=option.thread
        else:
            threadsayisi=20
            
           
            
        print("""
        #######################################################
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #              SubDomain TakeOver v1.5                #
        #                    Coder: 0x94                      #
        #                  twitter.com/0x94                   #
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #######################################################  
        """)          
        if option.filem:
            x=hazirla(option.domain,option.wordlist,threadsayisi,option.filem)
        else:
            x=hazirla(option.domain,option.wordlist,threadsayisi,"")
        x.main()    
    except KeyboardInterrupt:
        print('\n Exit.')
        sys.exit(0)
