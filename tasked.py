#/usr/bin/python3

import sys
from os import system, name
import json
import datetime as DT


class Item:

    def __init__(self,  title="",
                        itemtype="item",
                        tags=[], 
                        notes="", 
                        deadline=DT.datetime, 
                        done=False, 
                        children=[]):
        self.title      = title
        self.itemtype   = itemtype
        self.tags       = tags
        self.notes      = notes
        self.deadline   = deadline
        self.done       = done
        self.children   = children

    def __init__(self, json_obj):
        self.title      = json_obj['title']
        self.itemtype   = json_obj['itemtype']
        self.tags       = json_obj['tags']
        self.notes      = json_obj['notes']
        self.deadline   = json_obj['deadline']
        self.done       = json_obj['done']
        self.children   = [Item(child) for child in json_obj['children']]


    def show(self, depth=0):

        shown = ("[{done}] {title}\n".format(   done=("X" if self.done else " "),
                                                deadline=self.deadline,
                                                title=self.title ))
        for child in self.children:
            shown += "{indent}{child}".format(indent=("   "*depth), child = child.show(depth+1))

        return shown


    def dict(self):
        mapping = {}
        mapping["title"] = self.title
        mapping["itemtype"] = self.itemtype
        mapping["tags"] = self.tags
        mapping["notes"] = self.notes
        mapping["deadline"] = self.deadline
        mapping["done"] = self.done
        mapping["children"] = [ child.dict() for child in self.children ]
        return mapping

    def __str__(self):
        return json.dumps(self.dict(), indent=4)


def loadjson(filename):
    
    obj = json.loads( open(filename, "r").read() )

    return Item(obj)


def save( root, filename="save.json" ):
    with open(filename,'w') as outfile:
        outfile.write(str(root))



def main():

    prompt = ">"

    debug = False
    selected = None
    root = None
    results = []


    if "-d" in sys.argv:
        debug = True

    for arg in sys.argv:
        if arg.endswith(".json"):
            root = loadjson(arg)
        
    if root:
        selected = root

    while True:
        
        
        line = input(selected.title+" > ")

        ''' COMMANDS:
                exit
                clear   
                ls      <Item>
                cl      <Item>
                save    
                load    <filepath>
                select  <Item>
                new     <Item>
                edit    <Item>
                delete  <Item>
        '''

        commands = line.split("&")

        for cmd in commands:
            tokens = [ x.strip() for x in cmd.strip().split(" ") if x ]

            if debug:
                print(tokens)

            if not tokens:
                continue


            if tokens[0] == "exit":
                sys.exit()

            elif tokens[0] == "list":

                for child in selected.children:
                    print(child.title)

            elif tokens[0] == "save":

                save(root)

            elif tokens[0] == "show":

                if tokens[1] == 'all':
                    print(root.show())

            elif tokens[0] == 'select':

               pass

            elif tokens[0] == "find":

                pass
                    

            else:
                print("err: invalid command")




if __name__ == '__main__':
    main()





