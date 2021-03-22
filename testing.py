import unittest
import json
from manipulate_json import split_url, create_dic, get_json_data, rearrange_data

class TestJsonMethods(unittest.TestCase):

    def test_get_json_data(self):
        dummy_data = {'injection': {'findings': [{'location': 'github.com/myorg/a/file.py', 'startLineNumber': '1', 'endLineNumber': '2', 'type': 'sql-injection'}, {'location': 'githu.com/myorg/a/file.py', 'startLineNumber': '5', 'endLineNumber': '10', 'type': 'command-injection'}]}, 'bad-crypto': {'findings': [{'location': 'github.com/myorg/a/file.py', 'startLineNumber': '1', 'endLineNumber': '2', 'type': 'weak-crypto'}, {'location': 'github.com/myorg/c/file.py', 'startLineNumber': '1', 'endLineNumber': '5', 'type': 'weak-crypto-2'}]}}
        valid_url ="https://raw.githubusercontent.com/peaudecastor/data-converter-take-home-test/main/sample.json"
        data1 = get_json_data(valid_url)
        self.assertEqual(dummy_data, data1)

        # can not decode json if we try to access a random url with no json, should raise decode error
        invalid_url = "https://randomURL.com"
        with self.assertRaises(json.JSONDecodeError):
            get_json_data(invalid_url)

    def test_split_url(self):

        s1 = "github.com/frontend/x.txt"
        list_url = split_url(s1)
        self.assertEqual('github.com/frontend', list_url[0])
        self.assertEqual('x.txt', list_url[1])

        s2 = "github.com/backend/homepage/routes.py"
        list_url = split_url(s2)
        self.assertEqual('github.com/backend/homepage', list_url[0])
        self.assertEqual('routes.py', list_url[1])

        # since there is not '/' present this should raise an index out of bound error when trying to create list
        s3 = "github"
        with self.assertRaises(IndexError):
            list_url = split_url(s3)

    def test_create_dic(self):
        
        dummy_dic = {
            'repository': 'github.com/myorg/a', 
            'file': 'file.py', 
            'startLineNumber': 1, 
            'endLineNumber': 2, 
            'class': 'injection', 
            'type': 'sql-injection'
        }
        dic1 = create_dic("github.com/myorg/a", "file.py", 1, 2, "injection", "sql-injection")
        self.assertEqual(type(dic1),type(dummy_dic))
        self.assertEqual(dummy_dic, dic1)

        dic2 = create_dic("github.com/myorg/b", "file2.py", 1, 2, "injection", "sql-injection")
        self.assertNotEqual(dic2,dummy_dic)
        
    def test_rearrange_data(self):

        json_dummy_data = {'injection': {'findings': [{'location': 'github.com/myorg/a/file.py', 'startLineNumber': '1', 'endLineNumber': '2', 'type': 'sql-injection'}, {'location': 'githu.com/myorg/a/file.py', 'startLineNumber': '5', 'endLineNumber': '10', 'type': 'command-injection'}]}, 'bad-crypto': {'findings': [{'location': 'github.com/myorg/a/file.py', 'startLineNumber': '1', 'endLineNumber': '2', 'type': 'weak-crypto'}, {'location': 'github.com/myorg/c/file.py', 'startLineNumber': '1', 'endLineNumber': '5', 'type': 'weak-crypto-2'}]}}
        complete_list = [
            {'repository': 'github.com/myorg/a', 'file': 'file.py', 'startLineNumber': '1', 'endLineNumber': '2', 'class': 'injection', 'type': 'sql-injection'}, 
            {'repository': 'githu.com/myorg/a', 'file': 'file.py', 'startLineNumber': '5', 'endLineNumber': '10', 'class': 'injection', 'type': 'command-injection'}, 
            {'repository': 'github.com/myorg/a', 'file': 'file.py', 'startLineNumber': '1', 'endLineNumber': '2', 'class': 'bad-crypto', 'type': 'weak-crypto'}, 
            {'repository': 'github.com/myorg/c', 'file': 'file.py', 'startLineNumber': '1', 'endLineNumber': '5', 'class': 'bad-crypto', 'type': 'weak-crypto-2'}
        ]

        all_findings = rearrange_data(json_dummy_data,None, None, None)
        self.assertEqual(all_findings, complete_list)

        # test output if we specific class name
        list_class_injection = rearrange_data(json_dummy_data, 'injection', None,None)
        self.assertEqual(list_class_injection, complete_list[0:2])
        list_class_badcrypto = rearrange_data(json_dummy_data, 'bad-crypto', None,None)
        self.assertEqual(list_class_badcrypto, complete_list[2:4])

        # test output if we specific type
        list_type_sqlinjection = rearrange_data(json_dummy_data, None,"sql-injection", None)
        self.assertEqual(list_type_sqlinjection[0], complete_list[0])

        # test output if we specify a repo
        list_repo_c = rearrange_data(json_dummy_data, None,None, "github.com/myorg/c")
        self.assertEqual(list_repo_c[0], complete_list[3])

        # test output if we test multiple elements such as repo and class
        list_repo_c_and_class_badcrypto = rearrange_data(json_dummy_data,'bad-crypto',None,'github.com/myorg/c')
        self.assertEqual(list_repo_c_and_class_badcrypto[0], complete_list[3])

if __name__ == '__main__':
    unittest.main()