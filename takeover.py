#!/usr/bin/env python
# -*- coding: utf-8 -*-
#SubDomain Takeover Scanner by 0x94

import Queue
import threading
import sys
import optparse
import requests
from lib.TerminalSize import get_terminal_size
import platform
from thirdparty.colorama import *
import time

if platform.system() == 'Windows':
    from thirdparty.colorama.win32 import *
    
queue = Queue.Queue()
progress=0
lastInLine = False

try:
    import dns.resolver
except:
    print("You need to install dnspython")
    sys.exit(1)




class hazirla:
    def __init__(self,domain,wordlist,thread):
        self.domain=domain
        self.wordlist=wordlist
        self.thread=thread
        
    def thbaslat(self,sublar,num_lines):
        
        lock    = threading.Lock()
        
        for subum in sublar:
            if subum.strip():
                queue.put(subum.strip()+"."+self.domain)
                
        threads = []
        exit = threading.Event()
                
        for i in range(self.thread):
            t = DnsSorgu(queue,lock,num_lines,exit)
            t.setDaemon(True)
            threads.append(t)
            t.start()
            
        try:
            queue.join() 
        except KeyboardInterrupt:
            print "Exit"
            sys.exit(1)        

            
        
    def main(self):
        try:
            num_lines = sum(1 for line in open(self.wordlist))            
            dosya  = open(self.wordlist)
        except IOError:
            print "File not found %s" % (self.wordlist)
            sys.exit(0)
        try:
            self.thbaslat(dosya.xreadlines(),num_lines) 
        except (KeyboardInterrupt,SystemExit):
            print "Cancelled"
            exit()
            
class DnsSorgu(threading.Thread):
    def __init__(self, queue,lock,num_lines,exit):
        threading.Thread.__init__(self)
        self.queue      = queue
        self.lock       = lock
        self.num_lines = num_lines
        self.exit = exit
                 
        self.firma={"createsend":"https://www.zendesk.com/",
                    "cargocollective":"https://cargocollective.com/",
                    "cloudfront":"https://aws.amazon.com/cloudfront/",
                    "desk.com":"https://www.desk.com/",
                    "fastly.net":"https://www.fastly.com/",
                    "feedpress.me":"https://feed.press/",
                    "ghost.io":"https://ghost.org/",
                    "helpjuice.com":"https://helpjuice.com/",
                    "helpscoutdocs.com":"https://www.helpscout.net/",
                    "herokudns.com":"https://www.heroku.com/",
                    "herokussl.com":"https://www.heroku.com/",
                    "herokuapp.com":"https://www.heroku.com/",
                    "jetbrains.com":"https://myjetbrains.com/",
                    "pageserve.co":"https://instapage.com/",
                    "pingdom.com":"https://www.pingdom.com/",
                    "amazonaws.com":"https://aws.amazon.com/s3/",
                    "myshopify.com":"https://www.shopify.com/",
                    "stspg-customer.com":"https://www.statuspage.io/",
                    "sgizmo.com":"https://www.surveygizmo.com/",
                    "surveygizmo.eu":"https://www.surveygizmo.com//",
                    "sgizmoca.com":"https://www.surveygizmo.com/",
                    "teamwork.com":"https://www.teamwork.com/",
                    "tictail.com":"https://tictail.com/",
                    "domains.tumblr.com":"https://www.tumblr.com/",
                    "unbouncepages.com":"https://unbounce.com/",
                    "uservoice.com":"https://www.uservoice.com/",
                    "bitbucket":"https://bitbucket.org/",
                    "unbounce.com":"https://unbounce.com/",
                    "vend":"https://vendcommerce.com/",
                    "zendesk.com":"https://www.zendesk.com/"}    
        
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
                        "The requested URL was not found on this server",
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
                            
                            message = '[{0}] {1} - {2} - {3}'.format(
                                        time.strftime('%H:%M:%S'),
                                       gelenq,
                                        answers.qname,
                                        rdata.target.to_text()
                                    )
                            
                        
                            self.newLine(message)
                            
                            self.domaindel(rdata.target.to_text())
                            self.takeover(rdata.target.to_text(),gelenq)                    
                    except:
                        hata ="hata"                
                    #answers.timeout = 0.2
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
            print Style.BRIGHT+self.error+yaz+Style.RESET_ALL
            self.filewrite(yaz)
            return False
    
    
    def detect(self,subdomain):
        try:
            subrespon=requests.get("http://"+subdomain).text      
            for finder in self.response:
                if finder in subrespon:
                    self.filewrite("--- TAKEOVER DETECTED !!! : "+subdomain+Style.RESET_ALL)
                    print self.error+"--- TAKEOVER DETECTED !!! : "+subdomain+ Style.RESET_ALL
        except Exception as e:
            for finder in self.response:
                if finder in subrespon:
                    self.filewrite("--- TAKEOVER DETECTED !!! : "+subdomain+Style.RESET_ALL)
                    print self.error+"--- TAKEOVER DETECTED !!! : "+subdomain+Style.RESET_ALL         
        
    def filewrite(self,veri):
        open("takeover.txt","a+").write(veri+"\n")
                
    def takeover(self,domain,subdomain):
        for firmap in self.firma.keys():
            if firmap in str(domain):
                yollanacak="-- Company: "+firmap+" WebSite :"+self.firma[firmap]
                self.filewrite(subdomain+" --> "+str(domain)+yollanacak+"\n")
                print self.info+yollanacak+Style.RESET_ALL
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
            type   = "string", 
            help = "example: ./takeover.py -d host.com")
        parser.add_option('-w',
            action = "store", 
            dest   = "wordlist",
            type   = "string", 
            help = "example: ./takeover.py -d host.com -w wordlist.txt ")  
        parser.add_option('-t',
            action = "store", 
            dest   = "thread",
            type   = "int", 
            help = "example: ./takeover.py -d host.com -w wordlist.txt  -t 10")        
        (option,args) = parser.parse_args()
        
        if not option.domain:
            print "example: ./takeover.py -d host.com -w wordlist.txt  -t 10" 
            sys.exit(0)   
            
        if not option.wordlist:
            print "example: ./takeover.py -d host.com -w wordlist.txt" 
            sys.exit(0)  
            
        if option.thread:
            threadsayisi=option.thread
        else:
            threadsayisi=20
            
           
            
        print"""
        #######################################################
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #              SubDomain TakeOver v1.5                #
        #                    Coder: 0x94                      #
        #                  twitter.com/0x94                   #
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #######################################################  
        """          
        x=hazirla(option.domain,option.wordlist,threadsayisi)
        x.main()    
    except KeyboardInterrupt:
        print('\n Exit.')
        sys.exit(0)
