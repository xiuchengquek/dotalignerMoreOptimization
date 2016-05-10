import zmq
import sys
import os

def main(reciever_ip, sink_ip, bash_script):
    context = zmq.Context()

    # Get reciever
    sender = context.socket(zmq.PUSH)
    sender.bind(reciever_ip)

    sinker = context.socket(zmq.PUSH)
    sinker.connect(sink_ip)

    command_files = os.listdir('./dotaligner_command')
    command_files = [os.path.join(x) for x in command_files]

    sender.send_unicode(u'%s' % bash_script)



if __name__ == '__main__' :
    reciever_id = sys.argv[1]
    sink_ip = sys.argv[2]
    bash_script = sys.argv[3]
    main(reciever_ip=reciever_id,sink_ip= sink_ip ,bash_script= bash_script)





