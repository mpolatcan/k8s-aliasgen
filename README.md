# k8s-aliasgen

Configurable, customizable alias generator for Kubernetes command inspired from @ahmetb's **kubectl-aliases** project

## Usage

    python k8s_aliasgen.py config.yml
        
## Config Structure and Example Config

### Config Structure

```yaml
output_filename: # string
api_resources:
   <resource_1_alias>: # <resource_1_id>
   <resource_2_alias>: # <resource_2_id>
#   ...
   <resource_n_alias>: # <resource_n_id>


api_cmds:
  <api_cmd_1_alias>:
    cmd: # (string)
    opts:
      <opt_1_alias>:
        opt: # (string)
        exclude_resources>: # (list: optional)
        exclude_opts>: # (list: optional)
        parametric>: # (bool: optional)
#      ...
      <opt_n_alias>:
        opt: # (string)
        exclude_resources>: # (list: optional)
        exclude_opts>: # (list: optional)
        parametric: # (bool: optional)
    exclude_resources: # (list: optional)
#   ....
  <api_cmd_n_alias>:
    cmd: # (string)
    opts:
      <opt_1_alias>:
        opt: # (string)
        exclude_resources: # (list: optional)
        exclude_opts: # (list: optional)
        parametric: # (bool: optional)
#       ...
      <opt_n_alias>:
        opt: # (string)
        exclude_resources: # (list: optional)
        exclude_opts: # (list: optional)
        parametric: # (bool: optional)
    exclude_resources: #(list: optional)
```

### Config Example

```yaml
output_filename: ".k8s_aliases"

api_resources:
  "no": "no"
  pv: "pv"
  pvc: "pvc"
  sec: "secret"
  po: "po"
  svc: "svc"
  ing: "ing"
  dep: "deploy"
  sts: "sts"
  hpa: "hpa"


api_cmds:
  g:
    cmd: "get"
    opts:
      all:
        opt: "--all-namespaces"
        exclude_resources: ["no"]
      w:
        opt: "--watch"
        exclude_resources: ["pv", "pvc", "sec", "svc", "ing"]
        exclude_opts: ["ojson", "oyaml"]
      sl:
        opt: "--show-labels"
        exclude_opts: ["ojson", "oyaml"]
      l:
        opt: "-l ${}"
        parametric: true
        exclude_resources: ["no"]
      ns:
        opt: "-n ${}"
        parametric: true
        exclude_resources: ["no"]
      owide:
        opt: "-o wide"
        exclude_opts: ["oyaml", "ojson"]
      oyaml:
        opt: "-o yaml"
        exclude_opts: ["w", "owide", "ojson"]
      ojson:
        opt: "-o json"
        exclude_opts: ["w", "owide", "oyaml"]

  rm:
    cmd: "delete"
    exclude_resources: ["no"]

  d:
    cmd: "describe"
    exclude_resources: ["no"]
```