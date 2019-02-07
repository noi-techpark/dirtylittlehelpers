import json
import difflib
import re
import math

class JsonDiff:
    
    def __init__(self, json1, json2):
        if json1:
            self.json1 = JsonDiff.sort_json(json.loads(json1))
        else:
            self.json1 = ""
        if json2:
            self.json2 = JsonDiff.sort_json(json.loads(json2))
        else:
            self.json2 = ""
        self.json1 = JsonDiff.__clean_dump(self.json1)
        self.json2 = JsonDiff.__clean_dump(self.json2)
        self.difftxt = None
        self.equal = None
        self.ignore_list = []
        self.ignore_list_activate = True
        
        # Maximum relative difference while comparing numbers (used for math.isclose) 
        self.max_relative_diff = 1e-12
        
    def set_max_relative_diff(self, n):
        self.max_relative_diff = n
        
    def ignore_rules_set(self, regxp_list):
        self.ignore_list = regxp_list
        
    def ignore_rules_add(self, regxp):
        self.ignore_list.append(regxp)
        
    def ignore_rules_active(self, flag):
        self.ignore_list_activate = flag
        
    def get_json1(self):
        return "\n".join(self.json1)
    
    def get_json2(self):
        return "\n".join(self.json2)
    
    def get_equality(self):
        return self.equal
    
    def diff(self):
        if self.difftxt == None:
            self.difftxt = "".join(JsonDiff.__diff(self))
        return self.difftxt
        
    def __diff(self):
        self.diff = difflib.Differ().compare(self.json1, self.json2)
        lines = list(self.diff)
        
        skip = 0
        self.equal = True
        for i, line in enumerate(lines):
            if skip > 0:
                skip -= 1
                continue
    
            if self.ignore_list_activate:
                matched = False
                for pattern in self.ignore_list:
                    match = re.match(".*" + pattern + ".*", line)
                    if match:
                        matched = True
                        break
                if matched:
                    yield('i ' + line[2:] + "\n")
                    continue
    
            if line[0] == '-':
                """ Ignore floating point representations, if values are equal
                """
                if (len(lines) > i+2 and ((lines[i+1][0] == '?' and lines[i+2][0] == '+')
                        or (lines[i+1][0] == '+' and lines[i+2][0] == '?'))):
                    try:
                        n1 = float(JsonDiff.__extract_json_number(lines[i][1:]))
                        if lines[i+2][0] == '+':
                            n2 = float(JsonDiff.__extract_json_number(lines[i+2][1:]))
                        else:
                            n2 = float(JsonDiff.__extract_json_number(lines[i+1][1:]))
                        if not math.isclose(n1, n2, rel_tol=self.max_relative_diff):
                            yield(line)
                            self.equal = False
                        else:
                            yield (" " + line[1:])
                            if i+3 <= len(lines) and lines[i+3][0] == '?':
                                skip = 3
                            else:
                                skip = 2
                    except Exception:
                        yield(line)
                else:
                    yield(line)
                    self.equal = False
            elif line[0] == '+':
                yield(line)
                self.equal = False
            else:
                yield(line)
            if not line.endswith('\n'):
                yield("\n")
        
    def __clean_dump(jsontxt):
        json_clean = []
        for line in json.dumps(jsontxt, indent=4, sort_keys=True).splitlines():
            json_clean.append(line.rstrip(' ,'))
        return json_clean
    
    
    def __extract_json_number(l):
        groups = l.split(':')
        if len(groups) == 2:
            n = groups[1]
        else:
            n = groups[0]
        return n.strip('\n, ')
        
    def __sort_json_key_func(item):
        """ helper function used to sort nested types
    
        :param item: any type
        :return: sorted list of tuples (k, v), where v can also be a list of tuples
        """
        pairs = []
        if isinstance(item, dict):
            if not item:
                pairs.append(('$__dict_empty', {}))
            for k, v in item.items():
                if isinstance (v, (dict, list)):
                    pairs.append((k, JsonDiff.__sort_json_key_func(v)))
                else:
                    pairs.append((k, v))
        if isinstance(item, list):
            for k, v in enumerate(item):
                if isinstance (v, (dict, list)):
                    v_sorted = JsonDiff.__sort_json_key_func(v)
                    keys = ''
                    for key in v_sorted:
                        keys += key[0]
                        if key[0] == 'id' and isinstance(key[1], (str, int)):
                            keys = str(key[1]) + '_' + keys
                    pairs.append(('$__list_' + str(type(key[0]).__name__) + '_' + keys, v_sorted))
                else:
                    pairs.append(('$__list_' +  str(type(v).__name__) + '_' + str(v), v))
            
        return sorted(pairs, key=lambda x: x[0])

    
    def sort_json(j):
        sorted_pairs = JsonDiff.__sort_json_key_func(j)
        return JsonDiff.__sort_json_by_key_func(sorted_pairs)
    
    def __sort_json_by_key_func(y):
        res = None
        if isinstance(y, list):
            for i, x in enumerate(y):
                if x[0].startswith('$__dict_empty'):
                    res = {}
                elif x[0].startswith('$__list_'):
                    if not isinstance(res, list):
                        res = []
                    res.append(JsonDiff.__sort_json_by_key_func(x[1]))
                else:
                    if not isinstance(res, dict):
                        res = {}
                    res[x[0]] = JsonDiff.__sort_json_by_key_func(x[1])
            
        if res == None:
            res = y
    
        return res
