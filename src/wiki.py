import wikipedia
import sys, osc


class Wiki:

    def __init__(self, osc_server_port=7077, osc_client_host='127.0.0.1', osc_client_port=7078):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        self.osc_client = osc.Client(osc_client_host, osc_client_port)
        self.osc_server = osc.Server(host='0.0.0.0', port=osc_server_port, callback=self.osc_server_message)
        self.osc_server.run(non_blocking=True)
        
        self.osc_client.send("/wiki/ready")
        
        wikipedia.set_lang("fr")
    
        print("Wiki Ready")
        
    def osc_server_message(self, message):
        print(message)
        if message == '/exit':
            self.osc_server.shutdown()
            sys.exit(0)
        else:
            self.search(message)
            
    def search(self, args):
        #searchStr = ("   " + unicode(str(args)) + "   ").encode('utf-8').strip('<eos>')
        #res = wikipedia.summary(searchStr, sentences=2)
        #resStr = ("   " + unicode(str(res)) + "   ").encode('utf-8').strip('<eos>')
        
        try:
            result = wikipedia.summary(args, sentences=1);
            result = unicode(result).encode('utf-8').strip('<eos>')
            result = result.strip('\"')
            result = result.replace(",", " ")
            result = result.replace("(", " ")
            result = result.replace(")", " ")
            result = result.strip(';')
            self.osc_client.send("/wiki/result "+ result)
        except:
            self.osc_client.send("/wiki/noresult")
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        Wiki();
    elif len(sys.argv) == 4:
        Wiki(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')