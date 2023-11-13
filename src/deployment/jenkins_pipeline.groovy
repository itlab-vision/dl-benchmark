node {
    
	def workersIP = ['ip_1','ip_2']
	def deploy_config = '''<?xml version="1.0" encoding="utf-8" ?>
<Computers>
	<Computer>
    	<IP>ip1</IP>
    	<Login>user_login</Login>
    	<Password>user_password</Password>
    	<OS>Linux</OS>
    	<DownloadFolder>/home/user_login/dli-jenkins-worker</DownloadFolder>
    	<DatasetFolder>/mnt/datasets</DatasetFolder>
    	<ModelFolder>/mnt/models</ModelFolder>
	</Computer>
    <Computer>
    	<IP>ip2</IP>
    	<Login>user_login</Login>
    	<Password>user_password</Password>
    	<OS>Linux</OS>
    	<DownloadFolder>/home/user_login/dli-jenkins-worker</DownloadFolder>
    	<DatasetFolder>/mnt/datasets</DatasetFolder>
    	<ModelFolder>/mnt/models</ModelFolder>
	</Computer>
</Computers>'''
    
    
    
	stage('Clone repository') {
    	git url: 'https://github.com/itlab-vision/dl-benchmark.git', branch: 'master'
	}
	stage('Build docker') {
    	sh 'docker build -t ubuntu_for_dli --build-arg DATASET_DOWNLOAD_LINK="https://<github_user>:<github_user_gpg>@github.com/<repo_with_your_bench_dataset>.git" docker/'
    	sh 'docker build -t openvino:2022.3 docker/OpenVINO_DLDT'
    	sh 'docker save openvino:2022.3 > openvino_2022.3.tar' 
	}
	stage('Prepare workers') {
    	workersIP.each { item ->
    	def remote = [:]
    	remote.name = '<user_login>'
    	remote.host = item
    	remote.user = '<user_login>'
    	remote.password = '<user_password>'
    	remote.allowAnyHosts = true
    	remote.pty  = true
    	sshCommand remote: remote, command: "hostname -I"
    	sshCommand remote: remote, command: "mkdir -p /home/<user_login>/dli-jenkins-worker && cd /home/<user_login>/dli-jenkins-worker"
    	sshCommand remote: remote, command: 'cd /home/<user_login>/dli-jenkins-worker && git -C $"dl-benchmark" pull || git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1 dl-benchmark'
    	sshCommand remote: remote, command: 'cd /home/<user_login>/dli-jenkins-worker && git -C $"open_model_zoo" pull || git clone https://github.com/openvinotoolkit/open_model_zoo.git --recursive --branch 2022.3.0 --single-branch --depth 1 open_model_zoo'
    	sshCommand remote: remote, command: "mkdir -p /home/<user_login>/dli-jenkins-worker/results"
   	 
    	//Mount shared folder with models and datasets
    	sshCommand remote: remote, command: 'mountpoint -q /mnt && echo "Directory already mounted" || sudo mount -t cifs -o username=<ftp_login>,password=<ftp_password> //<ip_linuxshare>/linuxshare /mnt', sudo: true, pty:true
    	}
	}
	stage('Deploy docker on workers') {
    	sh 'touch deploy_config.xml'
    	sh 'echo ${deploy_config} >> deploy_config.xml'
    	sh 'python3 src/deployment/deploy.py -s <share_ip> -l <share_login> -p <share_password> -i ./openvino_2022.3.tar -d /home/<ftp_login>/ftp -n OpenVINO_DLDT --machine_list ./deploy_config.xml --project_folder /home/<user_login>/dli-jenkins-worker/dl-benchmark'

	}
	stage('Remote start') {
   	 
    	def remote = [:]
    	remote.name = 'ftp_login'
    	remote.host = 'ftp_ip'
    	remote.user = 'ftp_login'
    	remote.password = 'ftp_password'
    	remote.allowAnyHosts = true
    	remote.pty  = true
   	 
    	sshCommand remote: remote, command: "python3 /home/<ftp_login>/ftp/dl-benchmark/src/remote_control/remote_start.py -c /home/<ftp_login>/ftp/jenkins_remote_configs/openvino_2022.3/config.xml -s <ftp_ip> -l <ftp_login> -p <ftp_pass> -acr accuracy_checker_results.csv -br benchmark_results.csv --ftp_dir /home/<ftp_login>/ftp/jenkins_results"
    	sshCommand remote: remote, command: "python3 /home/<ftp_login>/ftp/dl-benchmark/src/remote_control/remote_start.py -c /home/<ftp_login>/ftp/jenkins_remote_configs/openvino_2022.3/config.xml -s <ftp_ip> -l <ftp_login> -p <ftp_pass> -acr accuracy_checker_results.csv -br benchmark_results.csv --ftp_dir /home/<ftp_login>/ftp/jenkins_results"
	}
	stage('Convert results') {
	}
}
