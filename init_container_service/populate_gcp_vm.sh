#!/usr/bin/env bash

# Auto populating 7 EC2 instances from the based VM image
for ((i=1; i<=7; i++))
do
    gcloud beta compute instances create grpc-vm-$i \
        --project=fluted-cogency-340019 \
        --zone=us-central1-a \
        --machine-type=e2-micro \
        --network-interface=network-tier=PREMIUM,subnet=default \
        --metadata=^,@^ssh-keys=mduc458:ecdsa-sha2-nistp256\ AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAqm48qlacNS8E7RnnxDhlsj0GpcDqgNW9eEgFjSyDPvJjVuP5GR7VbinrZoewtNx57Dkh5Pr9Pz3fZOwIjk3aM=\ google-ssh\ \{\"userName\":\"mduc458@gmail.com\",\"expireOn\":\"2022-04-20T05:47:17\+0000\"\}$'\n'mduc458:ssh-rsa\ AAAAB3NzaC1yc2EAAAADAQABAAABAQDBJc3un9NwvHo6EAKhjFzPCRqHGIVWMGQcnIx54YRw4dauS5SIXxHVzD/sKRu4zy0xgjDnR3G8UY9zPhh13Jw2aCIdm0yyf6klaXuHE8MkHRxGppFUZzNGVBUUL3u0uGEmE1qa42ZtLoqP34BZX5C6b3SvAOQUJhjDM6XRANAhIm3LFVptYRB6p5vjesZha8e5eQLspqFkgqzrMZC65HYLqPWL4vTPy6XX4caeKYlqgvFq7/goddaTRaQsWmkRQPx1o1\+7AHxhZhGBm\+khvFUjGUY8mV91/Mb7pvL5ykhv8F3rwASM3pn\+lQLySuWARh4oJP4n3pkxxT1Uu3kAqAQZ\ google-ssh\ \{\"userName\":\"mduc458@gmail.com\",\"expireOn\":\"2022-04-20T05:47:32\+0000\"\} \
        --maintenance-policy=MIGRATE \
        --provisioning-model=STANDARD \
        --service-account=990230744444-compute@developer.gserviceaccount.com \
        --scopes=https://www.googleapis.com/auth/cloud-platform \
        --min-cpu-platform=Automatic \
        --tags=http-server,https-server \
        --no-shielded-secure-boot \
        --shielded-vtpm \
        --shielded-integrity-monitoring \
        --reservation-affinity=any \
        --source-machine-image=grpc-vm;
done
