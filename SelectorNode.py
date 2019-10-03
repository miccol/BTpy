from ControlNode import ControlNode
from NodeStatus import *
import thread
import time
from graphviz import Digraph

class SelectorNode(ControlNode):

    def __init__(self,name = 'SelectorNode'):
        ControlNode.__init__(self,name)
        self.nodeType = 'Selector'


    def Execute(self):
        #print 'Starting Children Threads'
        self.SetStatus(NodeStatus.Idle)

#create threads at start with node idle and then execute them
        # for c in self.Children:
        #     thread.start_new_thread(c.Execute,())

        #check if you have to tick a new child or halt the current
        i = -1
        #try:
        for c in self.Children:
            i = i + 1

            c.Execute()
               # print '???' + str(i)

            child_status = int(c.GetStatus())
            while child_status == NodeStatus.STATENOTDEFINED or child_status == NodeStatus.Idle:
                #print 'Node '+self.name+' waiting for child ' + c.name
                child_status = int(c.GetStatus())
                time.sleep(0.1)

            if child_status == NodeStatus.Running:
                self.SetStatus(NodeStatus.Running)
                self.SetColor(NodeColor.Gray)
              #  print 'Breaking'  + str(i)
                self.HaltChildren(i + 1)
                break
            elif child_status == NodeStatus.Failure:
                c.SetStatus(NodeStatus.Idle)


                if i == len(self.Children):
                    self.SetStatus(NodeStatus.Failure)
                    self.SetColor(NodeColor.Red)
                    # while self.GetStatus() != NodeStatus.Idle:
                    #     time.sleep(0.1)
                    break

            elif child_status == NodeStatus.Success:
                c.SetStatus(NodeStatus.Idle)
                self.HaltChildren(i + 1)
                self.SetStatus(NodeStatus.Success)
                self.SetColor(NodeColor.Green)
                # while self.GetStatus() != NodeStatus.Idle:
                #     time.sleep(0.1)
                break


            # elif child_status == NodeStatus.Idle:
            #     self.SetStatus(NodeStatus.Idle)
            #     break


            else:
                raise Exception('Node ' +self.name + ' does not recognize the status of child ' + str(i) +'. (1 is the first). Child name: '+c.name+ 'Status:' + str(child_status) +'RUNNING IS '+ str(NodeStatus.Running))



           # except:
             #   print 'Error'


    def GDraw(self):
        dot = Digraph()
        dot.node(self.id.__str__(),'?', shape='square',color='gray')


        for child in self.Children:
            dot.subgraph(child.GDraw())
            dot.edge(self.id.__str__(),child.id.__str__(),color='black',penwidth='0.8',headwidth='0.8')

    #dot.render('hello')
        return dot

    def ActionsExecuted(self):
        actions = 0
        for c in self.Children:
            actions += c.ActionsExecuted()
            if actions > 0:
                break
        return actions