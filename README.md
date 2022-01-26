# automated-vagrant-network-deployment

## Running the program
User will be able to provide network configuration parameters based on the script prompts.
To run the program:
1. Clone the repository: `git clone https://github.com/nlacko97/automated-vagrant-network-deployment.git`
2. Run the configurator script
    1. Directly: `python configurator.py`
    2. Using Docker: `docker build -t conf .`, then `docker run -it --rm -v $(pwd)/output:/output conf`
3. The generated Vagrantfile will be in the `generated_topology` folder. Run the `vagrant up` command from that folder to deploy 
4. Check the generated VMs are running with `vagrant status` 
5. Connect to any of the VMs to make tests with `vagrant ssh NAME_OF_THE_VM_TO_CONNECT`
 