# Flexible distributed matrix multiplication

### Project specs:
- A cloud-based Azure web application using Flask connected to a distributed backend using AKS for reliability and load-balancing
![diagram](https://user-images.githubusercontent.com/14797495/203980866-f5b35e32-63ac-4f14-a01b-a25076ca0ecd.png)
- Auto Scaling up to eight worker nodes by estimating workload by the input deadline
- Matrix multiplication algorithm: Non-recursive divide-and-conquer (optimal packet size for matrix 2^13 x 2^13 or smaller)

### Future works for better scalability:
- Matrix multiplication algorithm: Dynamic recursion layers for optimal packet size communication to improve multiplication performance
- Infrastructure:
    - Horizontal scaling: Create a cluster within a GCP zone for better bandwidth
    - Vertical scaling: Host cluster nodes on each CPU in a high-performance compute engine with high CPUs number to eliminate the network overhead cost
