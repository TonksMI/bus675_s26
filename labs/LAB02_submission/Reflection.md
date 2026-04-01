# Lab 2 Reflection

In this lab, both containers ran on your laptop. In production, the preprocessor would run in the warehouse datacenter and the inference API would run in Congo's main datacenter.

**How would the architecture and your `docker run` commands differ if these containers were actually running in separate datacenters?**

Consider:
- How would the preprocessor find the inference API?
- What about the shared volumes?
- What new challenges would arise?


## Your Reflection Below

In a real production environment where the preprocessor and the inference API are in separate datacenters, the architecture would evolve in several ways:

1. **Networking and Discovery**: The preprocessor would need a stable, public URL or a secure private link (like a VPN or AWS Direct Connect) to reach the inference API. Instead of `host.docker.internal` (which only works locally), it would use a domain name like `https://api.congo-returns.com`.
2. **Shared Data and Persistence**: Since physical volumes can't be shared across datacenters, the `incoming/` folder would be local to the warehouse. For results and long-term storage, both services would likely use a centralized object storage service (like Amazon S3) or a distributed database rather than local file system mounts.
3. **Security and Resilience**: The inference API would need robust authentication (API keys or OAuth tokens) and TLS encryption for all traffic. Additionally, the preprocessor would require much more sophisticated retry logic and error handling to manage the increased latency and potential for inter-datacenter network failures.
4. **Scalability**: The main datacenter API would likely be behind a load balancer to handle traffic from multiple warehouse preprocessors across different regions, allowing it to scale independently based on total classification demand.