% Flexible distributed matrix multiplication
% Minh Duc Nguyen
% Apr 2022

## Project specs:
- A cloud-based web application using Flask connected to a distributed system with Client-Side Load-Balancing
- Auto Scaling up to eight worker nodes by estimating workload by the input deadline
- Matrix multiplication algorithm: Non-recursive divide-and-conquer (optimal packet size for matrix 2^13 x 2^13 or smaller)

## Future works for better scalability:
- Matrix multiplication algorithm: Dynamic recursion layers for optimal packet size communication to improve multiplication performance
- Infrastructure:
    - Horizontal scaling: Create a cluster within a GCP zone for better bandwidth
    - Vertical scaling: Host all cluster's nodes on each CPU in a high performance compute engine with high CPUs number to eliminate the network overhead cost