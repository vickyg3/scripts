#! /usr/bin/python

from bs4 import BeautifulSoup

import requests
import sys

def exit(err):
    print err
    sys.exit(0)

def get_text(node, lower = True):
    if lower:
        return (''.join(node.findAll(text = True))).strip().lower()
    return (''.join(node.findAll(text = True))).strip()

def get_method_signature(tag):
    gold = 'Method signature:'.lower()
    return tag.name == "td" and get_text(tag) == gold

def get_returns(tag):
    gold = 'Returns:'.lower()
    return tag.name == "pre" and gold in get_text(tag)

def main():

    if len(sys.argv) != 3:
        exit("Usage: %s <srm_number> <class_name>" % sys.argv[0])

    srm = sys.argv[1].strip().lower()
    class_name = sys.argv[2].strip().lower()

    domain = "http://community.topcoder.com"
    search_url = "%(domain)s/tc?module=ProblemArchive&class=%(class_name)s"

    data = requests.get(search_url % locals()).text
    # f = open('/tmp/data.html', 'w')
    # f.write(data)
    # f.close()
    # data = open('/tmp/data.html', 'r')

    soup = BeautifulSoup(data)
    result_table = None
    result_table_string = 'Challenge'
    tables = soup.findAll('table')
    tables.reverse()
    for table in tables:
        if result_table_string.lower() in get_text(table):
            result_table = table
            break
    else:
        exit("no problem found, please check class name")

    result_row = None
    actual_class_name = None
    for row in result_table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) < 3:
            continue
        if get_text(cells[1]) == class_name and srm in get_text(cells[2]):
            actual_class_name = get_text(cells[1], lower = False)
            result_row = row
            break
    else:
        exit("no problem found, please check class name and SRM number")

    problem_url = "%s%s" % (domain, cells[1].find('a').get('href'))

    data = requests.get(problem_url).text
    # f = open('/tmp/problem.html', 'w')
    # f.write(data)
    # f.close()
    #data = open('/tmp/problem.html', 'r')

    soup = BeautifulSoup(data)
    try:
        method_signature_text = soup.findAll(get_method_signature)[-1]
        method_signature = method_signature_text.nextSibling.string
        returns_tr = method_signature_text.parent.previousSibling
        return_type = returns_tr.findAll('td')[1].string.strip()
        parameters_tr  = returns_tr.previousSibling
        parameters = parameters_tr.findAll('td')[1].string.split(",")
        method_tr = parameters_tr.previousSibling
        method_name = method_tr.findAll('td')[1].string.strip()
        test_cases = soup.findAll(get_returns)
        expected_return_values = []
        inputs = []
        for i in range(len(test_cases)):
            inputs.append([])
        for i, test_case in enumerate(test_cases):
            expected_return_values.append(test_case.string.strip().split(": ")[1])
            input_values = test_case.parent.parent.previousSibling.findAll('pre')
            for input_value in input_values:
                inputs[i].append(input_value.string.strip())
    except:
        raise
        exit("error getting method signature, no luck")

    # inject test cases into template
    spaces = "        "
    input_test_case = "%(parameter)s var_%(index_1)d_%(index_2)d = %(value)s;\n"
    invoke_method = "%(return_type)s expected_%(index_1)d = %(lower_actual_class_name)s.%(method_name)s(%(method_params)s);\n"
    if return_type == "String":
        compare_outputs = "System.out.println((expected_%(index_1)d.equals(%(expected_value)s) ? \"Passed\" : \"Failed\") + \" for case %(index_1)d\");"
    else:
        compare_outputs = "System.out.println(((expected_%(index_1)d == %(expected_value)s) ? \"Passed\" : \"Failed\") + \" for case %(index_1)d\");"
    compare_outputs += "\n"
    lower_actual_class_name = actual_class_name.lower()
    test_case_str = ""
    for index_1, input_case in enumerate(inputs):
        # declare the inputs
        method_params_list = []
        for index_2, parameter in enumerate(parameters):
            value = input_case[index_2]
            test_case_str += spaces
            test_case_str += input_test_case % locals()
            method_params_list.append("var_%(index_1)d_%(index_2)d" % locals())
        # invoke the function
        method_params = ','.join(method_params_list)
        test_case_str += spaces
        test_case_str += invoke_method % locals()
        # compare the output
        expected_value = expected_return_values[index_1]
        test_case_str += spaces
        test_case_str += compare_outputs % locals()

    # inject everything else into final template
    template = open('template.java', 'r').read()
    fp = open('%(actual_class_name)s.java' % locals(), 'w')
    fp.write(template % locals())
    fp.close()
    print "done :) generated %(actual_class_name)s.java" % locals()

if __name__ == "__main__":
    main()