# Amazon Elastic Load Balancing Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-elasticloadbalancing` package provides constructs for configuring
classic load balancers.

## Configuring a Load Balancer

Load balancers send traffic to one or more AutoScalingGroups. Create a load
balancer, set up listeners and a health check, and supply the fleet(s) you want
to load balance to in the `targets` property.

```python
# vpc: ec2.IVpc

# my_auto_scaling_group: autoscaling.AutoScalingGroup

lb = elb.LoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True,
    health_check=elb.HealthCheck(
        port=80
    )
)
lb.add_target(my_auto_scaling_group)
lb.add_listener(
    external_port=80
)
```

The load balancer allows all connections by default. If you want to change that,
pass the `allowConnectionsFrom` property while setting up the listener:

```python
# my_security_group: ec2.SecurityGroup
# lb: elb.LoadBalancer

lb.add_listener(
    external_port=80,
    allow_connections_from=[my_security_group]
)
```
