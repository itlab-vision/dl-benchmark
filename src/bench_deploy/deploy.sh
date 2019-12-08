#!/bin/bash

while [ $# -ne 0 ]
do
    case $1 in
        -h|--help)
            echo "-d <link> -c <config_name> -u <username> -p <password>"
            exit 0
            ;;
        -d)
            shift
            download_link=$1
            ;;
        -c)
            shift
            config_file=$1
            ;;
        -u)
            shift
            username=$1
            ;;
        -p)
            shift
            password=$1
            ;;
    esac
    shift
done

if [ "$download_link" == "" ]; then
    echo "No argument download_link"
    exit 1
elif [ "$config_file" == "" ]; then
    echo "No argument config_file"
    exit 1
elif [ "$username" == "" ]; then
    echo "No argument username"
    exit 1
elif [ "$password" == "" ]; then
    echo "No argument password"
    exit 1
fi


echo "Start on all machines"
for var in $(cat $config_file)
do
        sshpass -p $password ssh -n -f $username@$var "sh -c 'cd ~/Documents/;
            git clone https://github.com/TheG1uy/openvino-dl-benchmark;
            cd ~/Documents/openvino-dl-benchmark && git checkout bench_deploy;
            cd ~/Documents/openvino-dl-benchmark/src/bench_deploy &&
            chmod u+x client.sh && chmod u+x dependencies.sh;
            cd ~/Documents/openvino-dl-benchmark/src/bench_deploy &&
            nohup echo $password | sudo -S ./client.sh $1 > ./log.txt 2>&1 &'"
done

echo "Run client script"
sudo ./client.sh $1
cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader
source ~/Documents/benchmark/OpenVINO_env/bin/activate

python3 -mpip install --user -r ./requirements.in

echo "Wait all machines"
for var in $(cat $config_file)
do
    status="Working"
    while [ $status == "Working" ];
    do
        sshpass -p osboxes.org ssh -n -f osboxes@10.0.2.15 "sh -c 'if [ $(ps fx | grep client.sh | wc -l) -ne 1 ]; 
            then cd ErrorPath; fi'" > ~/Documents/openvino-dl-benchmark/src/bench_deploy/log.txt 2>&1
        sleep 5
        if [ $(cat ~/Documents/openvino-dl-benchmark/src/bench_deploy/log.txt | wc -l) -eq 0 ]; then
            status="Done"
        else
            sleep 120
        fi
    done

    sshpass -p osboxes.org ssh -n -f osboxes@10.0.2.15 "sh -c 'if [ $(grep InstallSuccess ~/Documents/openvino-dl-benchmark/src/bench_deploy/log.txt | wc -l) -ne 1 ];
        then cd ErrorPath; fi'" > ~/Documents/openvino-dl-benchmark/src/bench_deploy/log.txt 2>&1
    sleep 5
    if [ $(cat ~/Documents/openvino-dl-benchmark/src/bench_deploy/log.txt | wc -l) -eq 0 ]; then
        echo "On machine $var install done with success"
    else
        echo "On machine $var install failed"
    fi
done
