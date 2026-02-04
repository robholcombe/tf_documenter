# terraform_documenter/utils.py

# Mapping from Terraform provider name to a display-friendly name
PROVIDER_DISPLAY_NAMES = {
    "aws": "AWS",
    "azurerm": "Azure",
    "google": "Google Cloud Platform"
}

# Mapping of Terraform resource types to our internal data structure categories for each provider
# This is the core mapping that drives the information extraction.
RESOURCE_MAP = {
    "aws": {
        # Networking
        "vpcs": ["aws_vpc"],
        "subnets": ["aws_subnet"],
        "route_tables": ["aws_route_table", "aws_route"],
        "internet_gateways": ["aws_internet_gateway"],
        "nat_gateways": ["aws_nat_gateway"],
        "vpn_gateways": ["aws_vpn_gateway"],
        "peering_connections": ["aws_vpc_peering_connection"],
        "endpoints": ["aws_vpc_endpoint"],
        "alb": ["aws_lb", "aws_alb"],
        "nlb": ["aws_network_load_balancer"],
        "target_groups": ["aws_lb_target_group", "aws_alb_target_group"],
        "listeners": ["aws_lb_listener", "aws_alb_listener"],
        "route53": ["aws_route53_zone", "aws_route53_record"],
        "cloudfront": ["aws_cloudfront_distribution"],
        "apigateway": ["aws_api_gateway_rest_api", "aws_api_gateway_v2_api"],
        "transit_gateways": ["aws_transit_gateway"],

        # Compute
        "instances": ["aws_instance"],
        "asg": ["aws_autoscaling_group"],
        "launch_templates": ["aws_launch_template"],

        # Containers
        "eks": ["aws_eks_cluster", "aws_eks_node_group", "aws_eks_fargate_profile"],
        "ecs": ["aws_ecs_cluster", "aws_ecs_service", "aws_ecs_task_definition"],
        "ecr": ["aws_ecr_repository"],

        # Serverless
        "lambda": ["aws_lambda_function"],
        "sqs": ["aws_sqs_queue"],
        "sns": ["aws_sns_topic"],
        "eventbridge": ["aws_cloudwatch_event_rule", "aws_cloudwatch_event_target"],
        
        # Storage
        "s3": ["aws_s3_bucket", "aws_s3_bucket_policy"],
        "ebs": ["aws_ebs_volume"],
        "efs": ["aws_efs_file_system"],
        "glacier": ["aws_glacier_vault"],

        # Databases
        "rds": ["aws_db_instance", "aws_db_subnet_group"],
        "aurora": ["aws_rds_cluster"],
        "dynamodb": ["aws_dynamodb_table"],
        "elasticache": ["aws_elasticache_cluster", "aws_elasticache_subnet_group"],
        "neptune": ["aws_neptune_cluster"],
        "documentdb": ["aws_docdb_cluster"],

        # Security & Identity
        "iam_roles": ["aws_iam_role"],
        "iam_policies": ["aws_iam_policy", "aws_iam_role_policy_attachment"],
        "iam_users": ["aws_iam_user"],
        "security_groups": ["aws_security_group", "aws_security_group_rule"],
        "nacl": ["aws_network_acl", "aws_network_acl_rule"],
        "kms": ["aws_kms_key"],
        "acm": ["aws_acm_certificate"],
        "secretsmanager": ["aws_secretsmanager_secret"],
        "waf": ["aws_wafv2_web_acl"],

        # Analytics
        "redshift": ["aws_redshift_cluster"],
        "emr": ["aws_emr_cluster"],
        "glue": ["aws_glue_catalog_database", "aws_glue_job"],
        "kinesis": ["aws_kinesis_stream"],
        "athena": ["aws_athena_database", "aws_athena_workgroup"],
        
        # Management & Monitoring
        "cloudwatch": ["aws_cloudwatch_metric_alarm", "aws_cloudwatch_dashboard"],
        "cloudtrail": ["aws_cloudtrail"],
        "config": ["aws_config_config_rule"],
    },
    "azurerm": {
        # Networking
        "vnets": ["azurerm_virtual_network"],
        "subnets": ["azurerm_subnet"],
        "route_tables": ["azurerm_route_table"],
        "nat_gateways": ["azurerm_nat_gateway"],
        "vpn_gateways": ["azurerm_virtual_network_gateway"],
        "app_gateway": ["azurerm_application_gateway"],
        "load_balancer": ["azurerm_lb", "azurerm_lb_backend_address_pool"],
        "dns": ["azurerm_dns_zone", "azurerm_private_dns_zone"],
        "firewall": ["azurerm_firewall"],
        "public_ip": ["azurerm_public_ip"],
        "network_interfaces": ["azurerm_network_interface"],

        # Compute
        "vms": ["azurerm_virtual_machine", "azurerm_linux_virtual_machine", "azurerm_windows_virtual_machine"],
        "vmss": ["azurerm_virtual_machine_scale_set"],
        
        # Containers
        "aks": ["azurerm_kubernetes_cluster"],
        "acr": ["azurerm_container_registry"],
        "aci": ["azurerm_container_group"],

        # Serverless
        "functions": ["azurerm_function_app", "azurerm_windows_function_app", "azurerm_linux_function_app"],
        "eventgrid": ["azurerm_eventgrid_topic"],
        "servicebus": ["azurerm_servicebus_namespace"],
        "logic_apps": ["azurerm_logic_app_workflow"],

        # Storage
        "storage_accounts": ["azurerm_storage_account"],
        "storage_containers": ["azurerm_storage_container"],
        "managed_disks": ["azurerm_managed_disk"],

        # Databases
        "sql_db": ["azurerm_sql_database", "azurerm_mssql_database"],
        "sql_server": ["azurerm_sql_server", "azurerm_mssql_server"],
        "cosmosdb": ["azurerm_cosmosdb_account"],
        "redis": ["azurerm_redis_cache"],
        "postgresql": ["azurerm_postgresql_server"],
        "mysql": ["azurerm_mysql_server"],

        # Security & Identity
        "key_vault": ["azurerm_key_vault", "azurerm_key_vault_secret"],
        "nsgs": ["azurerm_network_security_group", "azurerm_network_security_rule"],
        "managed_identity": ["azurerm_user_assigned_identity"],
        
        # Monitoring
        "monitor": ["azurerm_monitor_metric_alert", "azurerm_log_analytics_workspace"],

        # AI & ML
        "machine_learning": ["azurerm_machine_learning_workspace"],
        "cognitive_services": ["azurerm_cognitive_account"],
    },
    "google": {
        # Networking
        "networks": ["google_compute_network"],
        "subnets": ["google_compute_subnetwork"],
        "routes": ["google_compute_route"],
        "routers": ["google_compute_router"],
        "nat": ["google_compute_router_nat"],
        "vpn": ["google_compute_vpn_gateway"],
        "firewall": ["google_compute_firewall"],
        "load_balancing": ["google_compute_forwarding_rule", "google_compute_global_forwarding_rule", "google_compute_backend_service"],
        "dns": ["google_dns_managed_zone", "google_dns_record_set"],
        "cloud_armor": ["google_compute_security_policy"],

        # Compute
        "instances": ["google_compute_instance", "google_workbench_instance"],
        "instance_groups": ["google_compute_instance_group_manager"],
        "instance_templates": ["google_compute_instance_template"],

        # Containers
        "gke": ["google_container_cluster", "google_container_node_pool"],
        "artifact_registry": ["google_artifact_registry_repository"],
        
        # Serverless
        "functions": ["google_cloudfunctions_function", "google_cloudfunctions2_function"],
        "cloud_run": ["google_cloud_run_v2_service"],
        "pubsub": ["google_pubsub_topic", "google_pubsub_subscription"],
        "workflows": ["google_workflows_workflow"],

        # Storage
        "storage_buckets": ["google_storage_bucket", "google_storage_bucket_iam_binding"],
        "disks": ["google_compute_disk"],
        "filestore": ["google_filestore_instance"],

        # Databases
        "sql": ["google_sql_database_instance"],
        "spanner": ["google_spanner_instance"],
        "bigtable": ["google_bigtable_instance"],
        "firestore": ["google_firestore_database", "google_firestore_document"],
        "memorystore": ["google_redis_instance"],

        # Security & Identity
        "iam_roles": ["google_service_account", "google_project_iam_binding", "google_project_iam_member"],
        "kms": ["google_kms_key_ring", "google_kms_crypto_key"],
        "secret_manager": ["google_secret_manager_secret", "google_secret_manager_secret_version"],
        
        # Analytics & Big Data
        "bigquery": ["google_bigquery_dataset", "google_bigquery_table"],
        "dataproc": ["google_dataproc_cluster"],
        "dataflow": ["google_dataflow_job"],
        "composer": ["google_composer_environment"],
        
        # AI & ML
        "vertex_ai": ["google_vertex_ai_dataset", "google_vertex_ai_endpoint"],
        "notebooks": ["google_notebooks_instance"],
    }
}