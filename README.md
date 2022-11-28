# Flexible distributed matrix multiplication

### Project specs:
- A cloud-based Azure web application using Flask connected to a distributed backend using AKS for reliability and load-balancing
![Diagram drawio (1)](https://user-images.githubusercontent.com/14797495/204392742-b174ad89-054f-44da-8931-b435864a966a.png)
- Auto Scaling up to eight worker nodes by estimating workload by the input deadline
- Matrix multiplication algorithm: Non-recursive divide-and-conquer (optimal packet size for matrix 2^13 x 2^13 or smaller)

### Future works for better multiplication performance:
- Matrix multiplication algorithm: Dynamic number of recursion layers for optimal packet size between client - server.
- Infrastructure:
    - Horizontal scaling: Scale up the number of replicas on the back-end.
    - Vertical scaling: Host cluster nodes on each CPU in a high-performance compute engine with high CPUs number to eliminate the network overhead cost.
