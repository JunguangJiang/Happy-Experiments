# Happy Experiments for Python (HEPY)

### Usage
1. Init workspace 
```shell script
he init --watch ${watch_dir} --ws ${workspace_dir}
```

2. Run one experiment
```shell script
he run --exp ${experiment_name} --code ${code_snapshot} -- ${script}
```
Note that when ${experiment_name} is an old experiment, 
the ${code_snapshot} will always be the origin code for the old experiment.
When ${experiment_name} is an old experiment, the ${code_snapshot} will be
created automatically when not provided. 

Run multiple experiments
```shell script
he run --exp ${experiment_name} --code ${code_snapshot} --script ${script_file}
```

Quick commands for python (mostly used for debugging)
```shell script
hepy --exp ${experiment_name} --code ${code_snapshot} -- ${script}
```

3. Display experiment information
```shell script
he display ${experiment_name}
```