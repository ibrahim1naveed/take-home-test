import json
import urllib.request
import argparse

# rearranges the data by looking at what user wants in types of class name, type and repo 
def rearrange_data(data,className, typeName, repoName):
    list_of_output = []
    # loop through the various classes in our data
    for current_class in data:
        current_class_info = data[current_class]
        # if the user has specified that they want a specfic class, ignore all the rest
        if (className is not None and current_class.lower() != className.lower()):
            continue
        # loop thrugh all findings in our current class information
        for findings in current_class_info:
            list_of_findings = current_class_info[findings]
            # loop through each finding 
            for finding in list_of_findings:
                # split url using by calling split_url method
                list_url = split_url(finding['location'])
                current_start = finding['startLineNumber']
                current_end = finding['endLineNumber']
                current_type = finding['type']
                # check if repo was specified by user, if so add only the one specified
                if (repoName is not None and list_url[0].lower() != repoName.lower()):
                    continue
                # check if type was specified by user, if so add only the one specified
                if (typeName is not None and current_type.lower() != typeName.lower()):
                    continue
                temp_dic = create_dic(list_url[0], list_url[1],current_start, current_end, current_class,current_type)
                list_of_output.append(temp_dic)
    return list_of_output

# gets json data from url and returns it in the form of a dictionary
def get_json_data(url):
    with urllib.request.urlopen(url) as u:
        data = json.loads(u.read().decode())
        data = (data['data'][0])
        return data

# create a dictionary from inputs and return this dictionary
def create_dic(repo, file, startLineNumber, end, className, type):
    temp_dic = {
        "repository": repo,
        "file": file,
        "startLineNumber": startLineNumber,
        "endLineNumber": end,
        "class": className,
        "type": type
    }
    return temp_dic

# splits url into two strings, one which indicates repo name and one which indicates file name
def split_url(url):
    split = url.rsplit('/', 1)
    return [split[0],split[1]]

def main():
    # set up 4 arguments using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourceUrl", help="source URL to get JSON file from")
    parser.add_argument("--className", help="name of class you want to map to")
    parser.add_argument("--type", help="name of type you want to map to")
    parser.add_argument("--repo", help="name of repo you want to map to")
    args = parser.parse_args()
    url = args.sourceUrl
    className = args.className
    typeName = args.type
    repoName = args.repo
    # get json data by making a request
    data = get_json_data(url)
    # rearrange data and print
    print(rearrange_data(data, className, typeName, repoName))
    

if __name__ == '__main__':
    main()