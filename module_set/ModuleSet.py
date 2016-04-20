from __future__ import print_function

class ModuleSet(object):

    def __init__(self, yaml_fpath):
        from os import path
        import yaml

        from gronexctl.validation import check_true

        check_true(
            yaml_fpath.endswith('.yml'),
            'file does not have an extension of ".yml"',
        )

        self.yaml_fpath = yaml_fpath
        self.yaml_fname = path.split(self.yaml_fpath)[-1]
        self.yaml_dpath = path.dirname(self.yaml_fpath)
        self.yaml = None
        self.id = None
        self.name = None
        self.description = None
        self.dependencies = None
        self.addon_dependencies = None
        self.absolute_dependencies = None
        self.absolute_addon_dependencies = None


    def resolve(self):
        self.__read()
        self.__aggregate()


    def __aggregate(self, __deps=[], __adeps=[], __depth=0):
        from copy import deepcopy

        __depth += 1
        if self.dependencies is not None:
            for v in self.dependencies:
                v.__aggregate(__deps, __adeps, __depth)

        if self.id not in __deps:
            __deps.append(self.id)

        if self.addon_dependencies is not None:
            for v in self.addon_dependencies:
                __adeps.append(v)

        __depth -= 1

        for i in xrange(0, len(__adeps) - 1):
            for ii in xrange(i+1, len(__adeps)):
                __adeps[ii] = list(set(__adeps[ii]) - set(__adeps[i]))

        __adeps = [l for l in __adeps if l != []]

        self.absolute_dependencies = deepcopy(__deps)
        self.absolute_addon_dependencies = deepcopy(__adeps)


    def __read(self, __depth=[]):
        from os import path
        from sys import stderr
        import yaml

        from gronexctl.validation import check_true
        from gronexctl.validation.regex import (
            addon_name,
            module_set_id,
            module_set_name,
            module_set_description,
        )

        with open(self.yaml_fpath, 'r') as yaml_f:
            self.yaml = yaml.load(yaml_f)

        self.id = self.yaml['id']
        self.name = self.yaml['name']
        self.description = self.yaml['description']

        module_set_id.check(self.id)
        module_set_name.check(self.name)
        if self.description is not None:
            module_set_description.check(self.description)

        deps = self.yaml['dependencies']
        addon_deps = self.yaml['addon_dependencies']
        deps_is_list = type(deps) is list
        addon_deps_is_list = type(addon_deps) is list

        check_true(
            deps is None or deps_is_list,
            'in module set "{0}": "dependencies" is not None or a list.'
                .format(self.id)
        )
        check_true(
            addon_deps is None or addon_deps_is_list,
            '"in module set "{0}": addon_dependencies" is not None or a list.'
                .format(self.id)
        )
        check_true(
            deps_is_list or addon_deps_is_list,
            'in module set "{0}": either "dependencies" or "addon_dependencies" must be a list.'
        )

        __depth.append(self.id)
        if deps_is_list:
            self.dependencies = []
            for v in deps:
                module_set_id.check(v)
                if v in __depth:
                    print(
                        'Circular dependency for set "{0}" in {1}, ignoring...'
                        .format(v, __depth),
                        file=stderr,
                    )
                    continue

                child_ms = ModuleSet(
                    path.join(
                        self.yaml_dpath,
                        '{0}.yml'.format(v)
                    )
                )
                child_ms.__read(__depth)
                self.dependencies.append(child_ms)

        if addon_deps_is_list:
            self.addon_dependencies = []
            for v in addon_deps:
                check_true(
                    type(v) is list,
                    'in module set "{0}": addon_deps does not entirely consist of lists.'
                )
                tmp = []
                for vv in v:
                    addon_name.check(vv)
                    tmp.append(vv)

                self.addon_dependencies.append(tmp)

        __depth.pop()
