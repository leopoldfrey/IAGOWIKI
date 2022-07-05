import wikipedia
import sys
from pyosc import Client, Server

class Wiki:

    def __init__(self, osc_server_port=7077, osc_client_host='127.0.0.1', osc_client_port=7078):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        self.osc_client = Client('127.0.0.1', osc_client_port)
        self.osc_server = Server('127.0.0.1', osc_server_port, self.osc_server_message)
        # self.osc_server.run(non_blocking=True)

        wikipedia.set_lang("fr")

        self.osc_client.send("/ready", 1)

        print("Wiki Ready")

    def osc_server_message(self, address, *args):
        if address == '/exit':
            self.osc_server.shutdown()
            sys.exit(0)
        elif address == '/search':
            self.search(str(args[0]))
        else:
            print(address, args)

    def search(self, args):
        # searchStr = args)) + "   ").encode('utf-8').strip('<eos>')
        #res = wikipedia.summary(searchStr, sentences=2)
        #resStr = ("   " + unicode(str(res)) + "   ").encode('utf-8').strip('<eos>')

        print("[Wiki] Searching for ", args, "...")
        try:
            result = wikipedia.summary(args, sentences=1);
            # result = unicode(result).encode('utf-8').strip('<eos>')
            result = result.strip('\"')
            result = result.replace(",", " ")
            result = result.replace("(", " ")
            result = result.replace(")", " ")
            result = result.strip(';')
            print("[Wiki]", result)
            self.osc_client.send("/result", result)
        except:
            self.osc_client.send("/noresult", 1)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Wiki();
    elif len(sys.argv) == 4:
        Wiki(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')
