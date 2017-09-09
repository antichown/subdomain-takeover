#!/usr/bin/env python
# -*- coding: utf-8 -*-
#SubDomain Takeover Scanner by 0x94

import Queue
import threading
import sys
import optparse
import requests
import colorama

queue = Queue.Queue()

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
        
    def thbaslat(self,sublar):
        
        lock    = threading.Lock()
        for subum in sublar:
            if subum.strip():
                queue.put(subum.strip()+"."+self.domain)
                
        threads = []
                
        for i in range(self.thread):
            t = DnsSorgu(queue,lock)
            t.setDaemon(True)
            threads.append(t)
            t.start()
            
        try:
            for x in threads:
                t.join() 
        except KeyboardInterrupt:
            print "Exit"
            sys.exit(1)        

            
        
    def main(self):
        try:
            dosya  = open(self.wordlist)
        except IOError:
            print "File not found %s" % (self.wordlist)
            sys.exit(0)
        try:
            self.thbaslat(dosya.xreadlines()) 
        except (KeyboardInterrupt,SystemExit):
            self.stop = True
            print "Cancelled"
            exit()
            
class DnsSorgu(threading.Thread):
    def __init__(self, queue,lock):
        threading.Thread.__init__(self)
        self.queue      = queue
        self.lock       = lock
           
        
        self.firma={"createsend":"https://www.zendesk.com/",
                    "cargocollective":"https://cargocollective.com/",
                    "cloudfront":"https://aws.amazon.com/cloudfront/",
                    "desk.com":"https://www.desk.com/",
                    "fastly.net":"https://www.fastly.com/",
                    "feedpress.me":"https://feed.press/",
                    "freshdesk.com":"https://freshdesk.com/",
                    "ghost.io":"https://ghost.org/",
                    "github.io":"https://pages.github.com/",
                    "helpjuice.com":"https://helpjuice.com/",
                    "helpscoutdocs.com":"https://www.helpscout.net/",
                    "herokudns.com":"https://www.heroku.com/",
                    "herokussl.com":"https://www.heroku.com/",
                    "herokuapp.com":"https://www.heroku.com/",
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
                    "wpengine.com":"https://wpengine.com/",
                    "bitbucket":"https://bitbucket.org/",
                    "squarespace.com":"https://www.squarespace.com/",
                    "unbounce.com":"https://unbounce.com/",                    
                    "zendesk.com":"https://www.zendesk.com/"}    
        
        self.response=["<strong>Trying to access your account",
                       "Use a personal domain name",
                        "The request could not be satisfied",
                        "Sorry, We Couldn't Find That Page",
                        "Fastly error: unknown domain",
                        "The feed has not been found",
                        "You can claim it now at",
                        "Publishing platform",                        
                        "There isn't a GitHub Pages site here",
                        "<title>No such app</title>",                        
                        "No settings were found for this company",
                        "<title>No such app</title>",                        
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
                        "<title>Help Center Closed | Zendesk</title>"]
        
        self.success = colorama.Fore.GREEN 
        self.error = colorama.Fore.RED   
        self.info = colorama.Fore.YELLOW  
    def run(self):
        while not self.queue.empty(): 
            try:
                gelenq=self.queue.get()
                sys.stdout.write("Scanning : "+gelenq + "                                     \r")
                sys.stdout.flush()                
                answers = dns.resolver.query(gelenq, 'CNAME')
                #answers.timeout = 0.2
                #answers.lifetime = 0.10
                for rdata in answers:
                    self.lock.acquire()
                    print answers.qname,' CNAME:', rdata.target.to_text()
                    self.domaindel(rdata.target.to_text())
                    self.takeover(rdata.target.to_text(),gelenq)
                    self.lock.release()
            except:
                hata ="hata"
               
            self.queue.task_done() 
    
    
    def domaindel(self,cname):
        try:
            dns.resolver.query(cname)
            return True
        except:
            yaz="Cname NOT Resolved "+cname
            print self.error+yaz
            self.filewrite(yaz)
            return False
    
    
    def detect(self,subdomain):
        try:
            subrespon=requests.get("http://"+subdomain).text      
            for finder in self.response:
                if finder in subrespon:
                    self.filewrite("--- TAKEOVER DETECTED !!! : "+subdomain)
                    print self.error+"--- TAKEOVER DETECTED !!! : "+subdomain
        except Exception as e:
            for finder in self.response:
                if finder in subrespon:
                    self.filewrite("--- TAKEOVER DETECTED !!! : "+subdomain)
                    print self.error+"--- TAKEOVER DETECTED !!! : "+subdomain            
        
    def filewrite(self,veri):
        open("takeover.txt","a+").write(veri+"\n")
                
    def takeover(self,domain,subdomain):
        for firmap in self.firma.keys():
            if firmap in str(domain):
                yollanacak="-- Company: "+firmap+" WebSite :"+self.firma[firmap]
                self.filewrite(subdomain+" --> "+str(domain)+yollanacak+"\n")
                print self.info+yollanacak  
                self.detect(subdomain)  
   
    

if __name__ == '__main__':
    try:           
        colorama.init(autoreset=True) #windows icin        
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
        #              SubDomain TakeOver v1.2                #
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
