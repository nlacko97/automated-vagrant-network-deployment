### This script is used to perform the task of creating a Vagrantfile based on user input to provide a network topology.
# The user can choose between the given network topolgies: for now we have two options: 
# Star: Basic configuration consisting of two hosts and one switch
# Complex: More complex bus configuration: hosts + switch + router
# The script prompts the user for the: number of hosts, bandwidth allocation, delay configuration
# We create a data structure containing all the user inputs and a template Vagrantfile
# Using template substitution, we provide the data for the template and generate the final Vagrantfile, that
# can be used to create the network based on the parameters provided by running the 'vagrant up' command
# Testing the configuration can be done by doing ping operations, using netperf program and running benchmarks.

from statistics import variance
import string
import os

def import_template(fpath="Vagrantfile_template", text_needed=False):
    with open(fpath) as t:
        text = t.read()
        template = string.Template(text)
    t.close()
    if text_needed:
        return template, text
    else:
        return template

def export_config(config, fpath="Vagrantfile_generated"):
    print(config)
    with open(fpath, "w") as output:
        output.write(config)
    output.close()

def generate_component_templates(n_hosts, n_switches, host_names, switch_names):
    gen_hosts = ""
    gen_switches = ""
    gen_ports = ""

    # Generating Hosts
    host_template = import_template("host_template")    
    for i in range(0, n_hosts):
        gen_hosts += host_template.substitute(**host_names[i]) + "\n"
    # Aligning the code by removing fist 2 spaces
    gen_hosts = gen_hosts[2:]

    # Generating Switch Ports
    port_template, switch_text = import_template("port_template", True)
    switch_text = switch_text.replace("    ", "")
    for i in range(0, n_hosts):
        gen_ports += switch_text + "\n    "
    
    # Generating Switches
    switch_template, switch_text = import_template("switch_template", True)
    for i in range(0, n_switches):
        switch_text = switch_text.replace("${ports}", gen_ports)
        switch_template = string.Template(switch_text)
        gen_switches += switch_template.substitute(**switch_names[i])
    # Aligning the code by removing the last \n
    gen_switches = gen_switches[:len(gen_switches) - 1]

    #TODO Generate and configure file for each component
    return gen_hosts, gen_switches

if __name__ == "__main__":

    os.system('cls')
    print("Starting configurator script")

    # Ask user for number of hosts
    # n_hosts = input("Enter number of hosts: (Default=2) ")
    # n_hosts = int(n_hosts) if n_hosts != '' else 2
    n_hosts = 3
    n_switches = 1

    # Generate host names ( {'hostname1': 'host-a', 'hostname2': 'host-b'} )
    host_names = []
    switch_names = []
    for i in range(0, n_hosts):
        host_names.append({"hostname": "host_" + chr(ord('a') + i), "host_variable_name" : "host" + chr(ord('a') + i)})
        switch_names.append({"switchname": "switch_" + chr(ord('a') + i), "switch_variable_name" : "switch" + chr(ord('a') + i), "hostname": "host_" + chr(ord('a') + i)})

    # Import empty template to be populated with components
    template = import_template()
    
    # Generate components (Routers, Switches, Hosts)
    gen_hosts, gen_switches = generate_component_templates(n_hosts, n_switches, host_names, switch_names)

    # Adding components to the config template
    data = {'hosts': gen_hosts, 'switches': gen_switches}
    final_config = template.substitute(**data)

    # Export the final config
    export_config(final_config)

    print("Finalized generating Vagrantfile.")