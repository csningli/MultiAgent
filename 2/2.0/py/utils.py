
# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import time, datetime
from numpy import array, dot
from numpy.linalg import norm

def append_to_sys_path(path = None) :
    if path is None :
        unit_tests_path = os.path.dirname(os.path.abspath(__file__))
        path = '/'.join(unit_tests_path.split('/')[:-1]) + '/py'
    sys.path.append(path)


def test_func(data = None, show = []) :
    def real_test_func(func) : 
        def func_wrapper(*args, **kwargs) :
            print('| Run test: %s' % func.__name__)
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            for label in show :
                if label in ['INFO', 'ERROR'] :
                    print("Wait seconds for preparing the '%s' logs." % label)
                    Logger().print_logs(label = label)
            if data is not None : 
                print("Wait seconds for storing the data into files.")
                data.to_file()
            print('| Done. Time cost: %s (s)' % (end - start))
            print('-' * 60)
        return func_wrapper
    return real_test_func

def check_attrs(obj, attrs) :
    '''
    Example of 'attrs': 
    attrs = {
        'a' : None,
        'b' : {
            b1 : None, 
            b2 : None,
        }
    }
    '''
    is_valid = True
    if attrs is not None and hasattr(attrs, '__iter__') and hasattr(attrs, '__getitem__'):
        for attr in attrs :
            if not hasattr(obj, attr) :
                is_valid = False
                break
            elif attrs[attr] is not None and type(getattr(obj, attr)).__name__ not in ['method', 'builtin_function_or_method'] :
                is_valid = check_attrs(getattr(obj, attr), attrs[attr])
                if is_valid == False :
                    break
    else :
        is_valid = False
    return is_valid                   


def check_length_equals_two(obj) :
    return check_attrs(obj, {"__getitem__" : None, "__len__" : None}) and len(obj) == 2 
    
    
def timelabel() :
    return datetime.datetime.now().strftime('%y%m%d.%H%M%S.%f')


def dict2str(d) :
    result = ""
    if (hasattr(d, "items")) :
        for key, value in d.items() :
            if result != "" :
                result += ";"
            result += "%s:%s" % (key, value)
    return result

def str2dict(s) :
    result = {}
    for item in result.strip().split(';') :
        if len(item.strip().split(':')) > 1 :
            result[item.strip().split(':')[0]] = item.strip().split(':')[0]
    return result
        

def rfix_str_len(s, l, ignore = '') :
    fs = ""
    if len(s) <= l :
        fs = s + " " * (l - len(s))
    else : 
        if s[-1] == ignore and len(ignore) == 1 : 
            fl = min(3, l - 1)
            fs = s[:(l - fl)] + "." * fl + ignore
        else :
            fl = min(3, l)
            fs = s[:(l -fl)] + "." * fl
    return "{:<}".format(fs)
    
def lfix_str_len(s, l, ignore = "") :
    fs = ""
    if len(s) <= l :
        fs = " " * (l - len(s)) + s
    else : 
        if s[-1] == ignore and len(ignore) == 1 : 
            fl = min(3, l - 1)
            fs = s[:(l - fl)] + "." * fl + ignore
        else :
            fl = min(3, l)
            fs = s[:(l - fl)] + "." * fl
    return "{:>}".format(fs)
 
