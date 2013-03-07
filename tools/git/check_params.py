import yaml
import itertools

BASE_DIR = "app/config"
ERROR_MESSAGE = "file: %s/%s has keys %s which are not present in file: %s/%s"

def dict_diff(first, second, diff):
    for key in first.keys():
        if not second.has_key(key):
            diff[key] = first[key]
            continue
        if type(first[key]) is dict:
            return dict_diff(first[key], second[key], diff)

    return diff

parameters_files = ('parameters_dev.yml', 'parameters_prod.yml', 'parameters.yml')
parameters_files_combinations = itertools.combinations(parameters_files, 2)

try:
    errors = []
    for file1, file2 in parameters_files_combinations:
        stream1 = open("%s/%s" % (BASE_DIR, file1))
        dict1   = yaml.load(stream1)

        stream2 = open("%s/%s" % (BASE_DIR, file2))
        dict2   = yaml.load(stream2)

        diff1 = dict_diff(dict1, dict2, {})

        if diff1:
            errors.append(ERROR_MESSAGE % (BASE_DIR, file1, str(diff1), BASE_DIR, file2))

        diff2 = dict_diff(dict2, dict1, {})
        if diff2:
            errors.append(ERROR_MESSAGE % (BASE_DIR, file2, str(diff2), BASE_DIR, file1))
except Exception as e:
    errors.append(str(e))

if errors:
    print "\n".join(errors)
