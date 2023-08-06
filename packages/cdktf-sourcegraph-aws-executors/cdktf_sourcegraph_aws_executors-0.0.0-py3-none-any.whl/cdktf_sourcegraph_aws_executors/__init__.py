'''
# CDKTF Sourcegraph AWS Exeuctors
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Executors(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-sourcegraph-aws-executors.Executors",
):
    '''Defines an Executors based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/sourcegraph/executors/aws/~> 5.0.1 sourcegraph/executors/aws}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zone: builtins.str,
        executor_instance_tag: builtins.str,
        executor_metrics_environment_label: builtins.str,
        executor_queue_name: builtins.str,
        executor_sourcegraph_executor_proxy_password: builtins.str,
        executor_sourcegraph_external_url: builtins.str,
        docker_mirror_boot_disk_size: typing.Optional[jsii.Number] = None,
        docker_mirror_disk_iops: typing.Optional[jsii.Number] = None,
        docker_mirror_http_access_cidr_range: typing.Optional[builtins.str] = None,
        docker_mirror_machine_ami: typing.Optional[builtins.str] = None,
        docker_mirror_machine_type: typing.Optional[builtins.str] = None,
        docker_mirror_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        docker_mirror_static_ip: typing.Optional[builtins.str] = None,
        executor_boot_disk_iops: typing.Optional[jsii.Number] = None,
        executor_boot_disk_size: typing.Optional[jsii.Number] = None,
        executor_docker_auth_config: typing.Optional[builtins.str] = None,
        executor_firecracker_disk_space: typing.Optional[builtins.str] = None,
        executor_firecracker_memory: typing.Optional[builtins.str] = None,
        executor_firecracker_num_cpus: typing.Optional[jsii.Number] = None,
        executor_http_access_cidr_range: typing.Optional[builtins.str] = None,
        executor_job_memory: typing.Optional[builtins.str] = None,
        executor_job_num_cpus: typing.Optional[jsii.Number] = None,
        executor_jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
        executor_machine_image: typing.Optional[builtins.str] = None,
        executor_machine_type: typing.Optional[builtins.str] = None,
        executor_max_active_time: typing.Optional[builtins.str] = None,
        executor_maximum_num_jobs: typing.Optional[jsii.Number] = None,
        executor_maximum_runtime_per_job: typing.Optional[builtins.str] = None,
        executor_max_replicas: typing.Optional[jsii.Number] = None,
        executor_min_replicas: typing.Optional[jsii.Number] = None,
        executor_num_total_jobs: typing.Optional[jsii.Number] = None,
        executor_preemptible_machines: typing.Optional[builtins.bool] = None,
        executor_resource_prefix: typing.Optional[builtins.str] = None,
        executor_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        executor_use_firecracker: typing.Optional[builtins.bool] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        private_networking: typing.Optional[builtins.bool] = None,
        randomize_resource_names: typing.Optional[builtins.bool] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zone: The availability zone to create the instance in.
        :param executor_instance_tag: A label tag to add to all the executors. Can be used for filtering out the right instances in stackdriver monitoring.
        :param executor_metrics_environment_label: The value for environment by which to filter the custom metrics.
        :param executor_queue_name: The queue from which the executor should dequeue jobs.
        :param executor_sourcegraph_executor_proxy_password: The shared password used to authenticate requests to the internal executor proxy.
        :param executor_sourcegraph_external_url: The externally accessible URL of the target Sourcegraph instance.
        :param docker_mirror_boot_disk_size: Docker registry mirror node disk size in GB. Default: 64
        :param docker_mirror_disk_iops: Persistent Docker registry mirror additional IOPS. Default: 3000
        :param docker_mirror_http_access_cidr_range: DEPRECATED. This is not used anymore. Default: 10.0.0.0/16
        :param docker_mirror_machine_ami: AMI for the EC2 instance to use. Must be in the same availability zone. Leave empty to use latest compatible with the Sourcegraph version.
        :param docker_mirror_machine_type: Docker registry mirror node machine type. Default: m5.large
        :param docker_mirror_ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instance is acceptable. Default: 0.0.0.0/0
        :param docker_mirror_static_ip: The IP to statically assign to the instance. Should be internal. Default: 10.0.1.4
        :param executor_boot_disk_iops: Executor node disk additional IOPS. Default: 3000
        :param executor_boot_disk_size: Executor node disk size in GB. Default: 100
        :param executor_docker_auth_config: If provided, this docker auth config file will be used to authorize image pulls. See `Using private registries <https://docs.sourcegraph.com/admin/deploy_executors#using-private-registries>`_ for how to configure.
        :param executor_firecracker_disk_space: The amount of disk space to give to each firecracker VM. Default: 20GB
        :param executor_firecracker_memory: The amount of memory to give to each firecracker VM. Default: 12GB
        :param executor_firecracker_num_cpus: The number of CPUs to give to each firecracker VM. Default: 4
        :param executor_http_access_cidr_range: DEPRECATED. This is not used anymore. Default: 0.0.0.0/0
        :param executor_job_memory: The amount of memory to allocate to each virtual machine or container. Default: 12GB
        :param executor_job_num_cpus: The number of CPUs to allocate to each virtual machine or container. Default: 4
        :param executor_jobs_per_instance_scaling: The amount of jobs a single instance should have in queue. Used for autoscaling. Default: 360
        :param executor_machine_image: Executor node machine disk image to use for creating the boot volume. Leave empty to use latest compatible with the Sourcegraph version.
        :param executor_machine_type: Executor node machine type. Default: c5n.metal
        :param executor_max_active_time: The maximum time that can be spent by the worker dequeueing records to be handled. Default: 2h
        :param executor_maximum_num_jobs: The number of jobs to run concurrently per executor instance. Default: 18
        :param executor_maximum_runtime_per_job: The maximum wall time that can be spent on a single job. Default: 30m
        :param executor_max_replicas: The maximum number of executor instances to run in the autoscaling group. Default: 1
        :param executor_min_replicas: The minimum number of executor instances to run in the autoscaling group. Default: 1
        :param executor_num_total_jobs: The maximum number of jobs that will be dequeued by the worker. Default: 1800
        :param executor_preemptible_machines: Whether to use preemptible machines instead of standard machines; usually way cheaper but might be terminated at any time
        :param executor_resource_prefix: An optional prefix to add to all resources created.
        :param executor_ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instances is acceptable. Default: 0.0.0.0/0
        :param executor_use_firecracker: Whether to isolate commands in virtual machines. Default: true
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param private_networking: If true, the executors and docker mirror will live in a private subnet and communicate with the internet through NAT.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param security_group_id: If provided, the default security groups will not be created. The ID of the security group to associate the Docker Mirror network and the Launch Template network with.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a075a5951b704c69bba53af7ce7ab98e142a2a1c6e5357e051571de83bbb59)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ExecutorsConfig(
            availability_zone=availability_zone,
            executor_instance_tag=executor_instance_tag,
            executor_metrics_environment_label=executor_metrics_environment_label,
            executor_queue_name=executor_queue_name,
            executor_sourcegraph_executor_proxy_password=executor_sourcegraph_executor_proxy_password,
            executor_sourcegraph_external_url=executor_sourcegraph_external_url,
            docker_mirror_boot_disk_size=docker_mirror_boot_disk_size,
            docker_mirror_disk_iops=docker_mirror_disk_iops,
            docker_mirror_http_access_cidr_range=docker_mirror_http_access_cidr_range,
            docker_mirror_machine_ami=docker_mirror_machine_ami,
            docker_mirror_machine_type=docker_mirror_machine_type,
            docker_mirror_ssh_access_cidr_range=docker_mirror_ssh_access_cidr_range,
            docker_mirror_static_ip=docker_mirror_static_ip,
            executor_boot_disk_iops=executor_boot_disk_iops,
            executor_boot_disk_size=executor_boot_disk_size,
            executor_docker_auth_config=executor_docker_auth_config,
            executor_firecracker_disk_space=executor_firecracker_disk_space,
            executor_firecracker_memory=executor_firecracker_memory,
            executor_firecracker_num_cpus=executor_firecracker_num_cpus,
            executor_http_access_cidr_range=executor_http_access_cidr_range,
            executor_job_memory=executor_job_memory,
            executor_job_num_cpus=executor_job_num_cpus,
            executor_jobs_per_instance_scaling=executor_jobs_per_instance_scaling,
            executor_machine_image=executor_machine_image,
            executor_machine_type=executor_machine_type,
            executor_max_active_time=executor_max_active_time,
            executor_maximum_num_jobs=executor_maximum_num_jobs,
            executor_maximum_runtime_per_job=executor_maximum_runtime_per_job,
            executor_max_replicas=executor_max_replicas,
            executor_min_replicas=executor_min_replicas,
            executor_num_total_jobs=executor_num_total_jobs,
            executor_preemptible_machines=executor_preemptible_machines,
            executor_resource_prefix=executor_resource_prefix,
            executor_ssh_access_cidr_range=executor_ssh_access_cidr_range,
            executor_use_firecracker=executor_use_firecracker,
            permissions_boundary_arn=permissions_boundary_arn,
            private_networking=private_networking,
            randomize_resource_names=randomize_resource_names,
            security_group_id=security_group_id,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e346fcb720b4d2cbab55e6505bf26c9dbc7a274acbcc4a9fdb18282d014dda9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="executorInstanceTag")
    def executor_instance_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executorInstanceTag"))

    @executor_instance_tag.setter
    def executor_instance_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f345c5e3b34944c658deda25d81e150e808ba52d1fc5eca0dc1e3aa813862a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorInstanceTag", value)

    @builtins.property
    @jsii.member(jsii_name="executorMetricsEnvironmentLabel")
    def executor_metrics_environment_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executorMetricsEnvironmentLabel"))

    @executor_metrics_environment_label.setter
    def executor_metrics_environment_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa39d6fc8ebaeb76b9eb374cfa831b04dc81884e489b228ec449283c86c16dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMetricsEnvironmentLabel", value)

    @builtins.property
    @jsii.member(jsii_name="executorQueueName")
    def executor_queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executorQueueName"))

    @executor_queue_name.setter
    def executor_queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b0299442afa0bbc89db6b1aff554b1bd925b69b126c028de7d981c2d727118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorQueueName", value)

    @builtins.property
    @jsii.member(jsii_name="executorSourcegraphExecutorProxyPassword")
    def executor_sourcegraph_executor_proxy_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executorSourcegraphExecutorProxyPassword"))

    @executor_sourcegraph_executor_proxy_password.setter
    def executor_sourcegraph_executor_proxy_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902d10907f671a7a898816538f8f9224b756c22dd9f6b1478f3bc9db23318dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorSourcegraphExecutorProxyPassword", value)

    @builtins.property
    @jsii.member(jsii_name="executorSourcegraphExternalUrl")
    def executor_sourcegraph_external_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executorSourcegraphExternalUrl"))

    @executor_sourcegraph_external_url.setter
    def executor_sourcegraph_external_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0469c275627595896e0de24ff55013e7750eb297398857bf52a25cdf73a7701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorSourcegraphExternalUrl", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorBootDiskSize")
    def docker_mirror_boot_disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerMirrorBootDiskSize"))

    @docker_mirror_boot_disk_size.setter
    def docker_mirror_boot_disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d18e38008692b72b4a26ada719a8bcdcf3d3ec1dcfb3ff20a513c1c5b7ca90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorBootDiskSize", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorDiskIops")
    def docker_mirror_disk_iops(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerMirrorDiskIops"))

    @docker_mirror_disk_iops.setter
    def docker_mirror_disk_iops(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ac5e05688e9c26d8dd53082a78ac01853864cdb1a66c8567b86992751b595b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorDiskIops", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorHttpAccessCidrRange")
    def docker_mirror_http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerMirrorHttpAccessCidrRange"))

    @docker_mirror_http_access_cidr_range.setter
    def docker_mirror_http_access_cidr_range(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba81f0b01e77eac389021131622120f81f52ba7f992bb72e96bec6ee3f2234ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorHttpAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorMachineAmi")
    def docker_mirror_machine_ami(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerMirrorMachineAmi"))

    @docker_mirror_machine_ami.setter
    def docker_mirror_machine_ami(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789fdc9200c56687e1ff3f0de9804a803536b1889c9134b908ebbbf03b378dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorMachineAmi", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorMachineType")
    def docker_mirror_machine_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerMirrorMachineType"))

    @docker_mirror_machine_type.setter
    def docker_mirror_machine_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d5ea6662dd70f34a73db068177c553ef49a0cef7ca6c49052e2af5d78d367b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorMachineType", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorSshAccessCidrRange")
    def docker_mirror_ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerMirrorSshAccessCidrRange"))

    @docker_mirror_ssh_access_cidr_range.setter
    def docker_mirror_ssh_access_cidr_range(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a764fcfc6dbf3b7a6fde20d3e07c1706ebbbad7b34b44ed450ed3424059badb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorSshAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorStaticIp")
    def docker_mirror_static_ip(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerMirrorStaticIp"))

    @docker_mirror_static_ip.setter
    def docker_mirror_static_ip(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0cb944d9cecda4af60baa4e9dbc667fb4d41a61c844d9982ca353e07a041f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorStaticIp", value)

    @builtins.property
    @jsii.member(jsii_name="executorBootDiskIops")
    def executor_boot_disk_iops(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorBootDiskIops"))

    @executor_boot_disk_iops.setter
    def executor_boot_disk_iops(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81d0de343857d7049e1f892fca296e7460b95fbb1a04a66f216a6e8a199ae2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorBootDiskIops", value)

    @builtins.property
    @jsii.member(jsii_name="executorBootDiskSize")
    def executor_boot_disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorBootDiskSize"))

    @executor_boot_disk_size.setter
    def executor_boot_disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1c7ab5dbf61e9105d9046935ddb01871152e6a4a975828ea7fd717555a1dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorBootDiskSize", value)

    @builtins.property
    @jsii.member(jsii_name="executorDockerAuthConfig")
    def executor_docker_auth_config(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorDockerAuthConfig"))

    @executor_docker_auth_config.setter
    def executor_docker_auth_config(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06239811f0de6aab9a4dc02de61c19e915a933740fbb5a329e5a16bef3a31344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorDockerAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="executorFirecrackerDiskSpace")
    def executor_firecracker_disk_space(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorFirecrackerDiskSpace"))

    @executor_firecracker_disk_space.setter
    def executor_firecracker_disk_space(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2afca55a57e0bf59cebfd19ac3cdc6bb8e50b76ee2a302c21706f6771f4a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorFirecrackerDiskSpace", value)

    @builtins.property
    @jsii.member(jsii_name="executorFirecrackerMemory")
    def executor_firecracker_memory(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorFirecrackerMemory"))

    @executor_firecracker_memory.setter
    def executor_firecracker_memory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5950db96b73bb18d08bd00b9c5b055411042db4c7c7cfe31425d3915fbf661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorFirecrackerMemory", value)

    @builtins.property
    @jsii.member(jsii_name="executorFirecrackerNumCpus")
    def executor_firecracker_num_cpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorFirecrackerNumCpus"))

    @executor_firecracker_num_cpus.setter
    def executor_firecracker_num_cpus(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56666624923db91f7d3a1915520253c3ea85431564c7cc3857c0e747dafb2af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorFirecrackerNumCpus", value)

    @builtins.property
    @jsii.member(jsii_name="executorHttpAccessCidrRange")
    def executor_http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorHttpAccessCidrRange"))

    @executor_http_access_cidr_range.setter
    def executor_http_access_cidr_range(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53ef0732470c2d6b4217ce2e9f3ff61f49fefa1c7319d0e47d7192a8c85a983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorHttpAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="executorJobMemory")
    def executor_job_memory(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorJobMemory"))

    @executor_job_memory.setter
    def executor_job_memory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115eed0d3fe77c18474fa5832134dd40ea880a9f365beae9500666e7eee4a92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorJobMemory", value)

    @builtins.property
    @jsii.member(jsii_name="executorJobNumCpus")
    def executor_job_num_cpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorJobNumCpus"))

    @executor_job_num_cpus.setter
    def executor_job_num_cpus(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b413a86c6674d68c315bbfe85ea594f9eabb6164770da08b21ecd13180b4a5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorJobNumCpus", value)

    @builtins.property
    @jsii.member(jsii_name="executorJobsPerInstanceScaling")
    def executor_jobs_per_instance_scaling(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorJobsPerInstanceScaling"))

    @executor_jobs_per_instance_scaling.setter
    def executor_jobs_per_instance_scaling(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009b1096fa99026c4a895aae794959168ff4377828d4ce7a7ceebce81d322f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorJobsPerInstanceScaling", value)

    @builtins.property
    @jsii.member(jsii_name="executorMachineImage")
    def executor_machine_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorMachineImage"))

    @executor_machine_image.setter
    def executor_machine_image(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5607fb414140cf5406e44ee4f2af7569d9562fffd86a44e7771cd730df17dfd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMachineImage", value)

    @builtins.property
    @jsii.member(jsii_name="executorMachineType")
    def executor_machine_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorMachineType"))

    @executor_machine_type.setter
    def executor_machine_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2523f1eb19f8170f300fecbbdcd82af604c09be6a89d8959ca951a6d8f6aae3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMachineType", value)

    @builtins.property
    @jsii.member(jsii_name="executorMaxActiveTime")
    def executor_max_active_time(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorMaxActiveTime"))

    @executor_max_active_time.setter
    def executor_max_active_time(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a4bd5f6fff26329689230b3f588bc6abef59865a603796f06af5c5ed9e17c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMaxActiveTime", value)

    @builtins.property
    @jsii.member(jsii_name="executorMaximumNumJobs")
    def executor_maximum_num_jobs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorMaximumNumJobs"))

    @executor_maximum_num_jobs.setter
    def executor_maximum_num_jobs(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b492cfa560e045216a90dcded0c7269d98584a3cd20f01e93b5819189f8f08e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMaximumNumJobs", value)

    @builtins.property
    @jsii.member(jsii_name="executorMaximumRuntimePerJob")
    def executor_maximum_runtime_per_job(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorMaximumRuntimePerJob"))

    @executor_maximum_runtime_per_job.setter
    def executor_maximum_runtime_per_job(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d9dc04753fb2ee8692461444d2091dd80d7f29a2bb2e045b2ed14c75c2dde8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMaximumRuntimePerJob", value)

    @builtins.property
    @jsii.member(jsii_name="executorMaxReplicas")
    def executor_max_replicas(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorMaxReplicas"))

    @executor_max_replicas.setter
    def executor_max_replicas(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553ed49d5edf9f06359ea8797ebc85d06f4787bbf1d49beefa63bc2d107df475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMaxReplicas", value)

    @builtins.property
    @jsii.member(jsii_name="executorMinReplicas")
    def executor_min_replicas(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorMinReplicas"))

    @executor_min_replicas.setter
    def executor_min_replicas(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a124d54ce0d16b08e0f4bc6fc5cbf4665385050c980d2b41a4b2745db6cf5c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorMinReplicas", value)

    @builtins.property
    @jsii.member(jsii_name="executorNumTotalJobs")
    def executor_num_total_jobs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorNumTotalJobs"))

    @executor_num_total_jobs.setter
    def executor_num_total_jobs(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f302eb93eacb0717ab0fa10091b20475cb482bfa0f188abd2f1ceb716a48c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorNumTotalJobs", value)

    @builtins.property
    @jsii.member(jsii_name="executorPreemptibleMachines")
    def executor_preemptible_machines(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "executorPreemptibleMachines"))

    @executor_preemptible_machines.setter
    def executor_preemptible_machines(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e344e81c8f08877019642a0a3aabe520a813c95186b6acf0b0412ed6fa86977a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorPreemptibleMachines", value)

    @builtins.property
    @jsii.member(jsii_name="executorResourcePrefix")
    def executor_resource_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorResourcePrefix"))

    @executor_resource_prefix.setter
    def executor_resource_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34dd09832e6a88c01dc9bbdf6861405332ff491d65aeb197f29b96c0ed3db426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorResourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="executorSshAccessCidrRange")
    def executor_ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executorSshAccessCidrRange"))

    @executor_ssh_access_cidr_range.setter
    def executor_ssh_access_cidr_range(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e155a981cddd4dc7769fd0d7ddf56ceeb69aeb23373427657599721042df73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorSshAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="executorUseFirecracker")
    def executor_use_firecracker(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "executorUseFirecracker"))

    @executor_use_firecracker.setter
    def executor_use_firecracker(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e84e8a2b93b276e49b0fbad85be8cc29b675407c7e1b7f45fea359d2364c5dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorUseFirecracker", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryArn")
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaryArn"))

    @permissions_boundary_arn.setter
    def permissions_boundary_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6e0a4c1188e33e882dd1d5876a7f791fa1b1bbf968142dd5eba0bfcb91d432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaryArn", value)

    @builtins.property
    @jsii.member(jsii_name="privateNetworking")
    def private_networking(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "privateNetworking"))

    @private_networking.setter
    def private_networking(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fca07388510fa77d84c58dda9a01ae5042622f3227fda26ea6fa39d9a72c924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateNetworking", value)

    @builtins.property
    @jsii.member(jsii_name="randomizeResourceNames")
    def randomize_resource_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "randomizeResourceNames"))

    @randomize_resource_names.setter
    def randomize_resource_names(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6794e191e37a371afc93d6a81cf2b2fcddc0e4bae2f342f3d79fb6a6c2aa6c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizeResourceNames", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9156a946246b1dc641924e8c681975d034ae22bc368b185038e71ef52182af42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value)


@jsii.data_type(
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "availability_zone": "availabilityZone",
        "executor_instance_tag": "executorInstanceTag",
        "executor_metrics_environment_label": "executorMetricsEnvironmentLabel",
        "executor_queue_name": "executorQueueName",
        "executor_sourcegraph_executor_proxy_password": "executorSourcegraphExecutorProxyPassword",
        "executor_sourcegraph_external_url": "executorSourcegraphExternalUrl",
        "docker_mirror_boot_disk_size": "dockerMirrorBootDiskSize",
        "docker_mirror_disk_iops": "dockerMirrorDiskIops",
        "docker_mirror_http_access_cidr_range": "dockerMirrorHttpAccessCidrRange",
        "docker_mirror_machine_ami": "dockerMirrorMachineAmi",
        "docker_mirror_machine_type": "dockerMirrorMachineType",
        "docker_mirror_ssh_access_cidr_range": "dockerMirrorSshAccessCidrRange",
        "docker_mirror_static_ip": "dockerMirrorStaticIp",
        "executor_boot_disk_iops": "executorBootDiskIops",
        "executor_boot_disk_size": "executorBootDiskSize",
        "executor_docker_auth_config": "executorDockerAuthConfig",
        "executor_firecracker_disk_space": "executorFirecrackerDiskSpace",
        "executor_firecracker_memory": "executorFirecrackerMemory",
        "executor_firecracker_num_cpus": "executorFirecrackerNumCpus",
        "executor_http_access_cidr_range": "executorHttpAccessCidrRange",
        "executor_job_memory": "executorJobMemory",
        "executor_job_num_cpus": "executorJobNumCpus",
        "executor_jobs_per_instance_scaling": "executorJobsPerInstanceScaling",
        "executor_machine_image": "executorMachineImage",
        "executor_machine_type": "executorMachineType",
        "executor_max_active_time": "executorMaxActiveTime",
        "executor_maximum_num_jobs": "executorMaximumNumJobs",
        "executor_maximum_runtime_per_job": "executorMaximumRuntimePerJob",
        "executor_max_replicas": "executorMaxReplicas",
        "executor_min_replicas": "executorMinReplicas",
        "executor_num_total_jobs": "executorNumTotalJobs",
        "executor_preemptible_machines": "executorPreemptibleMachines",
        "executor_resource_prefix": "executorResourcePrefix",
        "executor_ssh_access_cidr_range": "executorSshAccessCidrRange",
        "executor_use_firecracker": "executorUseFirecracker",
        "permissions_boundary_arn": "permissionsBoundaryArn",
        "private_networking": "privateNetworking",
        "randomize_resource_names": "randomizeResourceNames",
        "security_group_id": "securityGroupId",
    },
)
class ExecutorsConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        availability_zone: builtins.str,
        executor_instance_tag: builtins.str,
        executor_metrics_environment_label: builtins.str,
        executor_queue_name: builtins.str,
        executor_sourcegraph_executor_proxy_password: builtins.str,
        executor_sourcegraph_external_url: builtins.str,
        docker_mirror_boot_disk_size: typing.Optional[jsii.Number] = None,
        docker_mirror_disk_iops: typing.Optional[jsii.Number] = None,
        docker_mirror_http_access_cidr_range: typing.Optional[builtins.str] = None,
        docker_mirror_machine_ami: typing.Optional[builtins.str] = None,
        docker_mirror_machine_type: typing.Optional[builtins.str] = None,
        docker_mirror_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        docker_mirror_static_ip: typing.Optional[builtins.str] = None,
        executor_boot_disk_iops: typing.Optional[jsii.Number] = None,
        executor_boot_disk_size: typing.Optional[jsii.Number] = None,
        executor_docker_auth_config: typing.Optional[builtins.str] = None,
        executor_firecracker_disk_space: typing.Optional[builtins.str] = None,
        executor_firecracker_memory: typing.Optional[builtins.str] = None,
        executor_firecracker_num_cpus: typing.Optional[jsii.Number] = None,
        executor_http_access_cidr_range: typing.Optional[builtins.str] = None,
        executor_job_memory: typing.Optional[builtins.str] = None,
        executor_job_num_cpus: typing.Optional[jsii.Number] = None,
        executor_jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
        executor_machine_image: typing.Optional[builtins.str] = None,
        executor_machine_type: typing.Optional[builtins.str] = None,
        executor_max_active_time: typing.Optional[builtins.str] = None,
        executor_maximum_num_jobs: typing.Optional[jsii.Number] = None,
        executor_maximum_runtime_per_job: typing.Optional[builtins.str] = None,
        executor_max_replicas: typing.Optional[jsii.Number] = None,
        executor_min_replicas: typing.Optional[jsii.Number] = None,
        executor_num_total_jobs: typing.Optional[jsii.Number] = None,
        executor_preemptible_machines: typing.Optional[builtins.bool] = None,
        executor_resource_prefix: typing.Optional[builtins.str] = None,
        executor_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        executor_use_firecracker: typing.Optional[builtins.bool] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        private_networking: typing.Optional[builtins.bool] = None,
        randomize_resource_names: typing.Optional[builtins.bool] = None,
        security_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param availability_zone: The availability zone to create the instance in.
        :param executor_instance_tag: A label tag to add to all the executors. Can be used for filtering out the right instances in stackdriver monitoring.
        :param executor_metrics_environment_label: The value for environment by which to filter the custom metrics.
        :param executor_queue_name: The queue from which the executor should dequeue jobs.
        :param executor_sourcegraph_executor_proxy_password: The shared password used to authenticate requests to the internal executor proxy.
        :param executor_sourcegraph_external_url: The externally accessible URL of the target Sourcegraph instance.
        :param docker_mirror_boot_disk_size: Docker registry mirror node disk size in GB. Default: 64
        :param docker_mirror_disk_iops: Persistent Docker registry mirror additional IOPS. Default: 3000
        :param docker_mirror_http_access_cidr_range: DEPRECATED. This is not used anymore. Default: 10.0.0.0/16
        :param docker_mirror_machine_ami: AMI for the EC2 instance to use. Must be in the same availability zone. Leave empty to use latest compatible with the Sourcegraph version.
        :param docker_mirror_machine_type: Docker registry mirror node machine type. Default: m5.large
        :param docker_mirror_ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instance is acceptable. Default: 0.0.0.0/0
        :param docker_mirror_static_ip: The IP to statically assign to the instance. Should be internal. Default: 10.0.1.4
        :param executor_boot_disk_iops: Executor node disk additional IOPS. Default: 3000
        :param executor_boot_disk_size: Executor node disk size in GB. Default: 100
        :param executor_docker_auth_config: If provided, this docker auth config file will be used to authorize image pulls. See `Using private registries <https://docs.sourcegraph.com/admin/deploy_executors#using-private-registries>`_ for how to configure.
        :param executor_firecracker_disk_space: The amount of disk space to give to each firecracker VM. Default: 20GB
        :param executor_firecracker_memory: The amount of memory to give to each firecracker VM. Default: 12GB
        :param executor_firecracker_num_cpus: The number of CPUs to give to each firecracker VM. Default: 4
        :param executor_http_access_cidr_range: DEPRECATED. This is not used anymore. Default: 0.0.0.0/0
        :param executor_job_memory: The amount of memory to allocate to each virtual machine or container. Default: 12GB
        :param executor_job_num_cpus: The number of CPUs to allocate to each virtual machine or container. Default: 4
        :param executor_jobs_per_instance_scaling: The amount of jobs a single instance should have in queue. Used for autoscaling. Default: 360
        :param executor_machine_image: Executor node machine disk image to use for creating the boot volume. Leave empty to use latest compatible with the Sourcegraph version.
        :param executor_machine_type: Executor node machine type. Default: c5n.metal
        :param executor_max_active_time: The maximum time that can be spent by the worker dequeueing records to be handled. Default: 2h
        :param executor_maximum_num_jobs: The number of jobs to run concurrently per executor instance. Default: 18
        :param executor_maximum_runtime_per_job: The maximum wall time that can be spent on a single job. Default: 30m
        :param executor_max_replicas: The maximum number of executor instances to run in the autoscaling group. Default: 1
        :param executor_min_replicas: The minimum number of executor instances to run in the autoscaling group. Default: 1
        :param executor_num_total_jobs: The maximum number of jobs that will be dequeued by the worker. Default: 1800
        :param executor_preemptible_machines: Whether to use preemptible machines instead of standard machines; usually way cheaper but might be terminated at any time
        :param executor_resource_prefix: An optional prefix to add to all resources created.
        :param executor_ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instances is acceptable. Default: 0.0.0.0/0
        :param executor_use_firecracker: Whether to isolate commands in virtual machines. Default: true
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param private_networking: If true, the executors and docker mirror will live in a private subnet and communicate with the internet through NAT.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param security_group_id: If provided, the default security groups will not be created. The ID of the security group to associate the Docker Mirror network and the Launch Template network with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0003d9f354d4ab227ea287273cd989f9aa2fdef0039d070212a0a7db2efe8f77)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument executor_instance_tag", value=executor_instance_tag, expected_type=type_hints["executor_instance_tag"])
            check_type(argname="argument executor_metrics_environment_label", value=executor_metrics_environment_label, expected_type=type_hints["executor_metrics_environment_label"])
            check_type(argname="argument executor_queue_name", value=executor_queue_name, expected_type=type_hints["executor_queue_name"])
            check_type(argname="argument executor_sourcegraph_executor_proxy_password", value=executor_sourcegraph_executor_proxy_password, expected_type=type_hints["executor_sourcegraph_executor_proxy_password"])
            check_type(argname="argument executor_sourcegraph_external_url", value=executor_sourcegraph_external_url, expected_type=type_hints["executor_sourcegraph_external_url"])
            check_type(argname="argument docker_mirror_boot_disk_size", value=docker_mirror_boot_disk_size, expected_type=type_hints["docker_mirror_boot_disk_size"])
            check_type(argname="argument docker_mirror_disk_iops", value=docker_mirror_disk_iops, expected_type=type_hints["docker_mirror_disk_iops"])
            check_type(argname="argument docker_mirror_http_access_cidr_range", value=docker_mirror_http_access_cidr_range, expected_type=type_hints["docker_mirror_http_access_cidr_range"])
            check_type(argname="argument docker_mirror_machine_ami", value=docker_mirror_machine_ami, expected_type=type_hints["docker_mirror_machine_ami"])
            check_type(argname="argument docker_mirror_machine_type", value=docker_mirror_machine_type, expected_type=type_hints["docker_mirror_machine_type"])
            check_type(argname="argument docker_mirror_ssh_access_cidr_range", value=docker_mirror_ssh_access_cidr_range, expected_type=type_hints["docker_mirror_ssh_access_cidr_range"])
            check_type(argname="argument docker_mirror_static_ip", value=docker_mirror_static_ip, expected_type=type_hints["docker_mirror_static_ip"])
            check_type(argname="argument executor_boot_disk_iops", value=executor_boot_disk_iops, expected_type=type_hints["executor_boot_disk_iops"])
            check_type(argname="argument executor_boot_disk_size", value=executor_boot_disk_size, expected_type=type_hints["executor_boot_disk_size"])
            check_type(argname="argument executor_docker_auth_config", value=executor_docker_auth_config, expected_type=type_hints["executor_docker_auth_config"])
            check_type(argname="argument executor_firecracker_disk_space", value=executor_firecracker_disk_space, expected_type=type_hints["executor_firecracker_disk_space"])
            check_type(argname="argument executor_firecracker_memory", value=executor_firecracker_memory, expected_type=type_hints["executor_firecracker_memory"])
            check_type(argname="argument executor_firecracker_num_cpus", value=executor_firecracker_num_cpus, expected_type=type_hints["executor_firecracker_num_cpus"])
            check_type(argname="argument executor_http_access_cidr_range", value=executor_http_access_cidr_range, expected_type=type_hints["executor_http_access_cidr_range"])
            check_type(argname="argument executor_job_memory", value=executor_job_memory, expected_type=type_hints["executor_job_memory"])
            check_type(argname="argument executor_job_num_cpus", value=executor_job_num_cpus, expected_type=type_hints["executor_job_num_cpus"])
            check_type(argname="argument executor_jobs_per_instance_scaling", value=executor_jobs_per_instance_scaling, expected_type=type_hints["executor_jobs_per_instance_scaling"])
            check_type(argname="argument executor_machine_image", value=executor_machine_image, expected_type=type_hints["executor_machine_image"])
            check_type(argname="argument executor_machine_type", value=executor_machine_type, expected_type=type_hints["executor_machine_type"])
            check_type(argname="argument executor_max_active_time", value=executor_max_active_time, expected_type=type_hints["executor_max_active_time"])
            check_type(argname="argument executor_maximum_num_jobs", value=executor_maximum_num_jobs, expected_type=type_hints["executor_maximum_num_jobs"])
            check_type(argname="argument executor_maximum_runtime_per_job", value=executor_maximum_runtime_per_job, expected_type=type_hints["executor_maximum_runtime_per_job"])
            check_type(argname="argument executor_max_replicas", value=executor_max_replicas, expected_type=type_hints["executor_max_replicas"])
            check_type(argname="argument executor_min_replicas", value=executor_min_replicas, expected_type=type_hints["executor_min_replicas"])
            check_type(argname="argument executor_num_total_jobs", value=executor_num_total_jobs, expected_type=type_hints["executor_num_total_jobs"])
            check_type(argname="argument executor_preemptible_machines", value=executor_preemptible_machines, expected_type=type_hints["executor_preemptible_machines"])
            check_type(argname="argument executor_resource_prefix", value=executor_resource_prefix, expected_type=type_hints["executor_resource_prefix"])
            check_type(argname="argument executor_ssh_access_cidr_range", value=executor_ssh_access_cidr_range, expected_type=type_hints["executor_ssh_access_cidr_range"])
            check_type(argname="argument executor_use_firecracker", value=executor_use_firecracker, expected_type=type_hints["executor_use_firecracker"])
            check_type(argname="argument permissions_boundary_arn", value=permissions_boundary_arn, expected_type=type_hints["permissions_boundary_arn"])
            check_type(argname="argument private_networking", value=private_networking, expected_type=type_hints["private_networking"])
            check_type(argname="argument randomize_resource_names", value=randomize_resource_names, expected_type=type_hints["randomize_resource_names"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "executor_instance_tag": executor_instance_tag,
            "executor_metrics_environment_label": executor_metrics_environment_label,
            "executor_queue_name": executor_queue_name,
            "executor_sourcegraph_executor_proxy_password": executor_sourcegraph_executor_proxy_password,
            "executor_sourcegraph_external_url": executor_sourcegraph_external_url,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if docker_mirror_boot_disk_size is not None:
            self._values["docker_mirror_boot_disk_size"] = docker_mirror_boot_disk_size
        if docker_mirror_disk_iops is not None:
            self._values["docker_mirror_disk_iops"] = docker_mirror_disk_iops
        if docker_mirror_http_access_cidr_range is not None:
            self._values["docker_mirror_http_access_cidr_range"] = docker_mirror_http_access_cidr_range
        if docker_mirror_machine_ami is not None:
            self._values["docker_mirror_machine_ami"] = docker_mirror_machine_ami
        if docker_mirror_machine_type is not None:
            self._values["docker_mirror_machine_type"] = docker_mirror_machine_type
        if docker_mirror_ssh_access_cidr_range is not None:
            self._values["docker_mirror_ssh_access_cidr_range"] = docker_mirror_ssh_access_cidr_range
        if docker_mirror_static_ip is not None:
            self._values["docker_mirror_static_ip"] = docker_mirror_static_ip
        if executor_boot_disk_iops is not None:
            self._values["executor_boot_disk_iops"] = executor_boot_disk_iops
        if executor_boot_disk_size is not None:
            self._values["executor_boot_disk_size"] = executor_boot_disk_size
        if executor_docker_auth_config is not None:
            self._values["executor_docker_auth_config"] = executor_docker_auth_config
        if executor_firecracker_disk_space is not None:
            self._values["executor_firecracker_disk_space"] = executor_firecracker_disk_space
        if executor_firecracker_memory is not None:
            self._values["executor_firecracker_memory"] = executor_firecracker_memory
        if executor_firecracker_num_cpus is not None:
            self._values["executor_firecracker_num_cpus"] = executor_firecracker_num_cpus
        if executor_http_access_cidr_range is not None:
            self._values["executor_http_access_cidr_range"] = executor_http_access_cidr_range
        if executor_job_memory is not None:
            self._values["executor_job_memory"] = executor_job_memory
        if executor_job_num_cpus is not None:
            self._values["executor_job_num_cpus"] = executor_job_num_cpus
        if executor_jobs_per_instance_scaling is not None:
            self._values["executor_jobs_per_instance_scaling"] = executor_jobs_per_instance_scaling
        if executor_machine_image is not None:
            self._values["executor_machine_image"] = executor_machine_image
        if executor_machine_type is not None:
            self._values["executor_machine_type"] = executor_machine_type
        if executor_max_active_time is not None:
            self._values["executor_max_active_time"] = executor_max_active_time
        if executor_maximum_num_jobs is not None:
            self._values["executor_maximum_num_jobs"] = executor_maximum_num_jobs
        if executor_maximum_runtime_per_job is not None:
            self._values["executor_maximum_runtime_per_job"] = executor_maximum_runtime_per_job
        if executor_max_replicas is not None:
            self._values["executor_max_replicas"] = executor_max_replicas
        if executor_min_replicas is not None:
            self._values["executor_min_replicas"] = executor_min_replicas
        if executor_num_total_jobs is not None:
            self._values["executor_num_total_jobs"] = executor_num_total_jobs
        if executor_preemptible_machines is not None:
            self._values["executor_preemptible_machines"] = executor_preemptible_machines
        if executor_resource_prefix is not None:
            self._values["executor_resource_prefix"] = executor_resource_prefix
        if executor_ssh_access_cidr_range is not None:
            self._values["executor_ssh_access_cidr_range"] = executor_ssh_access_cidr_range
        if executor_use_firecracker is not None:
            self._values["executor_use_firecracker"] = executor_use_firecracker
        if permissions_boundary_arn is not None:
            self._values["permissions_boundary_arn"] = permissions_boundary_arn
        if private_networking is not None:
            self._values["private_networking"] = private_networking
        if randomize_resource_names is not None:
            self._values["randomize_resource_names"] = randomize_resource_names
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_zone(self) -> builtins.str:
        '''The availability zone to create the instance in.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def executor_instance_tag(self) -> builtins.str:
        '''A label tag to add to all the executors.

        Can be used for filtering out the right instances in stackdriver monitoring.
        '''
        result = self._values.get("executor_instance_tag")
        assert result is not None, "Required property 'executor_instance_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def executor_metrics_environment_label(self) -> builtins.str:
        '''The value for environment by which to filter the custom metrics.'''
        result = self._values.get("executor_metrics_environment_label")
        assert result is not None, "Required property 'executor_metrics_environment_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def executor_queue_name(self) -> builtins.str:
        '''The queue from which the executor should dequeue jobs.'''
        result = self._values.get("executor_queue_name")
        assert result is not None, "Required property 'executor_queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def executor_sourcegraph_executor_proxy_password(self) -> builtins.str:
        '''The shared password used to authenticate requests to the internal executor proxy.'''
        result = self._values.get("executor_sourcegraph_executor_proxy_password")
        assert result is not None, "Required property 'executor_sourcegraph_executor_proxy_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def executor_sourcegraph_external_url(self) -> builtins.str:
        '''The externally accessible URL of the target Sourcegraph instance.'''
        result = self._values.get("executor_sourcegraph_external_url")
        assert result is not None, "Required property 'executor_sourcegraph_external_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def docker_mirror_boot_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Docker registry mirror node disk size in GB.

        :default: 64
        '''
        result = self._values.get("docker_mirror_boot_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_mirror_disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Persistent Docker registry mirror additional IOPS.

        :default: 3000
        '''
        result = self._values.get("docker_mirror_disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_mirror_http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''DEPRECATED.

        This is not used anymore.

        :default: 10.0.0.0/16
        '''
        result = self._values.get("docker_mirror_http_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_mirror_machine_ami(self) -> typing.Optional[builtins.str]:
        '''AMI for the EC2 instance to use.

        Must be in the same availability zone. Leave empty to use latest compatible with the Sourcegraph version.
        '''
        result = self._values.get("docker_mirror_machine_ami")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_mirror_machine_type(self) -> typing.Optional[builtins.str]:
        '''Docker registry mirror node machine type.

        :default: m5.large
        '''
        result = self._values.get("docker_mirror_machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_mirror_ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range from where SSH access to the EC2 instance is acceptable.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("docker_mirror_ssh_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_mirror_static_ip(self) -> typing.Optional[builtins.str]:
        '''The IP to statically assign to the instance.

        Should be internal.

        :default: 10.0.1.4
        '''
        result = self._values.get("docker_mirror_static_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_boot_disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Executor node disk additional IOPS.

        :default: 3000
        '''
        result = self._values.get("executor_boot_disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_boot_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Executor node disk size in GB.

        :default: 100
        '''
        result = self._values.get("executor_boot_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_docker_auth_config(self) -> typing.Optional[builtins.str]:
        '''If provided, this docker auth config file will be used to authorize image pulls.

        See `Using private registries <https://docs.sourcegraph.com/admin/deploy_executors#using-private-registries>`_ for how to configure.
        '''
        result = self._values.get("executor_docker_auth_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_firecracker_disk_space(self) -> typing.Optional[builtins.str]:
        '''The amount of disk space to give to each firecracker VM.

        :default: 20GB
        '''
        result = self._values.get("executor_firecracker_disk_space")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_firecracker_memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory to give to each firecracker VM.

        :default: 12GB
        '''
        result = self._values.get("executor_firecracker_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_firecracker_num_cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs to give to each firecracker VM.

        :default: 4
        '''
        result = self._values.get("executor_firecracker_num_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''DEPRECATED.

        This is not used anymore.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("executor_http_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_job_memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory to allocate to each virtual machine or container.

        :default: 12GB
        '''
        result = self._values.get("executor_job_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_job_num_cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs to allocate to each virtual machine or container.

        :default: 4
        '''
        result = self._values.get("executor_job_num_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_jobs_per_instance_scaling(self) -> typing.Optional[jsii.Number]:
        '''The amount of jobs a single instance should have in queue.

        Used for autoscaling.

        :default: 360
        '''
        result = self._values.get("executor_jobs_per_instance_scaling")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_machine_image(self) -> typing.Optional[builtins.str]:
        '''Executor node machine disk image to use for creating the boot volume.

        Leave empty to use latest compatible with the Sourcegraph version.
        '''
        result = self._values.get("executor_machine_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_machine_type(self) -> typing.Optional[builtins.str]:
        '''Executor node machine type.

        :default: c5n.metal
        '''
        result = self._values.get("executor_machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_max_active_time(self) -> typing.Optional[builtins.str]:
        '''The maximum time that can be spent by the worker dequeueing records to be handled.

        :default: 2h
        '''
        result = self._values.get("executor_max_active_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_maximum_num_jobs(self) -> typing.Optional[jsii.Number]:
        '''The number of jobs to run concurrently per executor instance.

        :default: 18
        '''
        result = self._values.get("executor_maximum_num_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_maximum_runtime_per_job(self) -> typing.Optional[builtins.str]:
        '''The maximum wall time that can be spent on a single job.

        :default: 30m
        '''
        result = self._values.get("executor_maximum_runtime_per_job")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_max_replicas(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of executor instances to run in the autoscaling group.

        :default: 1
        '''
        result = self._values.get("executor_max_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_min_replicas(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of executor instances to run in the autoscaling group.

        :default: 1
        '''
        result = self._values.get("executor_min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_num_total_jobs(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of jobs that will be dequeued by the worker.

        :default: 1800
        '''
        result = self._values.get("executor_num_total_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def executor_preemptible_machines(self) -> typing.Optional[builtins.bool]:
        '''Whether to use preemptible machines instead of standard machines;

        usually way cheaper but might be terminated at any time
        '''
        result = self._values.get("executor_preemptible_machines")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executor_resource_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix to add to all resources created.'''
        result = self._values.get("executor_resource_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range from where SSH access to the EC2 instances is acceptable.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("executor_ssh_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor_use_firecracker(self) -> typing.Optional[builtins.bool]:
        '''Whether to isolate commands in virtual machines.

        :default: true
        '''
        result = self._values.get("executor_use_firecracker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        '''If not provided, there will be no permissions boundary on IAM roles and users created.

        The ARN of a policy to use for permissions boundaries with IAM roles and users.
        '''
        result = self._values.get("permissions_boundary_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_networking(self) -> typing.Optional[builtins.bool]:
        '''If true, the executors and docker mirror will live in a private subnet and communicate with the internet through NAT.'''
        result = self._values.get("private_networking")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def randomize_resource_names(self) -> typing.Optional[builtins.bool]:
        '''Use randomized names for resources.

        Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        '''
        result = self._values.get("randomize_resource_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''If provided, the default security groups will not be created.

        The ID of the security group to associate the Docker Mirror network and the Launch Template network with.
        '''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecutorsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExecutorsCredentials(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsCredentials",
):
    '''Defines an ExecutorsCredentials based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/sourcegraph/executors/aws/~> 5.0.1/submodules/credentials sourcegraph/executors/aws//modules/credentials}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param resource_prefix: An optional prefix to add to all resources created.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362a212560d933b8b9c2af0b2d250e58de53b6a1805967672f6fead07af410b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ExecutorsCredentialsConfig(
            permissions_boundary_arn=permissions_boundary_arn,
            resource_prefix=resource_prefix,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="metricWriterAccessKeyIdOutput")
    def metric_writer_access_key_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricWriterAccessKeyIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="metricWriterSecretKeyOutput")
    def metric_writer_secret_key_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricWriterSecretKeyOutput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryArn")
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaryArn"))

    @permissions_boundary_arn.setter
    def permissions_boundary_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42e7ffc155edb6b789fadb6dc7f4849e83fb767bce42009eef3a6ccebd69690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaryArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f16c54c9ac1dc6a26d567dc0ba25de6a2922c5c3cd669d4a50acf193c029e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)


@jsii.data_type(
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsCredentialsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "permissions_boundary_arn": "permissionsBoundaryArn",
        "resource_prefix": "resourcePrefix",
    },
)
class ExecutorsCredentialsConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param resource_prefix: An optional prefix to add to all resources created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3301cc66fac69c9e930365be1592d9bf64fd8e65ad62ab2441369089855fbbf9)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument permissions_boundary_arn", value=permissions_boundary_arn, expected_type=type_hints["permissions_boundary_arn"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if permissions_boundary_arn is not None:
            self._values["permissions_boundary_arn"] = permissions_boundary_arn
        if resource_prefix is not None:
            self._values["resource_prefix"] = resource_prefix

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        '''If not provided, there will be no permissions boundary on IAM roles and users created.

        The ARN of a policy to use for permissions boundaries with IAM roles and users.
        '''
        result = self._values.get("permissions_boundary_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix to add to all resources created.'''
        result = self._values.get("resource_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecutorsCredentialsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExecutorsDockerMirror(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsDockerMirror",
):
    '''Defines an ExecutorsDockerMirror based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/sourcegraph/executors/aws/~> 5.0.1/submodules/docker-mirror sourcegraph/executors/aws//modules/docker-mirror}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_tag_prefix: builtins.str,
        randomize_resource_names: builtins.bool,
        static_ip: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        disk_iops: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_throughput: typing.Optional[jsii.Number] = None,
        docker_mirror_access_security_group_id: typing.Optional[builtins.str] = None,
        http_access_cidr_range: typing.Optional[builtins.str] = None,
        http_metrics_access_cidr_range: typing.Optional[builtins.str] = None,
        machine_ami: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_tag_prefix: A label tag to add to all the machines; can be used for filtering out the right instances in stackdriver monitoring and in Prometheus instance discovery.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param static_ip: The IP to statically assign to the instance. Should be internal.
        :param subnet_id: The ID of the subnet within the given VPC to run the instance in.
        :param vpc_id: The ID of the VPC to run the instance in.
        :param assign_public_ip: If false, no public IP will be associated with the executors. Default: true
        :param boot_disk_size: Docker registry mirror node disk size in GB. Default: 32
        :param disk_iops: Persistent Docker registry mirror additional IOPS. Default: 3000
        :param disk_size: Persistent Docker registry mirror disk size in GB. Default: 64
        :param disk_throughput: Persistent Docker registry mirror disk throughput in MiB/s. Default: 125
        :param docker_mirror_access_security_group_id: If provided, the default security groups will not be created. The ID of the security group to associate the Docker Mirror network with.
        :param http_access_cidr_range: CIDR range from where HTTP access to the Docker registry is acceptable. Default: 10.0.0.0/16
        :param http_metrics_access_cidr_range: DEPRECATED: This is not used anymore. Default: 0.0.0.0/0
        :param machine_ami: AMI for the EC2 instance to use. Must be in the same availability zone. Leave empty to use latest compatible with the Sourcegraph version.
        :param machine_type: Docker registry mirror node machine type. Default: m5n.large
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param resource_prefix: An optional prefix to add to all resources created.
        :param ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instance is acceptable. Default: 10.0.0.0/16
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288d8682c0e6c3527731298cff85996a01af1f42519ecdb6061448ef0cd7a60e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ExecutorsDockerMirrorConfig(
            instance_tag_prefix=instance_tag_prefix,
            randomize_resource_names=randomize_resource_names,
            static_ip=static_ip,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            assign_public_ip=assign_public_ip,
            boot_disk_size=boot_disk_size,
            disk_iops=disk_iops,
            disk_size=disk_size,
            disk_throughput=disk_throughput,
            docker_mirror_access_security_group_id=docker_mirror_access_security_group_id,
            http_access_cidr_range=http_access_cidr_range,
            http_metrics_access_cidr_range=http_metrics_access_cidr_range,
            machine_ami=machine_ami,
            machine_type=machine_type,
            permissions_boundary_arn=permissions_boundary_arn,
            resource_prefix=resource_prefix,
            ssh_access_cidr_range=ssh_access_cidr_range,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTagPrefix")
    def instance_tag_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTagPrefix"))

    @instance_tag_prefix.setter
    def instance_tag_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32596c42f48278a8dac1734ba9974e4b7a23fc22f56bd7b7b47d11becafb7f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTagPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="randomizeResourceNames")
    def randomize_resource_names(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "randomizeResourceNames"))

    @randomize_resource_names.setter
    def randomize_resource_names(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b466df1b6635d614615409d1624da6753a43103294a61a9fea1f757e95d5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizeResourceNames", value)

    @builtins.property
    @jsii.member(jsii_name="staticIp")
    def static_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staticIp"))

    @static_ip.setter
    def static_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffd522a4ea3949942c09ab68342711b11abb207d7558935cfeb51788766a11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticIp", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fcd07c0d49535b1ebddaf5b0506f01572469f26a0aeb507c78f3c63c7a5d08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885894d7585064fae864e24aa72829a0fcebf6d204fa819ec34a1b8603e21301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "assignPublicIp"))

    @assign_public_ip.setter
    def assign_public_ip(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93f0196a55e002f3ce21f10ec1ee5ca433acb13b99f66db8ff9edbd48d64ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskSize")
    def boot_disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSize"))

    @boot_disk_size.setter
    def boot_disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879fec2bbf68095ad74b69d46edd5198b2c04416c67af365a3a6c1ea8e2875ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSize", value)

    @builtins.property
    @jsii.member(jsii_name="diskIops")
    def disk_iops(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskIops"))

    @disk_iops.setter
    def disk_iops(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2029f86f845d28012d80b512e23a8d6771d36ea8a381a901eefd617edd686a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskIops", value)

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSize"))

    @disk_size.setter
    def disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700be7fb57f1c58f5ecf419f84bb6fe1131d07a6ee660e84b7484cb5e34e1e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSize", value)

    @builtins.property
    @jsii.member(jsii_name="diskThroughput")
    def disk_throughput(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskThroughput"))

    @disk_throughput.setter
    def disk_throughput(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804759b98b7f064f2a8b5a9b092e702633f0ba9799d36915b4bdc942657f377a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskThroughput", value)

    @builtins.property
    @jsii.member(jsii_name="dockerMirrorAccessSecurityGroupId")
    def docker_mirror_access_security_group_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerMirrorAccessSecurityGroupId"))

    @docker_mirror_access_security_group_id.setter
    def docker_mirror_access_security_group_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97609b51937f49a83fc60de7a8a380b4ff7aa94b8f565f846a2ea7c0ef47c8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerMirrorAccessSecurityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="httpAccessCidrRange")
    def http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpAccessCidrRange"))

    @http_access_cidr_range.setter
    def http_access_cidr_range(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e1ac6d4fdc93edc4cec45d466524a85970cf5a73a6266002e4baca4af65c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="httpMetricsAccessCidrRange")
    def http_metrics_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMetricsAccessCidrRange"))

    @http_metrics_access_cidr_range.setter
    def http_metrics_access_cidr_range(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d50c035ee8bf1d722c32d4668333926e021cb5fa33a4fed74719b30c8ef9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMetricsAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="machineAmi")
    def machine_ami(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineAmi"))

    @machine_ami.setter
    def machine_ami(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536451cdbb7949281a5b22d24e2166f64f727bcb2f43da470d612ec371827a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineAmi", value)

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d803c51ec1f321c45123fe325d4a45f008ced6aed2f972303e2d403c3c9509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryArn")
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaryArn"))

    @permissions_boundary_arn.setter
    def permissions_boundary_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2683020821e46c7166679d48636b0865c428de14e08f01efe772be10aba501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaryArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013618a1baa01c1e1cd58161e1e9e6e8c478913f1c8b60a8274a0dea85110c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="sshAccessCidrRange")
    def ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshAccessCidrRange"))

    @ssh_access_cidr_range.setter
    def ssh_access_cidr_range(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656d02802e2e69b6f178e9a6d42931bb3781262fa74ecd4db9cecb0742f1ce7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshAccessCidrRange", value)


@jsii.data_type(
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsDockerMirrorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "instance_tag_prefix": "instanceTagPrefix",
        "randomize_resource_names": "randomizeResourceNames",
        "static_ip": "staticIp",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "assign_public_ip": "assignPublicIp",
        "boot_disk_size": "bootDiskSize",
        "disk_iops": "diskIops",
        "disk_size": "diskSize",
        "disk_throughput": "diskThroughput",
        "docker_mirror_access_security_group_id": "dockerMirrorAccessSecurityGroupId",
        "http_access_cidr_range": "httpAccessCidrRange",
        "http_metrics_access_cidr_range": "httpMetricsAccessCidrRange",
        "machine_ami": "machineAmi",
        "machine_type": "machineType",
        "permissions_boundary_arn": "permissionsBoundaryArn",
        "resource_prefix": "resourcePrefix",
        "ssh_access_cidr_range": "sshAccessCidrRange",
    },
)
class ExecutorsDockerMirrorConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        instance_tag_prefix: builtins.str,
        randomize_resource_names: builtins.bool,
        static_ip: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        disk_iops: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_throughput: typing.Optional[jsii.Number] = None,
        docker_mirror_access_security_group_id: typing.Optional[builtins.str] = None,
        http_access_cidr_range: typing.Optional[builtins.str] = None,
        http_metrics_access_cidr_range: typing.Optional[builtins.str] = None,
        machine_ami: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param instance_tag_prefix: A label tag to add to all the machines; can be used for filtering out the right instances in stackdriver monitoring and in Prometheus instance discovery.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param static_ip: The IP to statically assign to the instance. Should be internal.
        :param subnet_id: The ID of the subnet within the given VPC to run the instance in.
        :param vpc_id: The ID of the VPC to run the instance in.
        :param assign_public_ip: If false, no public IP will be associated with the executors. Default: true
        :param boot_disk_size: Docker registry mirror node disk size in GB. Default: 32
        :param disk_iops: Persistent Docker registry mirror additional IOPS. Default: 3000
        :param disk_size: Persistent Docker registry mirror disk size in GB. Default: 64
        :param disk_throughput: Persistent Docker registry mirror disk throughput in MiB/s. Default: 125
        :param docker_mirror_access_security_group_id: If provided, the default security groups will not be created. The ID of the security group to associate the Docker Mirror network with.
        :param http_access_cidr_range: CIDR range from where HTTP access to the Docker registry is acceptable. Default: 10.0.0.0/16
        :param http_metrics_access_cidr_range: DEPRECATED: This is not used anymore. Default: 0.0.0.0/0
        :param machine_ami: AMI for the EC2 instance to use. Must be in the same availability zone. Leave empty to use latest compatible with the Sourcegraph version.
        :param machine_type: Docker registry mirror node machine type. Default: m5n.large
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param resource_prefix: An optional prefix to add to all resources created.
        :param ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instance is acceptable. Default: 10.0.0.0/16
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eede05f92bb53955976dcf73b08229654e39bfeaecf513d086087ced2bd17c91)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument instance_tag_prefix", value=instance_tag_prefix, expected_type=type_hints["instance_tag_prefix"])
            check_type(argname="argument randomize_resource_names", value=randomize_resource_names, expected_type=type_hints["randomize_resource_names"])
            check_type(argname="argument static_ip", value=static_ip, expected_type=type_hints["static_ip"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument boot_disk_size", value=boot_disk_size, expected_type=type_hints["boot_disk_size"])
            check_type(argname="argument disk_iops", value=disk_iops, expected_type=type_hints["disk_iops"])
            check_type(argname="argument disk_size", value=disk_size, expected_type=type_hints["disk_size"])
            check_type(argname="argument disk_throughput", value=disk_throughput, expected_type=type_hints["disk_throughput"])
            check_type(argname="argument docker_mirror_access_security_group_id", value=docker_mirror_access_security_group_id, expected_type=type_hints["docker_mirror_access_security_group_id"])
            check_type(argname="argument http_access_cidr_range", value=http_access_cidr_range, expected_type=type_hints["http_access_cidr_range"])
            check_type(argname="argument http_metrics_access_cidr_range", value=http_metrics_access_cidr_range, expected_type=type_hints["http_metrics_access_cidr_range"])
            check_type(argname="argument machine_ami", value=machine_ami, expected_type=type_hints["machine_ami"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument permissions_boundary_arn", value=permissions_boundary_arn, expected_type=type_hints["permissions_boundary_arn"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument ssh_access_cidr_range", value=ssh_access_cidr_range, expected_type=type_hints["ssh_access_cidr_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_tag_prefix": instance_tag_prefix,
            "randomize_resource_names": randomize_resource_names,
            "static_ip": static_ip,
            "subnet_id": subnet_id,
            "vpc_id": vpc_id,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if boot_disk_size is not None:
            self._values["boot_disk_size"] = boot_disk_size
        if disk_iops is not None:
            self._values["disk_iops"] = disk_iops
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if disk_throughput is not None:
            self._values["disk_throughput"] = disk_throughput
        if docker_mirror_access_security_group_id is not None:
            self._values["docker_mirror_access_security_group_id"] = docker_mirror_access_security_group_id
        if http_access_cidr_range is not None:
            self._values["http_access_cidr_range"] = http_access_cidr_range
        if http_metrics_access_cidr_range is not None:
            self._values["http_metrics_access_cidr_range"] = http_metrics_access_cidr_range
        if machine_ami is not None:
            self._values["machine_ami"] = machine_ami
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if permissions_boundary_arn is not None:
            self._values["permissions_boundary_arn"] = permissions_boundary_arn
        if resource_prefix is not None:
            self._values["resource_prefix"] = resource_prefix
        if ssh_access_cidr_range is not None:
            self._values["ssh_access_cidr_range"] = ssh_access_cidr_range

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_tag_prefix(self) -> builtins.str:
        '''A label tag to add to all the machines;

        can be used for filtering out the right instances in stackdriver monitoring and in Prometheus instance discovery.
        '''
        result = self._values.get("instance_tag_prefix")
        assert result is not None, "Required property 'instance_tag_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def randomize_resource_names(self) -> builtins.bool:
        '''Use randomized names for resources.

        Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        '''
        result = self._values.get("randomize_resource_names")
        assert result is not None, "Required property 'randomize_resource_names' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def static_ip(self) -> builtins.str:
        '''The IP to statically assign to the instance.

        Should be internal.
        '''
        result = self._values.get("static_ip")
        assert result is not None, "Required property 'static_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ID of the subnet within the given VPC to run the instance in.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The ID of the VPC to run the instance in.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''If false, no public IP will be associated with the executors.

        :default: true
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def boot_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Docker registry mirror node disk size in GB.

        :default: 32
        '''
        result = self._values.get("boot_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Persistent Docker registry mirror additional IOPS.

        :default: 3000
        '''
        result = self._values.get("disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        '''Persistent Docker registry mirror disk size in GB.

        :default: 64
        '''
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_throughput(self) -> typing.Optional[jsii.Number]:
        '''Persistent Docker registry mirror disk throughput in MiB/s.

        :default: 125
        '''
        result = self._values.get("disk_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_mirror_access_security_group_id(self) -> typing.Optional[builtins.str]:
        '''If provided, the default security groups will not be created.

        The ID of the security group to associate the Docker Mirror network with.
        '''
        result = self._values.get("docker_mirror_access_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range from where HTTP access to the Docker registry is acceptable.

        :default: 10.0.0.0/16
        '''
        result = self._values.get("http_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_metrics_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''DEPRECATED: This is not used anymore.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("http_metrics_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_ami(self) -> typing.Optional[builtins.str]:
        '''AMI for the EC2 instance to use.

        Must be in the same availability zone. Leave empty to use latest compatible with the Sourcegraph version.
        '''
        result = self._values.get("machine_ami")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Docker registry mirror node machine type.

        :default: m5n.large
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        '''If not provided, there will be no permissions boundary on IAM roles and users created.

        The ARN of a policy to use for permissions boundaries with IAM roles and users.
        '''
        result = self._values.get("permissions_boundary_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix to add to all resources created.'''
        result = self._values.get("resource_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range from where SSH access to the EC2 instance is acceptable.

        :default: 10.0.0.0/16
        '''
        result = self._values.get("ssh_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecutorsDockerMirrorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExecutorsExecutors(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsExecutors",
):
    '''Defines an ExecutorsExecutors based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/sourcegraph/executors/aws/~> 5.0.1/submodules/executors sourcegraph/executors/aws//modules/executors}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_tag: builtins.str,
        metrics_environment_label: builtins.str,
        queue_name: builtins.str,
        randomize_resource_names: builtins.bool,
        sourcegraph_executor_proxy_password: builtins.str,
        sourcegraph_external_url: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        boot_disk_iops: typing.Optional[jsii.Number] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        boot_disk_throughput: typing.Optional[jsii.Number] = None,
        docker_auth_config: typing.Optional[builtins.str] = None,
        docker_registry_mirror: typing.Optional[builtins.str] = None,
        docker_registry_mirror_node_exporter_url: typing.Optional[builtins.str] = None,
        firecracker_disk_space: typing.Optional[builtins.str] = None,
        firecracker_memory: typing.Optional[builtins.str] = None,
        firecracker_num_cpus: typing.Optional[jsii.Number] = None,
        http_access_cidr_range: typing.Optional[builtins.str] = None,
        job_memory: typing.Optional[builtins.str] = None,
        job_num_cpus: typing.Optional[jsii.Number] = None,
        jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
        machine_image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_active_time: typing.Optional[builtins.str] = None,
        maximum_num_jobs: typing.Optional[jsii.Number] = None,
        maximum_runtime_per_job: typing.Optional[builtins.str] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        metrics_access_security_group_id: typing.Optional[builtins.str] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        num_total_jobs: typing.Optional[jsii.Number] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        preemptible_machines: typing.Optional[builtins.bool] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        use_firecracker: typing.Optional[builtins.bool] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_tag: A label tag to add to all the executors. Can be used for filtering out the right instances in stackdriver monitoring.
        :param metrics_environment_label: The value for environment by which to filter the custom metrics.
        :param queue_name: The queue from which the executor should dequeue jobs.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param sourcegraph_executor_proxy_password: The shared password used to authenticate requests to the internal executor proxy.
        :param sourcegraph_external_url: The externally accessible URL of the target Sourcegraph instance.
        :param subnet_id: The ID of the subnet within the given VPC to run the instance in.
        :param vpc_id: The ID of the VPC to run the instance in.
        :param assign_public_ip: If false, no public IP will be associated with the executors. Default: true
        :param boot_disk_iops: Executor node disk additional IOPS. Default: 3000
        :param boot_disk_size: Executor node disk size in GB. Default: 500
        :param boot_disk_throughput: Executor node disk throughput in MiB/s. Default: 125
        :param docker_auth_config: If provided, this docker auth config file will be used to authorize image pulls. See `Using private registries <https://docs.sourcegraph.com/admin/deploy_executors#using-private-registries>`_ for how to configure.
        :param docker_registry_mirror: A URL to a docker registry mirror to use (falling back to docker.io).
        :param docker_registry_mirror_node_exporter_url: A URL to a docker registry mirror node exporter to scrape (optional).
        :param firecracker_disk_space: The amount of disk space to give to each firecracker VM. Default: 20GB
        :param firecracker_memory: The amount of memory to give to each firecracker VM. Default: 12GB
        :param firecracker_num_cpus: The number of CPUs to give to each firecracker VM. Default: 4
        :param http_access_cidr_range: DEPRECATED. This is not used anymore. Default: 0.0.0.0/0
        :param job_memory: The amount of memory to allocate to each virtual machine or container. Default: 12GB
        :param job_num_cpus: The number of CPUs to allocate to each virtual machine or container. Default: 4
        :param jobs_per_instance_scaling: The amount of jobs a single instance should have in queue. Used for autoscaling. Default: 360
        :param machine_image: Executor node machine disk image to use for creating the boot volume. Leave empty to use latest compatible with the Sourcegraph version.
        :param machine_type: Executor node machine type. Default: c5n.metal
        :param max_active_time: The maximum time that can be spent by the worker dequeueing records to be handled. Default: 2h
        :param maximum_num_jobs: The number of jobs to run concurrently per executor instance. Default: 18
        :param maximum_runtime_per_job: The maximum wall time that can be spent on a single job. Default: 30m
        :param max_replicas: The maximum number of executor instances to run in the autoscaling group. Default: 1
        :param metrics_access_security_group_id: If provided, the default security groups will not be created. The ID of the security group to associate the Launch Template network with.
        :param min_replicas: The minimum number of executor instances to run in the autoscaling group. Default: 1
        :param num_total_jobs: The maximum number of jobs that will be dequeued by the worker. Default: 1800
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param preemptible_machines: Whether to use preemptible machines instead of standard machines; usually way cheaper but might be terminated at any time
        :param resource_prefix: An optional prefix to add to all resources created.
        :param ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instances is acceptable. Default: 10.0.0.0/16
        :param use_firecracker: Whether to isolate commands in virtual machines. Default: true
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2d472c3261a52d32c68cbe08084bd89bb269533851f3d17720a3c26992626c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ExecutorsExecutorsConfig(
            instance_tag=instance_tag,
            metrics_environment_label=metrics_environment_label,
            queue_name=queue_name,
            randomize_resource_names=randomize_resource_names,
            sourcegraph_executor_proxy_password=sourcegraph_executor_proxy_password,
            sourcegraph_external_url=sourcegraph_external_url,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            assign_public_ip=assign_public_ip,
            boot_disk_iops=boot_disk_iops,
            boot_disk_size=boot_disk_size,
            boot_disk_throughput=boot_disk_throughput,
            docker_auth_config=docker_auth_config,
            docker_registry_mirror=docker_registry_mirror,
            docker_registry_mirror_node_exporter_url=docker_registry_mirror_node_exporter_url,
            firecracker_disk_space=firecracker_disk_space,
            firecracker_memory=firecracker_memory,
            firecracker_num_cpus=firecracker_num_cpus,
            http_access_cidr_range=http_access_cidr_range,
            job_memory=job_memory,
            job_num_cpus=job_num_cpus,
            jobs_per_instance_scaling=jobs_per_instance_scaling,
            machine_image=machine_image,
            machine_type=machine_type,
            max_active_time=max_active_time,
            maximum_num_jobs=maximum_num_jobs,
            maximum_runtime_per_job=maximum_runtime_per_job,
            max_replicas=max_replicas,
            metrics_access_security_group_id=metrics_access_security_group_id,
            min_replicas=min_replicas,
            num_total_jobs=num_total_jobs,
            permissions_boundary_arn=permissions_boundary_arn,
            preemptible_machines=preemptible_machines,
            resource_prefix=resource_prefix,
            ssh_access_cidr_range=ssh_access_cidr_range,
            use_firecracker=use_firecracker,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTag")
    def instance_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTag"))

    @instance_tag.setter
    def instance_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6645408133970c664912cb082e79e449202b861814a86440f0d1e6581f0bf96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTag", value)

    @builtins.property
    @jsii.member(jsii_name="metricsEnvironmentLabel")
    def metrics_environment_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsEnvironmentLabel"))

    @metrics_environment_label.setter
    def metrics_environment_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d80b080b0ee365fd99f6aab240acdf8d6340de27d4209384b123fdaaae4ad86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsEnvironmentLabel", value)

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3651fb2cb46844b66eacfa397ccc9af6a080e60283315e383d015c2e87445b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value)

    @builtins.property
    @jsii.member(jsii_name="randomizeResourceNames")
    def randomize_resource_names(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "randomizeResourceNames"))

    @randomize_resource_names.setter
    def randomize_resource_names(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c287e9cd127170ae930114539d2e036d0e5f1613cc3a059e65324af14332f042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizeResourceNames", value)

    @builtins.property
    @jsii.member(jsii_name="sourcegraphExecutorProxyPassword")
    def sourcegraph_executor_proxy_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcegraphExecutorProxyPassword"))

    @sourcegraph_executor_proxy_password.setter
    def sourcegraph_executor_proxy_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333ac119311cc8162556133987582e7f5381a2aa20ae7403f75a2b0e8df8a9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcegraphExecutorProxyPassword", value)

    @builtins.property
    @jsii.member(jsii_name="sourcegraphExternalUrl")
    def sourcegraph_external_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcegraphExternalUrl"))

    @sourcegraph_external_url.setter
    def sourcegraph_external_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1c34c3f7b49ecc59790aa6ddacdc301d97c8d663f1d4f765d889d2013fe13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcegraphExternalUrl", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a532752da9dd626130b6d30f3b112a92c4e028cad619dca14501af87dc7e2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c589cb5a3e0ae2adf5c51fcdf16742543cd27d61f8de86a65df7228ad4bf4d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "assignPublicIp"))

    @assign_public_ip.setter
    def assign_public_ip(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e1fa6c279cd36a28aa40d27a082a3245a309b509b280256694aa2d7acfc320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskIops")
    def boot_disk_iops(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskIops"))

    @boot_disk_iops.setter
    def boot_disk_iops(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7661c6053fe5b73fb3cd09847f2135daf3341c7d79cadcbf9abdff47be11909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskIops", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskSize")
    def boot_disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSize"))

    @boot_disk_size.setter
    def boot_disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79696484cf29ab9830e40b7b1d06f3212299901a99a31a541cbf5fa5e3af7004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSize", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskThroughput")
    def boot_disk_throughput(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskThroughput"))

    @boot_disk_throughput.setter
    def boot_disk_throughput(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde166a071877b1935971cb129a71fa566629d95e718daa283a6360afa1b6587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskThroughput", value)

    @builtins.property
    @jsii.member(jsii_name="dockerAuthConfig")
    def docker_auth_config(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerAuthConfig"))

    @docker_auth_config.setter
    def docker_auth_config(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fc222ac29343351ea6b8a60c99682f0dd636d50e2a33c3430b2fed7583a765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dockerRegistryMirror")
    def docker_registry_mirror(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerRegistryMirror"))

    @docker_registry_mirror.setter
    def docker_registry_mirror(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7586d8bc5da12ce8b37169ddf34684d4a3c10864a808afbacb5db4daa07d70fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRegistryMirror", value)

    @builtins.property
    @jsii.member(jsii_name="dockerRegistryMirrorNodeExporterUrl")
    def docker_registry_mirror_node_exporter_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerRegistryMirrorNodeExporterUrl"))

    @docker_registry_mirror_node_exporter_url.setter
    def docker_registry_mirror_node_exporter_url(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df36398a9e96c19e61f85a00a5766e63591e94787936fd8d69ee9df21746b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRegistryMirrorNodeExporterUrl", value)

    @builtins.property
    @jsii.member(jsii_name="firecrackerDiskSpace")
    def firecracker_disk_space(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firecrackerDiskSpace"))

    @firecracker_disk_space.setter
    def firecracker_disk_space(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5888aa7874e17e5a8191ca53e9be57bdd2f4a58e402b0fa113afebe418afe40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firecrackerDiskSpace", value)

    @builtins.property
    @jsii.member(jsii_name="firecrackerMemory")
    def firecracker_memory(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firecrackerMemory"))

    @firecracker_memory.setter
    def firecracker_memory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13abb9af00f396b9211d1f581b54e4f56f0dca126e23268148a7f01ce40223c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firecrackerMemory", value)

    @builtins.property
    @jsii.member(jsii_name="firecrackerNumCpus")
    def firecracker_num_cpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firecrackerNumCpus"))

    @firecracker_num_cpus.setter
    def firecracker_num_cpus(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2e37dee9db072a4eec6fc746321a9170fac72c3c610e275dea642bea9cd890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firecrackerNumCpus", value)

    @builtins.property
    @jsii.member(jsii_name="httpAccessCidrRange")
    def http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpAccessCidrRange"))

    @http_access_cidr_range.setter
    def http_access_cidr_range(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f5691ce7d696b9bfaacf9115301b9a9dc871395e475c5ae86181404e8310e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="jobMemory")
    def job_memory(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobMemory"))

    @job_memory.setter
    def job_memory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe55962fbbaa6c6affb17526f09e20b87cf7413f8d826539c39bb7dabb8599a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobMemory", value)

    @builtins.property
    @jsii.member(jsii_name="jobNumCpus")
    def job_num_cpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jobNumCpus"))

    @job_num_cpus.setter
    def job_num_cpus(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77c751e03f121c93696752355d935b814fe547d806aaa7e0357f8d23338b482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobNumCpus", value)

    @builtins.property
    @jsii.member(jsii_name="jobsPerInstanceScaling")
    def jobs_per_instance_scaling(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jobsPerInstanceScaling"))

    @jobs_per_instance_scaling.setter
    def jobs_per_instance_scaling(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51586700096d7281a3dc306707c8fdd268273b5bb30c94967b11644ead387907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobsPerInstanceScaling", value)

    @builtins.property
    @jsii.member(jsii_name="machineImage")
    def machine_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineImage"))

    @machine_image.setter
    def machine_image(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d325f2d36d65736306a9cc9e45b0d1134e19a56862536c3b8b01a0200c41d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineImage", value)

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee19335ff8fdc83d580c34ab0586b38a3483a94c609ace1a0369369cc331d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value)

    @builtins.property
    @jsii.member(jsii_name="maxActiveTime")
    def max_active_time(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxActiveTime"))

    @max_active_time.setter
    def max_active_time(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93df5647d3ebeaeb3ee664b24afe33784141441644ea3a0722fb9f72f356d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxActiveTime", value)

    @builtins.property
    @jsii.member(jsii_name="maximumNumJobs")
    def maximum_num_jobs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumNumJobs"))

    @maximum_num_jobs.setter
    def maximum_num_jobs(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fc492a5423aed167a57bef6dcc51e84da60ea9d0ac34025a2c70cebcdd2fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumNumJobs", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRuntimePerJob")
    def maximum_runtime_per_job(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumRuntimePerJob"))

    @maximum_runtime_per_job.setter
    def maximum_runtime_per_job(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180785cc9cec53a3cde244a73d43a1a89bbfd944c254b74ddb48d900c1e433d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRuntimePerJob", value)

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3ec168e9c1359f2471a3f48c1c3db47d19ed57136019bcc0a2a43769e97129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value)

    @builtins.property
    @jsii.member(jsii_name="metricsAccessSecurityGroupId")
    def metrics_access_security_group_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsAccessSecurityGroupId"))

    @metrics_access_security_group_id.setter
    def metrics_access_security_group_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152782f0c0e7022250e10faed30e098657e5b1706b6b5c106a8e79f844992f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsAccessSecurityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e328d58ae5823a9b5ef9bb0294cad3ee8e77aa3f459dfd3573ad007646f5a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value)

    @builtins.property
    @jsii.member(jsii_name="numTotalJobs")
    def num_total_jobs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numTotalJobs"))

    @num_total_jobs.setter
    def num_total_jobs(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494a32cce41c82332b536f7bdc72654a4b8dd44c46367553f4115b6981c76cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numTotalJobs", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaryArn")
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaryArn"))

    @permissions_boundary_arn.setter
    def permissions_boundary_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0defac2ff6222aec0ec061eb9003da566a20d8ed6e2409f43a301dc1eeffb8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaryArn", value)

    @builtins.property
    @jsii.member(jsii_name="preemptibleMachines")
    def preemptible_machines(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "preemptibleMachines"))

    @preemptible_machines.setter
    def preemptible_machines(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3cceb1c5b4d3ebf707029cbbf1911ad3c9d242086e6d5100ac88fb907b63b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptibleMachines", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b50488ab753f1816da7d658f4f1d27941173bc84c56a8204ebcc554af37043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="sshAccessCidrRange")
    def ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshAccessCidrRange"))

    @ssh_access_cidr_range.setter
    def ssh_access_cidr_range(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a42b4a8c9a2a7357f319dde66f8cec5690b69c33554fc9176cf9d37623ba8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshAccessCidrRange", value)

    @builtins.property
    @jsii.member(jsii_name="useFirecracker")
    def use_firecracker(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useFirecracker"))

    @use_firecracker.setter
    def use_firecracker(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0738c72f1858464d7f949ec7bbf6eaff48500a9a3798e5a081c3a6f0f84a82a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFirecracker", value)


@jsii.data_type(
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsExecutorsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "instance_tag": "instanceTag",
        "metrics_environment_label": "metricsEnvironmentLabel",
        "queue_name": "queueName",
        "randomize_resource_names": "randomizeResourceNames",
        "sourcegraph_executor_proxy_password": "sourcegraphExecutorProxyPassword",
        "sourcegraph_external_url": "sourcegraphExternalUrl",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "assign_public_ip": "assignPublicIp",
        "boot_disk_iops": "bootDiskIops",
        "boot_disk_size": "bootDiskSize",
        "boot_disk_throughput": "bootDiskThroughput",
        "docker_auth_config": "dockerAuthConfig",
        "docker_registry_mirror": "dockerRegistryMirror",
        "docker_registry_mirror_node_exporter_url": "dockerRegistryMirrorNodeExporterUrl",
        "firecracker_disk_space": "firecrackerDiskSpace",
        "firecracker_memory": "firecrackerMemory",
        "firecracker_num_cpus": "firecrackerNumCpus",
        "http_access_cidr_range": "httpAccessCidrRange",
        "job_memory": "jobMemory",
        "job_num_cpus": "jobNumCpus",
        "jobs_per_instance_scaling": "jobsPerInstanceScaling",
        "machine_image": "machineImage",
        "machine_type": "machineType",
        "max_active_time": "maxActiveTime",
        "maximum_num_jobs": "maximumNumJobs",
        "maximum_runtime_per_job": "maximumRuntimePerJob",
        "max_replicas": "maxReplicas",
        "metrics_access_security_group_id": "metricsAccessSecurityGroupId",
        "min_replicas": "minReplicas",
        "num_total_jobs": "numTotalJobs",
        "permissions_boundary_arn": "permissionsBoundaryArn",
        "preemptible_machines": "preemptibleMachines",
        "resource_prefix": "resourcePrefix",
        "ssh_access_cidr_range": "sshAccessCidrRange",
        "use_firecracker": "useFirecracker",
    },
)
class ExecutorsExecutorsConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        instance_tag: builtins.str,
        metrics_environment_label: builtins.str,
        queue_name: builtins.str,
        randomize_resource_names: builtins.bool,
        sourcegraph_executor_proxy_password: builtins.str,
        sourcegraph_external_url: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        boot_disk_iops: typing.Optional[jsii.Number] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        boot_disk_throughput: typing.Optional[jsii.Number] = None,
        docker_auth_config: typing.Optional[builtins.str] = None,
        docker_registry_mirror: typing.Optional[builtins.str] = None,
        docker_registry_mirror_node_exporter_url: typing.Optional[builtins.str] = None,
        firecracker_disk_space: typing.Optional[builtins.str] = None,
        firecracker_memory: typing.Optional[builtins.str] = None,
        firecracker_num_cpus: typing.Optional[jsii.Number] = None,
        http_access_cidr_range: typing.Optional[builtins.str] = None,
        job_memory: typing.Optional[builtins.str] = None,
        job_num_cpus: typing.Optional[jsii.Number] = None,
        jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
        machine_image: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_active_time: typing.Optional[builtins.str] = None,
        maximum_num_jobs: typing.Optional[jsii.Number] = None,
        maximum_runtime_per_job: typing.Optional[builtins.str] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        metrics_access_security_group_id: typing.Optional[builtins.str] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        num_total_jobs: typing.Optional[jsii.Number] = None,
        permissions_boundary_arn: typing.Optional[builtins.str] = None,
        preemptible_machines: typing.Optional[builtins.bool] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        ssh_access_cidr_range: typing.Optional[builtins.str] = None,
        use_firecracker: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param instance_tag: A label tag to add to all the executors. Can be used for filtering out the right instances in stackdriver monitoring.
        :param metrics_environment_label: The value for environment by which to filter the custom metrics.
        :param queue_name: The queue from which the executor should dequeue jobs.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param sourcegraph_executor_proxy_password: The shared password used to authenticate requests to the internal executor proxy.
        :param sourcegraph_external_url: The externally accessible URL of the target Sourcegraph instance.
        :param subnet_id: The ID of the subnet within the given VPC to run the instance in.
        :param vpc_id: The ID of the VPC to run the instance in.
        :param assign_public_ip: If false, no public IP will be associated with the executors. Default: true
        :param boot_disk_iops: Executor node disk additional IOPS. Default: 3000
        :param boot_disk_size: Executor node disk size in GB. Default: 500
        :param boot_disk_throughput: Executor node disk throughput in MiB/s. Default: 125
        :param docker_auth_config: If provided, this docker auth config file will be used to authorize image pulls. See `Using private registries <https://docs.sourcegraph.com/admin/deploy_executors#using-private-registries>`_ for how to configure.
        :param docker_registry_mirror: A URL to a docker registry mirror to use (falling back to docker.io).
        :param docker_registry_mirror_node_exporter_url: A URL to a docker registry mirror node exporter to scrape (optional).
        :param firecracker_disk_space: The amount of disk space to give to each firecracker VM. Default: 20GB
        :param firecracker_memory: The amount of memory to give to each firecracker VM. Default: 12GB
        :param firecracker_num_cpus: The number of CPUs to give to each firecracker VM. Default: 4
        :param http_access_cidr_range: DEPRECATED. This is not used anymore. Default: 0.0.0.0/0
        :param job_memory: The amount of memory to allocate to each virtual machine or container. Default: 12GB
        :param job_num_cpus: The number of CPUs to allocate to each virtual machine or container. Default: 4
        :param jobs_per_instance_scaling: The amount of jobs a single instance should have in queue. Used for autoscaling. Default: 360
        :param machine_image: Executor node machine disk image to use for creating the boot volume. Leave empty to use latest compatible with the Sourcegraph version.
        :param machine_type: Executor node machine type. Default: c5n.metal
        :param max_active_time: The maximum time that can be spent by the worker dequeueing records to be handled. Default: 2h
        :param maximum_num_jobs: The number of jobs to run concurrently per executor instance. Default: 18
        :param maximum_runtime_per_job: The maximum wall time that can be spent on a single job. Default: 30m
        :param max_replicas: The maximum number of executor instances to run in the autoscaling group. Default: 1
        :param metrics_access_security_group_id: If provided, the default security groups will not be created. The ID of the security group to associate the Launch Template network with.
        :param min_replicas: The minimum number of executor instances to run in the autoscaling group. Default: 1
        :param num_total_jobs: The maximum number of jobs that will be dequeued by the worker. Default: 1800
        :param permissions_boundary_arn: If not provided, there will be no permissions boundary on IAM roles and users created. The ARN of a policy to use for permissions boundaries with IAM roles and users.
        :param preemptible_machines: Whether to use preemptible machines instead of standard machines; usually way cheaper but might be terminated at any time
        :param resource_prefix: An optional prefix to add to all resources created.
        :param ssh_access_cidr_range: CIDR range from where SSH access to the EC2 instances is acceptable. Default: 10.0.0.0/16
        :param use_firecracker: Whether to isolate commands in virtual machines. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99535d11a7a1a8cdddfe7c61de3cafa9dc4af5f409d6ef90c544d4618f3ab78c)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument instance_tag", value=instance_tag, expected_type=type_hints["instance_tag"])
            check_type(argname="argument metrics_environment_label", value=metrics_environment_label, expected_type=type_hints["metrics_environment_label"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument randomize_resource_names", value=randomize_resource_names, expected_type=type_hints["randomize_resource_names"])
            check_type(argname="argument sourcegraph_executor_proxy_password", value=sourcegraph_executor_proxy_password, expected_type=type_hints["sourcegraph_executor_proxy_password"])
            check_type(argname="argument sourcegraph_external_url", value=sourcegraph_external_url, expected_type=type_hints["sourcegraph_external_url"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument boot_disk_iops", value=boot_disk_iops, expected_type=type_hints["boot_disk_iops"])
            check_type(argname="argument boot_disk_size", value=boot_disk_size, expected_type=type_hints["boot_disk_size"])
            check_type(argname="argument boot_disk_throughput", value=boot_disk_throughput, expected_type=type_hints["boot_disk_throughput"])
            check_type(argname="argument docker_auth_config", value=docker_auth_config, expected_type=type_hints["docker_auth_config"])
            check_type(argname="argument docker_registry_mirror", value=docker_registry_mirror, expected_type=type_hints["docker_registry_mirror"])
            check_type(argname="argument docker_registry_mirror_node_exporter_url", value=docker_registry_mirror_node_exporter_url, expected_type=type_hints["docker_registry_mirror_node_exporter_url"])
            check_type(argname="argument firecracker_disk_space", value=firecracker_disk_space, expected_type=type_hints["firecracker_disk_space"])
            check_type(argname="argument firecracker_memory", value=firecracker_memory, expected_type=type_hints["firecracker_memory"])
            check_type(argname="argument firecracker_num_cpus", value=firecracker_num_cpus, expected_type=type_hints["firecracker_num_cpus"])
            check_type(argname="argument http_access_cidr_range", value=http_access_cidr_range, expected_type=type_hints["http_access_cidr_range"])
            check_type(argname="argument job_memory", value=job_memory, expected_type=type_hints["job_memory"])
            check_type(argname="argument job_num_cpus", value=job_num_cpus, expected_type=type_hints["job_num_cpus"])
            check_type(argname="argument jobs_per_instance_scaling", value=jobs_per_instance_scaling, expected_type=type_hints["jobs_per_instance_scaling"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument max_active_time", value=max_active_time, expected_type=type_hints["max_active_time"])
            check_type(argname="argument maximum_num_jobs", value=maximum_num_jobs, expected_type=type_hints["maximum_num_jobs"])
            check_type(argname="argument maximum_runtime_per_job", value=maximum_runtime_per_job, expected_type=type_hints["maximum_runtime_per_job"])
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument metrics_access_security_group_id", value=metrics_access_security_group_id, expected_type=type_hints["metrics_access_security_group_id"])
            check_type(argname="argument min_replicas", value=min_replicas, expected_type=type_hints["min_replicas"])
            check_type(argname="argument num_total_jobs", value=num_total_jobs, expected_type=type_hints["num_total_jobs"])
            check_type(argname="argument permissions_boundary_arn", value=permissions_boundary_arn, expected_type=type_hints["permissions_boundary_arn"])
            check_type(argname="argument preemptible_machines", value=preemptible_machines, expected_type=type_hints["preemptible_machines"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument ssh_access_cidr_range", value=ssh_access_cidr_range, expected_type=type_hints["ssh_access_cidr_range"])
            check_type(argname="argument use_firecracker", value=use_firecracker, expected_type=type_hints["use_firecracker"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_tag": instance_tag,
            "metrics_environment_label": metrics_environment_label,
            "queue_name": queue_name,
            "randomize_resource_names": randomize_resource_names,
            "sourcegraph_executor_proxy_password": sourcegraph_executor_proxy_password,
            "sourcegraph_external_url": sourcegraph_external_url,
            "subnet_id": subnet_id,
            "vpc_id": vpc_id,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if boot_disk_iops is not None:
            self._values["boot_disk_iops"] = boot_disk_iops
        if boot_disk_size is not None:
            self._values["boot_disk_size"] = boot_disk_size
        if boot_disk_throughput is not None:
            self._values["boot_disk_throughput"] = boot_disk_throughput
        if docker_auth_config is not None:
            self._values["docker_auth_config"] = docker_auth_config
        if docker_registry_mirror is not None:
            self._values["docker_registry_mirror"] = docker_registry_mirror
        if docker_registry_mirror_node_exporter_url is not None:
            self._values["docker_registry_mirror_node_exporter_url"] = docker_registry_mirror_node_exporter_url
        if firecracker_disk_space is not None:
            self._values["firecracker_disk_space"] = firecracker_disk_space
        if firecracker_memory is not None:
            self._values["firecracker_memory"] = firecracker_memory
        if firecracker_num_cpus is not None:
            self._values["firecracker_num_cpus"] = firecracker_num_cpus
        if http_access_cidr_range is not None:
            self._values["http_access_cidr_range"] = http_access_cidr_range
        if job_memory is not None:
            self._values["job_memory"] = job_memory
        if job_num_cpus is not None:
            self._values["job_num_cpus"] = job_num_cpus
        if jobs_per_instance_scaling is not None:
            self._values["jobs_per_instance_scaling"] = jobs_per_instance_scaling
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_active_time is not None:
            self._values["max_active_time"] = max_active_time
        if maximum_num_jobs is not None:
            self._values["maximum_num_jobs"] = maximum_num_jobs
        if maximum_runtime_per_job is not None:
            self._values["maximum_runtime_per_job"] = maximum_runtime_per_job
        if max_replicas is not None:
            self._values["max_replicas"] = max_replicas
        if metrics_access_security_group_id is not None:
            self._values["metrics_access_security_group_id"] = metrics_access_security_group_id
        if min_replicas is not None:
            self._values["min_replicas"] = min_replicas
        if num_total_jobs is not None:
            self._values["num_total_jobs"] = num_total_jobs
        if permissions_boundary_arn is not None:
            self._values["permissions_boundary_arn"] = permissions_boundary_arn
        if preemptible_machines is not None:
            self._values["preemptible_machines"] = preemptible_machines
        if resource_prefix is not None:
            self._values["resource_prefix"] = resource_prefix
        if ssh_access_cidr_range is not None:
            self._values["ssh_access_cidr_range"] = ssh_access_cidr_range
        if use_firecracker is not None:
            self._values["use_firecracker"] = use_firecracker

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_tag(self) -> builtins.str:
        '''A label tag to add to all the executors.

        Can be used for filtering out the right instances in stackdriver monitoring.
        '''
        result = self._values.get("instance_tag")
        assert result is not None, "Required property 'instance_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metrics_environment_label(self) -> builtins.str:
        '''The value for environment by which to filter the custom metrics.'''
        result = self._values.get("metrics_environment_label")
        assert result is not None, "Required property 'metrics_environment_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''The queue from which the executor should dequeue jobs.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def randomize_resource_names(self) -> builtins.bool:
        '''Use randomized names for resources.

        Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        '''
        result = self._values.get("randomize_resource_names")
        assert result is not None, "Required property 'randomize_resource_names' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def sourcegraph_executor_proxy_password(self) -> builtins.str:
        '''The shared password used to authenticate requests to the internal executor proxy.'''
        result = self._values.get("sourcegraph_executor_proxy_password")
        assert result is not None, "Required property 'sourcegraph_executor_proxy_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sourcegraph_external_url(self) -> builtins.str:
        '''The externally accessible URL of the target Sourcegraph instance.'''
        result = self._values.get("sourcegraph_external_url")
        assert result is not None, "Required property 'sourcegraph_external_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ID of the subnet within the given VPC to run the instance in.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The ID of the VPC to run the instance in.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''If false, no public IP will be associated with the executors.

        :default: true
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def boot_disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Executor node disk additional IOPS.

        :default: 3000
        '''
        result = self._values.get("boot_disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Executor node disk size in GB.

        :default: 500
        '''
        result = self._values.get("boot_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_throughput(self) -> typing.Optional[jsii.Number]:
        '''Executor node disk throughput in MiB/s.

        :default: 125
        '''
        result = self._values.get("boot_disk_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_auth_config(self) -> typing.Optional[builtins.str]:
        '''If provided, this docker auth config file will be used to authorize image pulls.

        See `Using private registries <https://docs.sourcegraph.com/admin/deploy_executors#using-private-registries>`_ for how to configure.
        '''
        result = self._values.get("docker_auth_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_registry_mirror(self) -> typing.Optional[builtins.str]:
        '''A URL to a docker registry mirror to use (falling back to docker.io).'''
        result = self._values.get("docker_registry_mirror")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_registry_mirror_node_exporter_url(self) -> typing.Optional[builtins.str]:
        '''A URL to a docker registry mirror node exporter to scrape (optional).'''
        result = self._values.get("docker_registry_mirror_node_exporter_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firecracker_disk_space(self) -> typing.Optional[builtins.str]:
        '''The amount of disk space to give to each firecracker VM.

        :default: 20GB
        '''
        result = self._values.get("firecracker_disk_space")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firecracker_memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory to give to each firecracker VM.

        :default: 12GB
        '''
        result = self._values.get("firecracker_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firecracker_num_cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs to give to each firecracker VM.

        :default: 4
        '''
        result = self._values.get("firecracker_num_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''DEPRECATED.

        This is not used anymore.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("http_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory to allocate to each virtual machine or container.

        :default: 12GB
        '''
        result = self._values.get("job_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_num_cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs to allocate to each virtual machine or container.

        :default: 4
        '''
        result = self._values.get("job_num_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def jobs_per_instance_scaling(self) -> typing.Optional[jsii.Number]:
        '''The amount of jobs a single instance should have in queue.

        Used for autoscaling.

        :default: 360
        '''
        result = self._values.get("jobs_per_instance_scaling")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[builtins.str]:
        '''Executor node machine disk image to use for creating the boot volume.

        Leave empty to use latest compatible with the Sourcegraph version.
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Executor node machine type.

        :default: c5n.metal
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_active_time(self) -> typing.Optional[builtins.str]:
        '''The maximum time that can be spent by the worker dequeueing records to be handled.

        :default: 2h
        '''
        result = self._values.get("max_active_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_num_jobs(self) -> typing.Optional[jsii.Number]:
        '''The number of jobs to run concurrently per executor instance.

        :default: 18
        '''
        result = self._values.get("maximum_num_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_runtime_per_job(self) -> typing.Optional[builtins.str]:
        '''The maximum wall time that can be spent on a single job.

        :default: 30m
        '''
        result = self._values.get("maximum_runtime_per_job")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_replicas(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of executor instances to run in the autoscaling group.

        :default: 1
        '''
        result = self._values.get("max_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics_access_security_group_id(self) -> typing.Optional[builtins.str]:
        '''If provided, the default security groups will not be created.

        The ID of the security group to associate the Launch Template network with.
        '''
        result = self._values.get("metrics_access_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_replicas(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of executor instances to run in the autoscaling group.

        :default: 1
        '''
        result = self._values.get("min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_total_jobs(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of jobs that will be dequeued by the worker.

        :default: 1800
        '''
        result = self._values.get("num_total_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def permissions_boundary_arn(self) -> typing.Optional[builtins.str]:
        '''If not provided, there will be no permissions boundary on IAM roles and users created.

        The ARN of a policy to use for permissions boundaries with IAM roles and users.
        '''
        result = self._values.get("permissions_boundary_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preemptible_machines(self) -> typing.Optional[builtins.bool]:
        '''Whether to use preemptible machines instead of standard machines;

        usually way cheaper but might be terminated at any time
        '''
        result = self._values.get("preemptible_machines")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix to add to all resources created.'''
        result = self._values.get("resource_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_access_cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range from where SSH access to the EC2 instances is acceptable.

        :default: 10.0.0.0/16
        '''
        result = self._values.get("ssh_access_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_firecracker(self) -> typing.Optional[builtins.bool]:
        '''Whether to isolate commands in virtual machines.

        :default: true
        '''
        result = self._values.get("use_firecracker")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecutorsExecutorsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExecutorsNetworking(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsNetworking",
):
    '''Defines an ExecutorsNetworking based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/sourcegraph/executors/aws/~> 5.0.1/submodules/networking sourcegraph/executors/aws//modules/networking}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zone: builtins.str,
        randomize_resource_names: builtins.bool,
        nat: typing.Optional[builtins.bool] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zone: The availability zone to create the network in.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param nat: When true, the network will contain a NAT router. Use when executors should not get public IPs.
        :param resource_prefix: An optional prefix to add to all resources created.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80b20b4ada2720173c646021f5b2745643f4356f093ee4ab657ed10102c259b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ExecutorsNetworkingConfig(
            availability_zone=availability_zone,
            randomize_resource_names=randomize_resource_names,
            nat=nat,
            resource_prefix=resource_prefix,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="ipCidrOutput")
    def ip_cidr_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCidrOutput"))

    @builtins.property
    @jsii.member(jsii_name="natIpOutput")
    def nat_ip_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natIpOutput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdOutput")
    def subnet_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdOutput")
    def vpc_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821bc2c55aeff422ebd73598a10423931a3f270cb2d73532b3506badb2a88d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="randomizeResourceNames")
    def randomize_resource_names(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "randomizeResourceNames"))

    @randomize_resource_names.setter
    def randomize_resource_names(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f043e04d1572edde9496b87241f08f2e43d2addc643b5231506a15695a0bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizeResourceNames", value)

    @builtins.property
    @jsii.member(jsii_name="nat")
    def nat(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "nat"))

    @nat.setter
    def nat(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31c8e76ff9a7f9ffda1920c7cb6cc133cab57f3b232d5f288603ee1752dee75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nat", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6600427918c7196da16f88e8c325d447ce7c8fad5d0d2e1ca2eda5eb7ee1bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)


@jsii.data_type(
    jsii_type="cdktf-sourcegraph-aws-executors.ExecutorsNetworkingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "availability_zone": "availabilityZone",
        "randomize_resource_names": "randomizeResourceNames",
        "nat": "nat",
        "resource_prefix": "resourcePrefix",
    },
)
class ExecutorsNetworkingConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        availability_zone: builtins.str,
        randomize_resource_names: builtins.bool,
        nat: typing.Optional[builtins.bool] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param availability_zone: The availability zone to create the network in.
        :param randomize_resource_names: Use randomized names for resources. Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        :param nat: When true, the network will contain a NAT router. Use when executors should not get public IPs.
        :param resource_prefix: An optional prefix to add to all resources created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eccaeadd18edb5384c886b8492680582d86cda677bcb2eb73ebbd3d3c26408)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument randomize_resource_names", value=randomize_resource_names, expected_type=type_hints["randomize_resource_names"])
            check_type(argname="argument nat", value=nat, expected_type=type_hints["nat"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "randomize_resource_names": randomize_resource_names,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if nat is not None:
            self._values["nat"] = nat
        if resource_prefix is not None:
            self._values["resource_prefix"] = resource_prefix

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_zone(self) -> builtins.str:
        '''The availability zone to create the network in.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def randomize_resource_names(self) -> builtins.bool:
        '''Use randomized names for resources.

        Deployments using the legacy naming convention will be updated in-place with randomized names when enabled.
        '''
        result = self._values.get("randomize_resource_names")
        assert result is not None, "Required property 'randomize_resource_names' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def nat(self) -> typing.Optional[builtins.bool]:
        '''When true, the network will contain a NAT router.

        Use when executors should not get public IPs.
        '''
        result = self._values.get("nat")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix to add to all resources created.'''
        result = self._values.get("resource_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecutorsNetworkingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Executors",
    "ExecutorsConfig",
    "ExecutorsCredentials",
    "ExecutorsCredentialsConfig",
    "ExecutorsDockerMirror",
    "ExecutorsDockerMirrorConfig",
    "ExecutorsExecutors",
    "ExecutorsExecutorsConfig",
    "ExecutorsNetworking",
    "ExecutorsNetworkingConfig",
]

publication.publish()

def _typecheckingstub__f0a075a5951b704c69bba53af7ce7ab98e142a2a1c6e5357e051571de83bbb59(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zone: builtins.str,
    executor_instance_tag: builtins.str,
    executor_metrics_environment_label: builtins.str,
    executor_queue_name: builtins.str,
    executor_sourcegraph_executor_proxy_password: builtins.str,
    executor_sourcegraph_external_url: builtins.str,
    docker_mirror_boot_disk_size: typing.Optional[jsii.Number] = None,
    docker_mirror_disk_iops: typing.Optional[jsii.Number] = None,
    docker_mirror_http_access_cidr_range: typing.Optional[builtins.str] = None,
    docker_mirror_machine_ami: typing.Optional[builtins.str] = None,
    docker_mirror_machine_type: typing.Optional[builtins.str] = None,
    docker_mirror_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    docker_mirror_static_ip: typing.Optional[builtins.str] = None,
    executor_boot_disk_iops: typing.Optional[jsii.Number] = None,
    executor_boot_disk_size: typing.Optional[jsii.Number] = None,
    executor_docker_auth_config: typing.Optional[builtins.str] = None,
    executor_firecracker_disk_space: typing.Optional[builtins.str] = None,
    executor_firecracker_memory: typing.Optional[builtins.str] = None,
    executor_firecracker_num_cpus: typing.Optional[jsii.Number] = None,
    executor_http_access_cidr_range: typing.Optional[builtins.str] = None,
    executor_job_memory: typing.Optional[builtins.str] = None,
    executor_job_num_cpus: typing.Optional[jsii.Number] = None,
    executor_jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
    executor_machine_image: typing.Optional[builtins.str] = None,
    executor_machine_type: typing.Optional[builtins.str] = None,
    executor_max_active_time: typing.Optional[builtins.str] = None,
    executor_maximum_num_jobs: typing.Optional[jsii.Number] = None,
    executor_maximum_runtime_per_job: typing.Optional[builtins.str] = None,
    executor_max_replicas: typing.Optional[jsii.Number] = None,
    executor_min_replicas: typing.Optional[jsii.Number] = None,
    executor_num_total_jobs: typing.Optional[jsii.Number] = None,
    executor_preemptible_machines: typing.Optional[builtins.bool] = None,
    executor_resource_prefix: typing.Optional[builtins.str] = None,
    executor_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    executor_use_firecracker: typing.Optional[builtins.bool] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    private_networking: typing.Optional[builtins.bool] = None,
    randomize_resource_names: typing.Optional[builtins.bool] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e346fcb720b4d2cbab55e6505bf26c9dbc7a274acbcc4a9fdb18282d014dda9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f345c5e3b34944c658deda25d81e150e808ba52d1fc5eca0dc1e3aa813862a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa39d6fc8ebaeb76b9eb374cfa831b04dc81884e489b228ec449283c86c16dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b0299442afa0bbc89db6b1aff554b1bd925b69b126c028de7d981c2d727118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902d10907f671a7a898816538f8f9224b756c22dd9f6b1478f3bc9db23318dcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0469c275627595896e0de24ff55013e7750eb297398857bf52a25cdf73a7701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d18e38008692b72b4a26ada719a8bcdcf3d3ec1dcfb3ff20a513c1c5b7ca90(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ac5e05688e9c26d8dd53082a78ac01853864cdb1a66c8567b86992751b595b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba81f0b01e77eac389021131622120f81f52ba7f992bb72e96bec6ee3f2234ad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789fdc9200c56687e1ff3f0de9804a803536b1889c9134b908ebbbf03b378dfc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d5ea6662dd70f34a73db068177c553ef49a0cef7ca6c49052e2af5d78d367b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a764fcfc6dbf3b7a6fde20d3e07c1706ebbbad7b34b44ed450ed3424059badb3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cb944d9cecda4af60baa4e9dbc667fb4d41a61c844d9982ca353e07a041f1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81d0de343857d7049e1f892fca296e7460b95fbb1a04a66f216a6e8a199ae2b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1c7ab5dbf61e9105d9046935ddb01871152e6a4a975828ea7fd717555a1dab(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06239811f0de6aab9a4dc02de61c19e915a933740fbb5a329e5a16bef3a31344(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2afca55a57e0bf59cebfd19ac3cdc6bb8e50b76ee2a302c21706f6771f4a8b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5950db96b73bb18d08bd00b9c5b055411042db4c7c7cfe31425d3915fbf661(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56666624923db91f7d3a1915520253c3ea85431564c7cc3857c0e747dafb2af9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53ef0732470c2d6b4217ce2e9f3ff61f49fefa1c7319d0e47d7192a8c85a983(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115eed0d3fe77c18474fa5832134dd40ea880a9f365beae9500666e7eee4a92f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b413a86c6674d68c315bbfe85ea594f9eabb6164770da08b21ecd13180b4a5c7(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009b1096fa99026c4a895aae794959168ff4377828d4ce7a7ceebce81d322f68(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5607fb414140cf5406e44ee4f2af7569d9562fffd86a44e7771cd730df17dfd1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2523f1eb19f8170f300fecbbdcd82af604c09be6a89d8959ca951a6d8f6aae3e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a4bd5f6fff26329689230b3f588bc6abef59865a603796f06af5c5ed9e17c9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b492cfa560e045216a90dcded0c7269d98584a3cd20f01e93b5819189f8f08e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d9dc04753fb2ee8692461444d2091dd80d7f29a2bb2e045b2ed14c75c2dde8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553ed49d5edf9f06359ea8797ebc85d06f4787bbf1d49beefa63bc2d107df475(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a124d54ce0d16b08e0f4bc6fc5cbf4665385050c980d2b41a4b2745db6cf5c96(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f302eb93eacb0717ab0fa10091b20475cb482bfa0f188abd2f1ceb716a48c73(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e344e81c8f08877019642a0a3aabe520a813c95186b6acf0b0412ed6fa86977a(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34dd09832e6a88c01dc9bbdf6861405332ff491d65aeb197f29b96c0ed3db426(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e155a981cddd4dc7769fd0d7ddf56ceeb69aeb23373427657599721042df73(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e84e8a2b93b276e49b0fbad85be8cc29b675407c7e1b7f45fea359d2364c5dc(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6e0a4c1188e33e882dd1d5876a7f791fa1b1bbf968142dd5eba0bfcb91d432(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fca07388510fa77d84c58dda9a01ae5042622f3227fda26ea6fa39d9a72c924(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6794e191e37a371afc93d6a81cf2b2fcddc0e4bae2f342f3d79fb6a6c2aa6c38(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9156a946246b1dc641924e8c681975d034ae22bc368b185038e71ef52182af42(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0003d9f354d4ab227ea287273cd989f9aa2fdef0039d070212a0a7db2efe8f77(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    availability_zone: builtins.str,
    executor_instance_tag: builtins.str,
    executor_metrics_environment_label: builtins.str,
    executor_queue_name: builtins.str,
    executor_sourcegraph_executor_proxy_password: builtins.str,
    executor_sourcegraph_external_url: builtins.str,
    docker_mirror_boot_disk_size: typing.Optional[jsii.Number] = None,
    docker_mirror_disk_iops: typing.Optional[jsii.Number] = None,
    docker_mirror_http_access_cidr_range: typing.Optional[builtins.str] = None,
    docker_mirror_machine_ami: typing.Optional[builtins.str] = None,
    docker_mirror_machine_type: typing.Optional[builtins.str] = None,
    docker_mirror_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    docker_mirror_static_ip: typing.Optional[builtins.str] = None,
    executor_boot_disk_iops: typing.Optional[jsii.Number] = None,
    executor_boot_disk_size: typing.Optional[jsii.Number] = None,
    executor_docker_auth_config: typing.Optional[builtins.str] = None,
    executor_firecracker_disk_space: typing.Optional[builtins.str] = None,
    executor_firecracker_memory: typing.Optional[builtins.str] = None,
    executor_firecracker_num_cpus: typing.Optional[jsii.Number] = None,
    executor_http_access_cidr_range: typing.Optional[builtins.str] = None,
    executor_job_memory: typing.Optional[builtins.str] = None,
    executor_job_num_cpus: typing.Optional[jsii.Number] = None,
    executor_jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
    executor_machine_image: typing.Optional[builtins.str] = None,
    executor_machine_type: typing.Optional[builtins.str] = None,
    executor_max_active_time: typing.Optional[builtins.str] = None,
    executor_maximum_num_jobs: typing.Optional[jsii.Number] = None,
    executor_maximum_runtime_per_job: typing.Optional[builtins.str] = None,
    executor_max_replicas: typing.Optional[jsii.Number] = None,
    executor_min_replicas: typing.Optional[jsii.Number] = None,
    executor_num_total_jobs: typing.Optional[jsii.Number] = None,
    executor_preemptible_machines: typing.Optional[builtins.bool] = None,
    executor_resource_prefix: typing.Optional[builtins.str] = None,
    executor_ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    executor_use_firecracker: typing.Optional[builtins.bool] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    private_networking: typing.Optional[builtins.bool] = None,
    randomize_resource_names: typing.Optional[builtins.bool] = None,
    security_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362a212560d933b8b9c2af0b2d250e58de53b6a1805967672f6fead07af410b5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42e7ffc155edb6b789fadb6dc7f4849e83fb767bce42009eef3a6ccebd69690(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f16c54c9ac1dc6a26d567dc0ba25de6a2922c5c3cd669d4a50acf193c029e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3301cc66fac69c9e930365be1592d9bf64fd8e65ad62ab2441369089855fbbf9(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288d8682c0e6c3527731298cff85996a01af1f42519ecdb6061448ef0cd7a60e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_tag_prefix: builtins.str,
    randomize_resource_names: builtins.bool,
    static_ip: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    boot_disk_size: typing.Optional[jsii.Number] = None,
    disk_iops: typing.Optional[jsii.Number] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    disk_throughput: typing.Optional[jsii.Number] = None,
    docker_mirror_access_security_group_id: typing.Optional[builtins.str] = None,
    http_access_cidr_range: typing.Optional[builtins.str] = None,
    http_metrics_access_cidr_range: typing.Optional[builtins.str] = None,
    machine_ami: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
    ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32596c42f48278a8dac1734ba9974e4b7a23fc22f56bd7b7b47d11becafb7f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b466df1b6635d614615409d1624da6753a43103294a61a9fea1f757e95d5f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffd522a4ea3949942c09ab68342711b11abb207d7558935cfeb51788766a11b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcd07c0d49535b1ebddaf5b0506f01572469f26a0aeb507c78f3c63c7a5d08b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885894d7585064fae864e24aa72829a0fcebf6d204fa819ec34a1b8603e21301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93f0196a55e002f3ce21f10ec1ee5ca433acb13b99f66db8ff9edbd48d64ed5(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879fec2bbf68095ad74b69d46edd5198b2c04416c67af365a3a6c1ea8e2875ca(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2029f86f845d28012d80b512e23a8d6771d36ea8a381a901eefd617edd686a74(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700be7fb57f1c58f5ecf419f84bb6fe1131d07a6ee660e84b7484cb5e34e1e09(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804759b98b7f064f2a8b5a9b092e702633f0ba9799d36915b4bdc942657f377a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97609b51937f49a83fc60de7a8a380b4ff7aa94b8f565f846a2ea7c0ef47c8ed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e1ac6d4fdc93edc4cec45d466524a85970cf5a73a6266002e4baca4af65c22(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d50c035ee8bf1d722c32d4668333926e021cb5fa33a4fed74719b30c8ef9ab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536451cdbb7949281a5b22d24e2166f64f727bcb2f43da470d612ec371827a0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d803c51ec1f321c45123fe325d4a45f008ced6aed2f972303e2d403c3c9509(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2683020821e46c7166679d48636b0865c428de14e08f01efe772be10aba501(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013618a1baa01c1e1cd58161e1e9e6e8c478913f1c8b60a8274a0dea85110c7e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656d02802e2e69b6f178e9a6d42931bb3781262fa74ecd4db9cecb0742f1ce7d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eede05f92bb53955976dcf73b08229654e39bfeaecf513d086087ced2bd17c91(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    instance_tag_prefix: builtins.str,
    randomize_resource_names: builtins.bool,
    static_ip: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    boot_disk_size: typing.Optional[jsii.Number] = None,
    disk_iops: typing.Optional[jsii.Number] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    disk_throughput: typing.Optional[jsii.Number] = None,
    docker_mirror_access_security_group_id: typing.Optional[builtins.str] = None,
    http_access_cidr_range: typing.Optional[builtins.str] = None,
    http_metrics_access_cidr_range: typing.Optional[builtins.str] = None,
    machine_ami: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
    ssh_access_cidr_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2d472c3261a52d32c68cbe08084bd89bb269533851f3d17720a3c26992626c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_tag: builtins.str,
    metrics_environment_label: builtins.str,
    queue_name: builtins.str,
    randomize_resource_names: builtins.bool,
    sourcegraph_executor_proxy_password: builtins.str,
    sourcegraph_external_url: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    boot_disk_iops: typing.Optional[jsii.Number] = None,
    boot_disk_size: typing.Optional[jsii.Number] = None,
    boot_disk_throughput: typing.Optional[jsii.Number] = None,
    docker_auth_config: typing.Optional[builtins.str] = None,
    docker_registry_mirror: typing.Optional[builtins.str] = None,
    docker_registry_mirror_node_exporter_url: typing.Optional[builtins.str] = None,
    firecracker_disk_space: typing.Optional[builtins.str] = None,
    firecracker_memory: typing.Optional[builtins.str] = None,
    firecracker_num_cpus: typing.Optional[jsii.Number] = None,
    http_access_cidr_range: typing.Optional[builtins.str] = None,
    job_memory: typing.Optional[builtins.str] = None,
    job_num_cpus: typing.Optional[jsii.Number] = None,
    jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
    machine_image: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_active_time: typing.Optional[builtins.str] = None,
    maximum_num_jobs: typing.Optional[jsii.Number] = None,
    maximum_runtime_per_job: typing.Optional[builtins.str] = None,
    max_replicas: typing.Optional[jsii.Number] = None,
    metrics_access_security_group_id: typing.Optional[builtins.str] = None,
    min_replicas: typing.Optional[jsii.Number] = None,
    num_total_jobs: typing.Optional[jsii.Number] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    preemptible_machines: typing.Optional[builtins.bool] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
    ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    use_firecracker: typing.Optional[builtins.bool] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6645408133970c664912cb082e79e449202b861814a86440f0d1e6581f0bf96d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d80b080b0ee365fd99f6aab240acdf8d6340de27d4209384b123fdaaae4ad86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3651fb2cb46844b66eacfa397ccc9af6a080e60283315e383d015c2e87445b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c287e9cd127170ae930114539d2e036d0e5f1613cc3a059e65324af14332f042(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333ac119311cc8162556133987582e7f5381a2aa20ae7403f75a2b0e8df8a9b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1c34c3f7b49ecc59790aa6ddacdc301d97c8d663f1d4f765d889d2013fe13a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a532752da9dd626130b6d30f3b112a92c4e028cad619dca14501af87dc7e2de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c589cb5a3e0ae2adf5c51fcdf16742543cd27d61f8de86a65df7228ad4bf4d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e1fa6c279cd36a28aa40d27a082a3245a309b509b280256694aa2d7acfc320(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7661c6053fe5b73fb3cd09847f2135daf3341c7d79cadcbf9abdff47be11909(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79696484cf29ab9830e40b7b1d06f3212299901a99a31a541cbf5fa5e3af7004(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde166a071877b1935971cb129a71fa566629d95e718daa283a6360afa1b6587(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fc222ac29343351ea6b8a60c99682f0dd636d50e2a33c3430b2fed7583a765(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7586d8bc5da12ce8b37169ddf34684d4a3c10864a808afbacb5db4daa07d70fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df36398a9e96c19e61f85a00a5766e63591e94787936fd8d69ee9df21746b65(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5888aa7874e17e5a8191ca53e9be57bdd2f4a58e402b0fa113afebe418afe40(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13abb9af00f396b9211d1f581b54e4f56f0dca126e23268148a7f01ce40223c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2e37dee9db072a4eec6fc746321a9170fac72c3c610e275dea642bea9cd890(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f5691ce7d696b9bfaacf9115301b9a9dc871395e475c5ae86181404e8310e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe55962fbbaa6c6affb17526f09e20b87cf7413f8d826539c39bb7dabb8599a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77c751e03f121c93696752355d935b814fe547d806aaa7e0357f8d23338b482(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51586700096d7281a3dc306707c8fdd268273b5bb30c94967b11644ead387907(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d325f2d36d65736306a9cc9e45b0d1134e19a56862536c3b8b01a0200c41d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee19335ff8fdc83d580c34ab0586b38a3483a94c609ace1a0369369cc331d2c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93df5647d3ebeaeb3ee664b24afe33784141441644ea3a0722fb9f72f356d98(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fc492a5423aed167a57bef6dcc51e84da60ea9d0ac34025a2c70cebcdd2fb9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180785cc9cec53a3cde244a73d43a1a89bbfd944c254b74ddb48d900c1e433d4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3ec168e9c1359f2471a3f48c1c3db47d19ed57136019bcc0a2a43769e97129(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152782f0c0e7022250e10faed30e098657e5b1706b6b5c106a8e79f844992f6a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e328d58ae5823a9b5ef9bb0294cad3ee8e77aa3f459dfd3573ad007646f5a6e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494a32cce41c82332b536f7bdc72654a4b8dd44c46367553f4115b6981c76cfc(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0defac2ff6222aec0ec061eb9003da566a20d8ed6e2409f43a301dc1eeffb8d6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cceb1c5b4d3ebf707029cbbf1911ad3c9d242086e6d5100ac88fb907b63b02(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b50488ab753f1816da7d658f4f1d27941173bc84c56a8204ebcc554af37043(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a42b4a8c9a2a7357f319dde66f8cec5690b69c33554fc9176cf9d37623ba8c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0738c72f1858464d7f949ec7bbf6eaff48500a9a3798e5a081c3a6f0f84a82a(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99535d11a7a1a8cdddfe7c61de3cafa9dc4af5f409d6ef90c544d4618f3ab78c(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    instance_tag: builtins.str,
    metrics_environment_label: builtins.str,
    queue_name: builtins.str,
    randomize_resource_names: builtins.bool,
    sourcegraph_executor_proxy_password: builtins.str,
    sourcegraph_external_url: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    boot_disk_iops: typing.Optional[jsii.Number] = None,
    boot_disk_size: typing.Optional[jsii.Number] = None,
    boot_disk_throughput: typing.Optional[jsii.Number] = None,
    docker_auth_config: typing.Optional[builtins.str] = None,
    docker_registry_mirror: typing.Optional[builtins.str] = None,
    docker_registry_mirror_node_exporter_url: typing.Optional[builtins.str] = None,
    firecracker_disk_space: typing.Optional[builtins.str] = None,
    firecracker_memory: typing.Optional[builtins.str] = None,
    firecracker_num_cpus: typing.Optional[jsii.Number] = None,
    http_access_cidr_range: typing.Optional[builtins.str] = None,
    job_memory: typing.Optional[builtins.str] = None,
    job_num_cpus: typing.Optional[jsii.Number] = None,
    jobs_per_instance_scaling: typing.Optional[jsii.Number] = None,
    machine_image: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_active_time: typing.Optional[builtins.str] = None,
    maximum_num_jobs: typing.Optional[jsii.Number] = None,
    maximum_runtime_per_job: typing.Optional[builtins.str] = None,
    max_replicas: typing.Optional[jsii.Number] = None,
    metrics_access_security_group_id: typing.Optional[builtins.str] = None,
    min_replicas: typing.Optional[jsii.Number] = None,
    num_total_jobs: typing.Optional[jsii.Number] = None,
    permissions_boundary_arn: typing.Optional[builtins.str] = None,
    preemptible_machines: typing.Optional[builtins.bool] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
    ssh_access_cidr_range: typing.Optional[builtins.str] = None,
    use_firecracker: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80b20b4ada2720173c646021f5b2745643f4356f093ee4ab657ed10102c259b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zone: builtins.str,
    randomize_resource_names: builtins.bool,
    nat: typing.Optional[builtins.bool] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821bc2c55aeff422ebd73598a10423931a3f270cb2d73532b3506badb2a88d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f043e04d1572edde9496b87241f08f2e43d2addc643b5231506a15695a0bfe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31c8e76ff9a7f9ffda1920c7cb6cc133cab57f3b232d5f288603ee1752dee75(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6600427918c7196da16f88e8c325d447ce7c8fad5d0d2e1ca2eda5eb7ee1bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eccaeadd18edb5384c886b8492680582d86cda677bcb2eb73ebbd3d3c26408(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    availability_zone: builtins.str,
    randomize_resource_names: builtins.bool,
    nat: typing.Optional[builtins.bool] = None,
    resource_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
