import yaml
from sys import argv
from itertools import permutations, chain, product


class K8SAliasgen:
    KEY_API_CMDS = "api_cmds"
    KEY_CMD = "cmd"
    KEY_API_RESOURCES = "api_resources"
    KEY_OPTS = "opts"
    KEY_OPT = "opt"
    KEY_PARAMETRIC = "parametric"
    KEY_EXCLUDE_RESOURCES = "exclude_resources"
    KEY_EXCLUDE_OPTS = "exclude_opts"

    def __init__(self, config_filename="config.yml"):
        self.__config = yaml.safe_load(open(config_filename, "r"))
        self.__api_cmds = self.__config[self.KEY_API_CMDS]
        self.__api_resources = self.__config[self.KEY_API_RESOURCES]

    def generate(self):
        aliases = []

        with open(self.__config["output_filename"], "w") as file:
            for api_cmd_alias in self.__api_cmds.keys():
                opts_config = self.__api_cmds[api_cmd_alias].get(self.KEY_OPTS, {})

                api_cmd_opts = {
                    opt_alias: opt_info[self.KEY_OPT]
                    for opt_alias, opt_info in opts_config.items()
                }

                for (resource_alias, resource_id), opts in product(self.__api_resources.items(),
                                                                   chain(*[
                                                                       permutations(api_cmd_opts.items(), r)
                                                                       for r in range(0, len(api_cmd_opts) + 1)
                                                                   ])):
                    opt_aliases = [opt[0] for opt in opts]
                    opt_cmds = [opt[1] for opt in opts]
                    parametric_opts_count = len([
                        opt_alias
                        for opt_alias in opt_aliases
                        if opts_config[opt_alias].get(self.KEY_PARAMETRIC, False)
                    ])
                    valid_alias = True

                    if resource_alias in self.__api_cmds[api_cmd_alias].get(self.KEY_EXCLUDE_RESOURCES, []):
                        valid_alias = False
                    else:
                        for opt_alias in opt_aliases:
                            if resource_alias in opts_config[opt_alias].get(self.KEY_EXCLUDE_RESOURCES, []):
                                valid_alias = False

                            for ignored_opt in opts_config[opt_alias].get(self.KEY_EXCLUDE_OPTS, []):
                                if ignored_opt in opt_aliases:
                                    valid_alias = False
                                    break

                            if not valid_alias:
                                break

                    if not valid_alias:
                        continue

                    if parametric_opts_count > 0:
                        aliases.append(
                            ("alias k{api_cmd_alias}{res_alias}{opt_aliases}='"
                             "function _k{api_cmd_alias}{res_alias}{opt_aliases}() {{ "
                             "kubectl {api_cmd} {res_id} {opts}; }}; "
                             "echo \"kubectl {api_cmd} {res_id} {opts}\"; "
                             "_k{api_cmd_alias}{res_alias}{opt_aliases}'\n").format(
                                api_cmd_alias=api_cmd_alias,
                                api_cmd=self.__api_cmds[api_cmd_alias][self.KEY_CMD],
                                res_alias=resource_alias,
                                opt_aliases="".join(opt_aliases),
                                opts=" ".join(opt_cmds).format(*range(1, parametric_opts_count + 1)),
                                res_id=resource_id
                            )
                        )
                    else:
                        aliases.append(
                            ("alias k{api_cmd_alias}{res_alias}{opt_aliases}="
                             "'echo \"kubectl {api_cmd} {res_id} {opts}\"; "
                             "kubectl {api_cmd} {res_id} {opts}'\n").format(
                                api_cmd_alias=api_cmd_alias,
                                api_cmd=self.__api_cmds[api_cmd_alias][self.KEY_CMD],
                                res_alias=resource_alias,
                                opt_aliases="".join(opt_aliases),
                                opts=" ".join(opt_cmds),
                                res_id=resource_id
                            )
                        )

            file.writelines(aliases)


if __name__ == "__main__":
    try:
        K8SAliasgen(config_filename=argv[1]).generate()
    except:
        print("usage: python k8s_aliasgen.py <config_filename>")