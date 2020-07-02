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
    cmd: # (string - Kubectl command)
    opts:
      <opt_1_alias>:
        opt: # (string)
        exclude_resources: # (list: optional - Exclude resources for this option of command if you don't want)
        exclude_opts: # (list: optional - Exclude combinations with these opts if defined)
        parametric: # (bool: optional - Option is parametric or not)
        resource_specific: # (bool: optional - Option is resource specific or not)
#      ...
      <opt_n_alias>:
        opt: # (string)
        exclude_resources: # (list: optional)
        exclude_opts: # (list: optional)
        parametric: # (bool: optional)
        resource_specific: # (bool: optional)
    exclude_resources: # (list: optional - Exclude resources for this command if you don't want)
    resource_specific: # (bool: optional - Command is resources specific or not)
#   ....
  <api_cmd_n_alias>:
    cmd: # (string)
    opts:
      <opt_1_alias>:
        opt: # (string)
        exclude_resources: # (list: optional)
        exclude_opts: # (list: optional)
        parametric: # (bool: optional)
        resource_specific: # (bool: optional)
#       ...
      <opt_n_alias>:
        opt: # (string)
        exclude_resources: # (list: optional)
        exclude_opts: # (list: optional)
        parametric: # (bool: optional)
        resource_specific: # (bool: optional)
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
  cj: "cj"
  j: "jobs"


api_cmds:
  g:
    cmd: "get"
    opts:
      all:
        opt: "--all-namespaces"
        exclude_resources:
          - "no"
        exclude_opts:
          - "ns"
      # ========================
      w:
        opt: "--watch"
        exclude_resources:
          - "pv"
          - "pvc"
          - "sec"
          - "svc"
          - "ing"
        exclude_opts:
          - "ojson"
          - "oyaml"
      # ========================
      sl:
        opt: "--show-labels"
        exclude_opts:
          - "ojson"
          - "oyaml"
      # ========================
      l:
        opt: "-l ${}"
        parametric: true
        exclude_resources:
          - "no"
      # ========================
      ns:
        opt: "-n ${}"
        parametric: true
        exclude_opts:
          - "all"
        exclude_resources:
          - "no"
      # ========================
      owide:
        opt: "-o wide"
        exclude_opts:
          - "oyaml"
          - "ojson"
      # ========================
      oyaml:
        opt: "-o yaml"
        exclude_opts:
          - "w"
          - "owide"
          - "ojson"
      # ========================
      ojson:
        opt: "-o json"
        exclude_opts:
          - "w"
          - "owide"
          - "oyaml"
      # ========================

# ==============================================================

  rm:
    cmd: "delete"
    opts:
      all:
        opt: "--all-namespaces"
        exclude_opts:
          - "ns"
      # ========================
      l:
        opt: "-l ${}"
        parametric: true
      # ========================
      ns:
        opt: "-n ${}"
        parametric: true
        exclude_opts:
          - "all"
      # ========================
      f:
        opt: "-f ${}"
        parametric: true
        exclude_opts:
          - "k"
        resource_specific: false
      # ========================
      k:
        opt: "-k ${}"
        parametric: true
        exclude_opts:
          - "f"
        resource_specific: false
        # ========================
    exclude_resources:
      - "no"

# ==============================================================

  d:
    cmd: "describe"
    opts:
      all:
        opt: "--all-namespaces"
        exclude_opts:
          - "ns"
      # ========================
      l:
        opt: "-l ${}"
        parametric: true
      # ========================
      ns:
        opt: "-n ${}"
        parametric: true
        exclude_opts:
          - "all"
      # ========================
      r:
        opt: "--recursive"
      # ========================
      f:
        opt: "-f ${}"
        parametric: true
        exclude_opts:
          - "k"
        resource_specific: false
      # ========================
      k:
        opt: "-k ${}"
        parametric: true
        exclude_opts:
          - "f"
        resource_specific: false
        # ========================
    exclude_resources:
      - "no"

# ==============================================================

  e:
    cmd: "edit"
    opts:
      ns:
        opt: "-n ${}"
        parametric: true
      # ========================
    exclude_resources:
      - "no"

# ==============================================================

  log:
    cmd: "logs"
    opts:
      f:
        opt: "-f"
      # ========================
      l:
        opt: "-l ${}"
        parametric: true
      # ========================
      ns:
        opt: "-n ${}"
        parametric: true
      # ========================
    resource_specific: false

# ==============================================================

  a:
    cmd: "apply"
    opts:
      f:
        opt: "-f ${}"
        parametric: true
        exclude_opts:
          - "k"
      # ========================
      l:
        opt: "-l ${}"
        parametric: true
      # ========================
      k:
        opt: "-k ${}"
        parametric: true
        exclude_opts:
          - "f"
      # ========================
      r:
        opt: "--recursive"
      # ========================
      ns:
        opt: "-n ${}"
        parametric: true
      # ========================
    resource_specific: false
```