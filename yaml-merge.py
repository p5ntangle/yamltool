__author__ = 'shauno'


import yaml
import os
import copy
import argparse

class YamlTools():


    def _load_yaml(self, file):
        return yaml.load(open(file, "r"))

    def _save_yaml(self, data, filename, filepath):
        """
        Move existing file .bck and save new file
        """
        backupfile = filename + ".bck"
        os.rename(filepath+filename, filepath+backupfile)
        with open(filepath+filename, 'w') as outfile:
            outfile.write(yaml.dump(data, default_flow_style=False))

    def _find_yaml(self, yamldir):
        """
        Search in give folder for files ending .yaml
        """
        files = []
        for f in os.listdir(yamldir):
            if f.endswith(".yaml"):
                files.append(f)
        return files

    def load_files(self, sourcedir):
        """
        Load all files in a directory into a dict with base of the filename.
        """
        out = {}
        for f in self._find_yaml(sourcedir):
            lp = f.split('.')[0]
            out[lp] = self._load_yaml(sourcedir+f)
        return out

    def dict_merge(self, a, b):
        """
        Merge to yaml based dicts.
        Checks to see if the entry that is being merged is a dict or list
        to ensure the correct append type is used.
        """
        if not isinstance(b, dict):
            return b
        result = copy.deepcopy(a)
        for k, v in b.iteritems():
            #print "l1 k=%s, v=%s" % (k, v)
            if k in result and isinstance(result[k], dict):
                result[k] = self.dict_merge(result[k], v)
            elif k in result and isinstance(result[k], list):
                for i in v:
                    result[k].append(i)
            else:
                result[k] = copy.deepcopy(v)
        return result

    def merge_all(self, yamldir, inputyaml):
        """
        Does a full merge of the source and dest yaml file, leaving no room for
        special entries for certain files.
        """
        wc = self.load_files(yamldir)
        mc = self._load_yaml(inputyaml)
        result = {}
        for each in wc:
            result[each] = self.dict_merge(wc[each], mc)

        return result

    def merge_selective(self, yamldir, inputyaml):
        """
        Performs a merge based on a input yaml that uses the base entry to determines
        the file that entries will be added to. The All option still needs to be
        implimented.

        Input Yaml Struct

        all:
          variable: change_to

        controller:
          variable: change_to

          network_scheme:
            transformations:
              - action: add-br
                name: br-fl

        """
        wc = self.load_files(yamldir)
        mc = self._load_yaml(inputyaml)
        result = {}
        for each in wc:
            for section in mc:
                if section in each:
                    result[each] = self.dict_merge(wc[each], mc[section])
        return result

    def save_all(self, data, filepath):
        for yfile in data:
            filename = yfile+".yaml"
            self._save_yaml(data[yfile], filename, filepath)
            print "File Saved: %s" % yfile


def help_parser():
    parser = argparse.ArgumentParser(description='Merge yaml files.')
    parser.add_argument('source-dir', metavar='source-dir', type=str, nargs='?',
                        help='directory containing yaml to be modfied')
    parser.add_argument('source-yaml', metavar='source-yaml', type=str, nargs='?',
                        help='input yaml with changes')
    args = parser.parse_args()
    return vars(args)


def main():
    yt = YamlTools()
    conf = help_parser()
    out = yt.merge_selective(conf['source-dir'], conf['source-yaml'])
    yt.save_all(out, conf['source-dir'])

if __name__ == "__main__":
    main()