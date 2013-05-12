#! /usr/bin/python

import urllib
import urllib2
import json
import sys
import os

def generate_test_code(class_name, input_types, return_type, topcoder_url):
    topcoder_url = urllib.quote(topcoder_url)
    url = "http://open.dapper.net/transform.php?dappName=topcoder_test_cases&transformer=JSON&v_url=%(topcoder_url)s" % locals()

    data = json.load(urllib2.urlopen(url))
    test_code = []

    # generate inputs and expected outputs
    inputs = []
    outputs = []
    for value in data['groups']['expected_result']:
        inputs.append(value['input'][0]['value'])
        outputs.append(value['output'][0]['value'])

    for i, ip in enumerate(inputs):
        input_parts = ip.split(",")
        for j, input_type in enumerate(input_types):
            test_code.append("%s input_%d_%d = %s;" % (input_type, j, i, input_parts[j]))
    test_code.append("\n")

    for i, op in enumerate(outputs):
        test_code.append("%s output_%d = %s;" % (return_type, i, op))
    test_code.append("\n")

    # generate function calls
    method_name = data['fields']['method'][0]['value']
    for i in range(len(inputs)):
        input_args = ','.join(["input_%d_%d" % (j, i) for j in range(len(input_types))])
        input_log = " + ".join(["input_%d_%d.toString()" % (j, i) for j in range(len(input_types))])
        test_code.append("System.out.println(\"Running input \" + %(input_log)s);" % locals())
        test_code.append("%(return_type)s a_output_%(i)d = (new %(class_name)s()).%(method_name)s(%(input_args)s);" % locals())
        test_code.append("System.out.println(\"Expected Output: \" + output_%(i)d);" % locals())
        test_code.append("System.out.println(\"Actual Output: \" + a_output_%(i)d);" % locals())
        if '[]' in return_type:
            test_code.append("assert Arrays.equals(a_output_%(i)d, output_%(i)d);" % locals())
        elif return_type[0].isupper():
            test_code.append("assert a_output_%(i)d.equals(output_%(i)d);" % locals())
        else:
            test_code.append("assert a_output_%(i)d == output_%(i)d;" % locals())
        test_code.append("System.out.println(\"Success!\");")
        test_code.append("\n")
    return "\n".join(test_code)

def search_topcoder(class_name):
    url = "http://open.dapper.net/transform.php?dappName=topcoder_search&transformer=JSON&v_class=%(class_name)s" % locals()
    data = json.load(urllib2.urlopen(url))
    return data['fields']['problem_link'][0]['href']

def parse_problem_page(problem_link):
    url = "http://open.dapper.net/transform.php?dappName=topcoder_parse_problem_page&transformer=JSON&applyToUrl=%s" % urllib.quote(problem_link)
    data = json.load(urllib2.urlopen(url))['fields']
    url2 = "http://open.dapper.net/transform.php?dappName=topcoder_test_cases_link&transformer=JSON&applyToUrl=%s" % urllib.quote(data['test_cases_link'][0]['href'])
    data2 = json.load(urllib2.urlopen(url2))['fields']
    return (data['input_types'][0]['value'].split(","),
            data['return_type'][0]['value'],
            data2['test_cases_link'][0]['href'])

def create_test_program(test_code):
    test_code_template = """
    import java.util.Arrays;
    public class test {
            public static void main(String[] args) {
                        %(test_code)s
                            }
    }
    """
    f = open("test.java", "w")
    f.write(test_code_template % locals())
    f.close()

def run_test_program():
    os.system("javac test.java")
    os.system("java test")
    #os.system("rm test.java")

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s <java_file>' % sys.argv[0]
        sys.exit(1)
    class_name = sys.argv[1].split(".")[0]
    problem_link = search_topcoder(class_name)
    input_types, return_type, test_cases_url = parse_problem_page(problem_link)
    test_code = generate_test_code(class_name, input_types, return_type, test_cases_url)
    create_test_program(test_code)
    run_test_program()

if __name__ == '__main__':
    main()
