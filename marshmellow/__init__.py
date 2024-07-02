import os 
import sys 
import json
import collections
import argparse

def load(fp): 
    try: 
        with open(fp) as f: 
            return json.loads(f.read());
    except: 
        return False

def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def merge(values):
    ret = {}
    if len(values) > 0: 
        if isinstance(values[0],dict): 
            for d in values:     
                dict_merge(ret,d)
            return ret    
        else: 
            return values[0]
    return "EmptyArray"

def cap(v): 
    return v[0].upper() + v[1:]


#returns new key and new Type name

def json_preview(v): 
    print("{")
    for k,v in v.items(): 
        x = "..."
        if isinstance(v,(str,bool,int)): 
            x = "{0}{1}".format(str(v)[0:10],"..." if len(str(v)) > 10 else "")
        else: 
            if isinstance(v,list): 
                x = "[]"
            if isinstance(v,dict):
                x = "{}" 
        print("    {0}: {1}".format(k,x))
    print("}")

def type_name(mapped,outer,inner,v):
    print("Creating new Struct for:")
    print("-" * 80)
    json_preview(v)
    print("-" * 80)
    while True:
        p = outer + cap(inner)
        print("Outer type is: {0} purposed inner type is: {1}".format(outer,p))
        x = input("Enter new type name (leave blank for purposed): ")
        if len(x) == 0:
            return p
        else: 
            if x in mapped.keys():
                print("Error: {0} is already used...\n")
            else: 
                return x



def go_type(v,is_array,static):
    if not static: 
        v = type(v).__name__
        if v == "str":
            v = "string"
    if is_array: 
        v = "[]" + v
    return v

def go_struct_mapper(key,o):
    ret = {key:{}}
    for k,v in o.items(): 
        a = False
        x = v 
        if isinstance(x,list):
            x = merge(v)
            a = True
        if isinstance(x,dict):
            tn = type_name(ret,key,k,x)
            ret[key][k] = go_type(tn,a,True)
            ret.update(go_struct_mapper(tn,x))
        else: 
            ret[key][k] = go_type(x,a,False)
    return ret
                

def go_struct_printer(mapped):
    for s,o in mapped.items(): 
        print("type {0} struct ".format(s) + "{")
        for k,v in o.items(): 
            print("    {0} {1} `json:\"{2}\"`".format(cap(k),v,k))
        print("}\n")

def main():
    parser = argparse.ArgumentParser(
        prog='marshmellow',
        description='Takes a json file and outputs golang structs for json Marshalling and Unmarshalling.',
        epilog='Example: marshmellow ./results.json -n Results'
    )

    parser.add_argument('filename', type=str,help='json input file')
    parser.add_argument('-n', dest="name", default="Root",type=str,help='Name of the outer most go struct')
    args = parser.parse_args()

    data = load(args.filename)
    if data: 
        try: 
            mapped = go_struct_mapper(args.name,data)
            print("\n Go Struct Output...")
            print("-" * 80)
            go_struct_printer(mapped)
        except: 
            print("[-] Error mapping json...")
    else: 
        print("[-] Error reading json file...")

if __name__ == "__main__":
    main()

