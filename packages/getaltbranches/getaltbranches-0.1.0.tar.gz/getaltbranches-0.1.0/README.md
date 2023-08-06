# getaltbranches

A lightweight library for getting branches from public REST API https://rdb.altlinux.org/api/

## Description

This library allows to get information to a console about binary branches (_sisyphus, p10, p9_) using the method _/export/branch_binary_packages/{branch}_.

## Getting Started

### Dependencies

The utility runs under all OS including Linux.

### Installing

Install this module with pip: `pip install getaltbranches`

### Executing program

After installing, you have several features:
* ```get_branches_packages(first branch, second branch, architecture[optional])``` 

  Get lists of binary packages of 2 branches or lists with a specific architecture. <br/><br/>
   
* ```first_branch_unique_packages(first branch, second branch, architecture[optional])```

  Makes a comparison of the received package lists (with specific architecture or not) and outputs JSON, which will display all packages that are in the 1st branch but not in the 2nd. <br/><br/>

* ```second_branch_unique_packages(first branch, second branch, architecture[optional])```

  Makes a comparison of the received package lists (with specific architecture or not) and outputs JSON, which will display all packages that are in the 2nd branch but not in the 1st. <br/><br/>

* ```unique_version_release(first branch, second branch, architecture[optional])```

  Makes a comparison of the received package lists (with specific architecture or not) and outputs JSON, which will display all packages whose "version-release" is more in the 1st than in the 2nd.

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

* [basealt](https://www.basealt.ru/)
