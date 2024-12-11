# depsync
depsync - is a tool for pulling dependencies (git repositories) of defined versions in defined paths according to configuration file.

## Example
Configuration file example:
```json
{
    "dependencies_path" : ".",
    
    "dep_test1" : {
        "path" : "dep_test1",
        "repo" : "git@github.com:dlyamets/test_repo1.git",
        "version" : "v1.1.0"
    },

    "dep_test2" : {
        "path" : "dep_test2",
        "repo" : "git@github.com:dlyamets/test_repo2.git",
        "version" : "v5.3.1"
    }
}
```
Running syncing script
```bash
./sync_deps.py -cfg dependencies.json
```
All repositories in defined paths in dependencies_path:
```bash
dep_test1 # Contains repo "git@github.com:dlyamets/test_repo1.git" on commit "v1.1.0"

dep_test2 # Contains repo "git@github.com:dlyamets/test_repo2.git" on commit "v5.3.1"
```
