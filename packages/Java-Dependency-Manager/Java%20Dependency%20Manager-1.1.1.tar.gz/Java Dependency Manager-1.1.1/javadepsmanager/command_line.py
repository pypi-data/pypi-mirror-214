import javadepsmanager
import requests
import subprocess
import os
import sys

MAXIMUM_SEARCH_RESULTS = 15
OUTPUT_DIR = os.path.join(os.path.expanduser('~'), '.jdm')
DEPENDENCIES_DIR = os.path.join(OUTPUT_DIR, 'dependencies')
if sys.platform == 'win32':
    SHELL = True  # Use shell=True for PowerShell on Windows
else:
    SHELL = False  # Use shell=False for macOS (and other Unix-like systems)


session = requests.Session()
base_url = 'https://repo1.maven.org/maven2'

def print_in_color(text, color):
    if color == "red":
        print("\033[91m {}\033[00m" .format(text))
    elif color == "green":
        print("\033[92m {}\033[00m" .format(text))
    elif color == "yellow":
        print("\033[93m {}\033[00m" .format(text))
    elif color == "blue":
        print("\033[94m {}\033[00m" .format(text))
    elif color == "magenta":
        print("\033[95m {}\033[00m" .format(text))
    elif color == "cyan":
        print("\033[96m {}\033[00m" .format(text))
    elif color == "white":
        print("\033[97m {}\033[00m" .format(text))
    else:
        print(text)

def advanced_search(q):
    url = "https://central.sonatype.com/api/internal/browse/components"
    payload = {
        "filter": [],
        "page": 0,
        "searchTerm": q,
        "size": MAXIMUM_SEARCH_RESULTS,
    }
    response = session.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["components"]

def search(q):
    url = f"https://search.maven.org/solrsearch/select?q={q}&rows=20&wt=json"
    response = session.get(url)
    response.raise_for_status()
    return response.json()["response"]["docs"]

def parse_pom_link(link):
    link = link.replace("https://repo1.maven.org/maven2/", "")
    link = link.split("/")
    group_id = ".".join(link[:-3])
    artifact_id = link[-3]
    version = link[-2]
    return group_id, artifact_id, version

def save_dependencies_list(group_id, artifact_id, version, nopom=False):
    if not nopom:
        print("Downloading POM.xml for version", version)
        save_pom(group_id, artifact_id, version)
    print("Generating dependencies list for version", version)
    file_path = os.path.join(DEPENDENCIES_DIR, f"{artifact_id}-{version}-list.txt")
    cmd = ["mvn", "dependency:list", "-Dstyle.color=never", "-Dsort=true","-DincludeScope=runtime", f"-DoutputFile={file_path}"]
    subprocess.run(cmd, capture_output=True, text=True, cwd=OUTPUT_DIR,shell=SHELL)


def parse_dependencies_list(file_name):
    file_path = os.path.join(DEPENDENCIES_DIR, file_name)
    with open(file_path) as f:
        lines = f.readlines()
    dependencies = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line == "The following files have been resolved:":
            continue
        if "--" in line:
            dependencies.append(line.split("--")[0].strip()[:-7])
        else:
            dependencies.append(line[:-7])
    return dependencies

def process_dependencies(dep1, dep2):
    dependencies1 = []
    dependencies2 = []
    for dep in dep1:
        dep = " >> ".join(dep.split(":")[:2])
        dependencies1.append(dep)
    for dep in dep2:
        dep = " >> ".join(dep.split(":")[:2])
        dependencies2.append(dep)
    return dependencies1, dependencies2

def save_dependency_tree(group_id, artifact_id, version):
    print(f"Downloading POM file for {artifact_id} v{version}...")
    save_pom(group_id, artifact_id, version)
    print(f"Generating dependency tree for {artifact_id} v{version}...")
    file_path = os.path.join(DEPENDENCIES_DIR, f"{artifact_id}-{version}-tree.txt")
    cmd = ["mvn", "dependency:tree", "-Dscope=runtime", f"-DoutputFile={file_path}"]
    subprocess.run(cmd, capture_output=True, text=True, cwd=OUTPUT_DIR,shell=SHELL)
    with open(file_path) as f:
        content = f.read()
    lines = content.split("\n")
    newlines = []
    for line in lines:
        if line.endswith("compile") or line.endswith("runtime"):
            newlines.append(line[:-7])
        elif "compile (optional)" in line:
            newlines.append(line.replace("compile (optional)", " (optional)"))
        elif "runtime (optional)" in line:
            newlines.append(line.replace("runtime (optional)", " (optional)"))
        else:
            newlines.append(line)
    newcontent = "\n".join(newlines)
    with open(file_path, "w") as f:
        f.write(newcontent)
    # get the full path of the file
    abs_file_path = os.path.abspath(file_path)
    print_in_color(f"\nDependency tree for {artifact_id} v{version} saved to {abs_file_path}", "green")
    print("----------------------------------------")
    print(f"Dependency tree for {artifact_id} v{version}:\n")
    print_in_color(newcontent, "cyan")
    print("----------------------------------------\n")
    return newcontent

def save_pom(group_id, artifact_id, version):
    group_url = group_id.replace(".","/")
    url = f"{base_url}/{group_url}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    response = session.get(url)
    if response.status_code == 404:
        print_in_color(f"POM not found for version {version} of {artifact_id}. Possible reasons might be version is incorrect or artifact might be moved.", "red")
        sys.exit()
    response.raise_for_status()
    xml = response.content.decode("utf-8")
    pom_path = os.path.join(OUTPUT_DIR, "pom.xml")
    with open(pom_path,"w") as f:
        f.write(xml)

def main():
    keeppom = False
    compare_versions = False
    version = None
    version2 = None
    choice = None
    results = None
    if(len(sys.argv) > 1 and sys.argv[1] == "keeppom"):
        keeppom = True
    
    print_in_color("Welcome to Java Dependency Manager", "green")
    if not os.path.exists(DEPENDENCIES_DIR):
        os.makedirs(DEPENDENCIES_DIR)

    query = input("Enter the maven artifact name to search (or pom.xml url): ")
    if(query.startswith("https://repo1.maven.org/maven2/")):
        group_id, artifact_id, version = parse_pom_link(query)
        print(f"Selected {group_id} >> {artifact_id} >> {version}")
    else:
        results = advanced_search(query)
        if(len(results) == 0):
            print_in_color("No results found for the given query", "red")
            sys.exit()
        for i,result in enumerate(results, start=1):
            print(f"{i}. {result['namespace']} >> {result['name']} -- {result['latestVersionInfo']['version']}(latest)")
        print_in_color("\nIf you cannot find the required artifact, try using the pom.xml url option\n", "magenta")
        choice = input("Select an option to proceed (or pom.xml url): ")
        if(choice.startswith("https://repo1.maven.org/maven2/")):
            group_id, artifact_id, version = parse_pom_link(choice)
            choice = None
            print(f"Selected {group_id} >> {artifact_id} >> {version}")
        else:
            if(choice == ""):
                choice = 0
            else:
                try:
                    choice = int(choice) - 1
                except:
                    print_in_color("Invalid choice", "red")
                    sys.exit()
            if(choice < len(results) and choice >= 0):
                group_id = results[choice]["namespace"]
                artifact_id = results[choice]["name"]
            else:
                print("Invalid choice")
                sys.exit()

            print(f"Selected {group_id} >> {artifact_id}")

    compare = input("Do you want to Compare versions?(y/n) [N]: ")
    if(compare.lower() == "y" or compare.lower() == "yes"):
        compare_versions = True

    if not version:
        version = input(f"Enter the required version or leave empty to use latest version: ").strip()
        if(version == ""):
            version = results[choice]['latestVersionInfo']['version']
    
    if(compare_versions):
        if choice:
            version2 = input(f"Enter the second version to compare with or leave empty to use latest version: ").strip()
            if(version2 == ""):
                version2 = results[choice]['latestVersionInfo']['version']
        else:
            version2 = input(f"Enter the second version to compare with: ").strip()
            while(version2 == ""):
                version2 = input(f"Enter the second version to compare with: ").strip()
        print_in_color(f"Comparing {version} and {version2}", "magenta")

    save_dependency_tree(group_id, artifact_id, version)
    if(compare_versions):
        save_dependencies_list(group_id, artifact_id, version, nopom=True)
        dependencies1 = parse_dependencies_list(f"{artifact_id}-{version}-list.txt")
        save_dependency_tree(group_id, artifact_id, version2)
        save_dependencies_list(group_id, artifact_id, version2, nopom=True)
        dependencies2 = parse_dependencies_list(f"{artifact_id}-{version2}-list.txt")
        dependencies1, dependencies2 = process_dependencies(dependencies1, dependencies2)
        print()
        print_in_color(f"Dependencies in version {version} but not in version {version2}:\n", "yellow")
        deps_in_version1 = list(set(dependencies1) - set(dependencies2))
        deps_in_version2 = list(set(dependencies2) - set(dependencies1))
        if(len(deps_in_version1) == 0):
            print_in_color("None", "red")
        else:
            print_in_color("\n".join(deps_in_version1), "red")
        print("\n----------------------------------------\n")
        print_in_color(f"Dependencies in version {version2} but not in version {version}:\n", "yellow")
        if(len(deps_in_version2) == 0):
            print_in_color("None", "red")
        else:
            print_in_color("\n".join(deps_in_version2), "red")
        print()
        list1_path = os.path.join(DEPENDENCIES_DIR, f"{artifact_id}-{version}-list.txt")
        list2_path = os.path.join(DEPENDENCIES_DIR, f"{artifact_id}-{version2}-list.txt")
        os.remove(list1_path)
        os.remove(list2_path)

    if(not keeppom):
        os.remove(os.path.join(OUTPUT_DIR, "pom.xml"))

if __name__ == "__main__":
    main()