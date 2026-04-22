import sys

import pkg_resources

def check_dependencies(requirements_file):

   try:

       with open(requirements_file, "r") as f:

           required = f.read().splitlines()

       installed = {pkg.key for pkg in pkg_resources.working_set}

       missing = []

       for package in required:

           pkg_name = package.split("==")[0].lower()

           if pkg_name not in installed:

               missing.append(pkg_name)

       if missing:

           print("ERROR: Missing dependencies detected:")

           for m in missing:

               print(f" - {m}")

           sys.exit(1)

       print("All dependencies are installed correctly.")

   except Exception as e:

       print(f"Dependency check failed: {str(e)}")

       sys.exit(1)


if __name__ == "__main__":

   check_dependencies("requirements.txt")
 