import os
import re


linebreakers = ["Issue/Error", "Cause", "Resolution/Workaround", ""]


def extract_content(path):
    kbase = []
    filecontent = []
    for file in os.listdir(path):
        content = dict()
        filename = os.path.join(path, file)
        with open(filename, 'r') as f:
            filecontent = f.readlines()

        content['issue'] = extract_lines(filecontent, linebreakers, 0)
        for idx, line in enumerate(content['issue']):
            content['issue'][idx] = line.replace('- ', '')
        content['cause'] =  extract_lines(filecontent, linebreakers, 1)
        for idx, line in enumerate(content['cause']):
            content['cause'][idx] = line.replace('- ', '')

        rm_idx = []
        content['resolution'] = extract_lines(filecontent, linebreakers, 2)
        for idx, line in enumerate(content['resolution']):
            if re.search('^\s*[a-z]\.', line):
                rm_idx.append(idx)
                continue
            content['resolution'][idx] = re.sub('^\d\.\s*', '', line)
            if content['resolution'][idx].startswith('If the'):
                rm_idx.append(idx)

        for val in reversed(rm_idx):
            content['resolution'].pop(val)

        kbase.append(content)
    return kbase


def extract_lines(f, linebreakers, index):
    arry = []
    test = True
    indx = 0
    while test:
        for idx, line in enumerate(f):
            if line.strip() == linebreakers[index]:
                test = False
                indx = idx
                break

    for xline in f[indx+1:]:
        if xline.strip() == linebreakers[index + 1]:
            break
        if xline.strip() == '':
            continue
        arry.append(xline.strip())
    return arry


# print extract_content("knowledge")

