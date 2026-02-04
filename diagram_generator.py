# terraform_documenter/diagram_generator.py

from diagrams import Diagram, Cluster
from typing import Dict, Any

def create_conceptual_diagram(data: Dict, provider: str, output_filename: str) -> str:
    """
    Generates a DYNAMIC conceptual diagram by drawing all major components found.
    """
    title = f"Conceptual Architecture ({provider.upper()})"
    graph_attr = {"pad": "0.5", "margin": "0.5", "nodesep": "1.0", "ranksep": "1.5"}
    
    try:
        with Diagram(title, show=False, filename=output_filename, outformat="png", graph_attr=graph_attr):
            resources = data.get("resources", {})
            
            # --- AMAZON WEB SERVICES (AWS) ---
            if provider == "aws":
                from diagrams.aws.compute import EC2, EKS, Lambda
                from diagrams.aws.database import RDS, Dynamodb, ElastiCache
                from diagrams.aws.network import Route53, CloudFront, ELB, APIGateway
                from diagrams.aws.storage import S3, EBS, EFS
                from diagrams.aws.security import ACM, IAM
                from diagrams.aws.integration import SQS
                
                with Cluster("AWS Account"):
                    with Cluster("Region"):
                        # Networking
                        with Cluster("Networking"):
                            lb_nodes = [ELB(lb.get("name", "elb")) for lb in resources.get("alb", []) + resources.get("nlb", [])]
                            cf_nodes = [CloudFront(cf.get("name", "cloudfront")) for cf in resources.get("cloudfront", [])]
                            route53_nodes = [Route53(r53.get("name", "route53")) for r53 in resources.get("route53", [])]
                        
                        # Compute
                        with Cluster("Compute"):
                            instance_nodes = [EC2(inst.get("name", "instance")) for inst in resources.get("instances", [])]
                            eks_nodes = [EKS(cluster.get("name", "eks-cluster")) for cluster in resources.get("eks", [])]
                        
                        # Serverless
                        with Cluster("Serverless"):
                            lambda_nodes = [Lambda(func.get("name", "lambda")) for func in resources.get("lambda", [])]
                            apigw_nodes = [APIGateway(gw.get("name", "api-gateway")) for gw in resources.get("apigateway", [])]

                        # Database
                        with Cluster("Database"):
                            db_nodes = [RDS(db.get("name", "database")) for db in resources.get("rds", [])]
                            dynamodb_nodes = [Dynamodb(table.get("name", "dynamodb")) for table in resources.get("dynamodb", [])]
                            elasticache_nodes = [ElastiCache(cluster.get("name", "elasticache")) for cluster in resources.get("elasticache", [])]
                        
                        # Storage
                        with Cluster("Storage"):
                            s3_nodes = [S3(b.get("config", {}).get("bucket", [b.get("name")])[0]) for b in resources.get("s3", [])]
                            efs_nodes = [EFS(fs.get("name", "efs")) for fs in resources.get("efs", [])]

                        # Security
                        with Cluster("Security"):
                            acm_nodes = [ACM(acm.get("name", "acm")) for acm in resources.get("acm", [])]
                            iam_nodes = [IAM(role.get("name", "iam-role")) for role in resources.get("iam_roles", [])]
                        
                        # Integration
                        with Cluster("Application Integration"):
                            sqs_nodes = [SQS(queue.get("name", "sqs")) for queue in resources.get("sqs", [])]

                # Connections
                if route53_nodes:
                    if cf_nodes: route53_nodes[0] >> cf_nodes
                    elif lb_nodes: route53_nodes[0] >> lb_nodes

                if cf_nodes:
                    if lb_nodes: cf_nodes[0] >> lb_nodes
                    if s3_nodes: cf_nodes[0] >> s3_nodes
                
                if acm_nodes:
                    if cf_nodes: acm_nodes[0] >> cf_nodes
                    if lb_nodes: acm_nodes[0] >> lb_nodes

                if lb_nodes:
                    if instance_nodes: lb_nodes[0] >> instance_nodes
                    if eks_nodes: lb_nodes[0] >> eks_nodes
                
                if apigw_nodes and lambda_nodes: apigw_nodes[0] >> lambda_nodes

                compute_nodes = instance_nodes + eks_nodes
                database_nodes = db_nodes + dynamodb_nodes + elasticache_nodes
                
                if compute_nodes and database_nodes: compute_nodes[0] >> database_nodes
                if compute_nodes and s3_nodes: compute_nodes[0] >> s3_nodes
                if compute_nodes and efs_nodes: compute_nodes[0] >> efs_nodes
                if lambda_nodes and database_nodes: lambda_nodes[0] >> database_nodes

            # --- GOOGLE CLOUD (GCP) ---
            elif provider == "google":
                from diagrams.gcp.compute import GCE, GKE, GCF
                from diagrams.gcp.database import SQL, Datastore, Memorystore
                from diagrams.gcp.network import VPC, DNS, LoadBalancing
                from diagrams.gcp.storage import GCS
                from diagrams.generic.blank import Blank
                
                with Cluster("GCP Project"):
                    with Cluster("Networking"):
                        dns_nodes = [DNS(zone.get("name", "dns")) for zone in resources.get("dns", [])]
                        lb_nodes = [LoadBalancing(lb.get("name", "lb")) for lb in resources.get("load_balancing", [])]

                    with Cluster("Compute"):
                        instance_nodes = [GCE(inst.get("name", "instance")) for inst in resources.get("instances", [])]
                        gke_nodes = [GKE(gke.get("name", "gke-cluster")) for gke in resources.get("gke", [])]
                        function_nodes = [GCF(f.get("name", "function")) for f in resources.get("functions", [])]
                    
                    with Cluster("Database"):
                        db_nodes = [SQL(db.get("name", "sql-db")) for db in resources.get("sql", [])]
                        firestore_nodes = [Datastore(db.get("name", "firestore")) for db in resources.get("firestore", [])]
                        redis_nodes = [Memorystore(r.get("name", "redis")) for r in resources.get("memorystore", [])]

                    with Cluster("Storage"):
                        bucket_nodes = [GCS(b.get("name", "bucket")) for b in resources.get("storage_buckets", [])]
                    
                    with Cluster("IAM"):
                        iam_nodes = [Blank(role.get("name", "iam-role")) for role in resources.get("iam_roles", [])]

                    # Establish logical connections
                    compute_nodes = instance_nodes + gke_nodes + function_nodes
                    database_nodes = db_nodes + firestore_nodes + redis_nodes

                    if dns_nodes and lb_nodes: dns_nodes[0] >> lb_nodes
                    if lb_nodes and compute_nodes: lb_nodes[0] >> compute_nodes
                    if compute_nodes and database_nodes: compute_nodes[0] >> database_nodes
                    if compute_nodes and bucket_nodes: compute_nodes[0] >> bucket_nodes
            else:
                from diagrams.generic.blank import Blank
                Blank(f"Diagrams for {provider.upper()} not implemented.")

    except Exception as e:
        print(f"DEBUG: Could not generate conceptual diagram. Error: {e}")
        with Diagram(show=False, filename=output_filename, outformat="png"):
             from diagrams.generic.blank import Blank
             Blank(f"Error: {e}")
            
    return f"{output_filename}.png"


def create_networking_diagram(data: Dict, provider: str, output_filename: str) -> str:
    """
    Generates a DYNAMIC networking diagram by drawing all networking components found
    and placing them in their correct VPC and Subnet.
    """
    title = f"Networking and Security ({provider.upper()})"
    graph_attr = {"pad": "1.0", "margin": "1.0", "splines": "ortho"}

    try:
        with Diagram(title, show=False, filename=output_filename, outformat="png", graph_attr=graph_attr):
            resources = data.get("resources", {})

            if provider == "aws":
                from diagrams.aws.compute import EC2
                from diagrams.aws.network import VPC, InternetGateway, NATGateway, RouteTable
                from diagrams.aws.security import WAF
                
                vpcs = resources.get("vpcs", [])
                subnets = resources.get("subnets", [])
                igws = resources.get("internet_gateways", [])
                nats = resources.get("nat_gateways", [])
                route_tables = resources.get("route_tables", [])
                nacls = resources.get("nacl", [])
                instances = resources.get("instances", [])

                if not vpcs:
                    VPC("No VPC found.")
                else:
                    # Create IGW node outside the VPC context, as is architecturally correct
                    igw_node = InternetGateway(igws[0]['name']) if igws else None

                    for vpc in vpcs:
                        vpc_name = vpc['name']
                        
                        # Start the VPC Cluster context
                        with Cluster(f"VPC: {vpc_name}") as vpc_cluster:
                            # --- 1. Find all resources belonging to this VPC ---
                            vpc_subnets = [s for s in subnets if vpc_name in s.get("config", {}).get("vpc_id", [""])[0]]
                            vpc_rts = [rt for rt in route_tables if vpc_name in rt.get("config", {}).get("vpc_id", [""])[0]]
                            vpc_nacls = [n for n in nacls if vpc_name in n.get("config", {}).get("vpc_id", [""])[0]]
                            
                            # --- 2. Create nodes within the VPC but outside of subnets ---
                            # Use naming conventions to identify public and private route tables
                            public_rt_data = next((rt for rt in vpc_rts if 'public' in rt['name'].lower()), None)
                            private_rt_data = next((rt for rt in vpc_rts if 'private' in rt['name'].lower()), None)
                            public_rt_node = RouteTable(public_rt_data['name']) if public_rt_data else None
                            private_rt_node = RouteTable(private_rt_data['name']) if private_rt_data else None

                            if vpc_nacls:
                                WAF(vpc_nacls[0]['name']) # Draw NACL inside VPC

                            # --- 3. Create Subnet Clusters and place resources inside them ---
                            nat_node = None # Hold the NAT gateway node
                            
                            with Cluster("Public Subnets", graph_attr={"bgcolor": "lightblue"}):
                                for subnet_data in [s for s in vpc_subnets if 'public' in s['name'].lower()]:
                                    with Cluster(f"Subnet: {subnet_data['name']}"):
                                        # Place EC2 instances that belong to this subnet
                                        [EC2(i['name']) for i in instances if subnet_data['name'] in i.get("config", {}).get("subnet_id", [""])[0]]
                                        # Place NAT Gateway if it belongs to this subnet
                                        nat_data = next((nat for nat in nats if subnet_data['name'] in nat.get("config", {}).get("subnet_id", [""])[0]), None)
                                        if nat_data:
                                            nat_node = NATGateway(nat_data['name'])
                            
                            with Cluster("Private Subnets", graph_attr={"bgcolor": "lightgrey"}):
                                for subnet_data in [s for s in vpc_subnets if 'private' in s['name'].lower()]:
                                    with Cluster(f"Subnet: {subnet_data['name']}"):
                                        # Place EC2 instances that belong to this subnet
                                        [EC2(i['name']) for i in instances if subnet_data['name'] in i.get("config", {}).get("subnet_id", [""])[0]]

                            # --- 4. Draw relationships at the end, now that all nodes exist ---
                            if igw_node and public_rt_node:
                                igw_node >> public_rt_node
                            
                            if private_rt_node and nat_node:
                                private_rt_node >> nat_node
                            
                            if nat_node and igw_node:
                                nat_node >> igw_node # Egress traffic from NAT goes to IGW


            elif provider == "google":
                from diagrams.gcp.compute import GCE, GKE
                from diagrams.gcp.network import VPC, Router, FirewallRules, NAT, VPN
                
                networks = resources.get("networks", [])
                subnets = resources.get("subnets", [])
                instances = resources.get("instances", [])
                gke_clusters = resources.get("gke", [])
                routers = resources.get("routers", [])
                firewalls = resources.get("firewall", [])
                nats = resources.get("nat", [])
                vpns = resources.get("vpn", [])
                
                if not networks:
                    VPC("No VPC/Network found.")
                else:
                    firewall_nodes = [FirewallRules(fw.get("name", "firewall-rule")) for fw in firewalls]
                    
                    for network in networks:
                        network_name = network.get("name", "default-vpc")
                        with Cluster(f"VPC: {network_name}"):
                            router_nodes_in_vpc = [Router(r.get("name", "router")) for r in routers if r.get("config",{}).get("network", [""])[0].endswith(network_name)]
                            
                            if router_nodes_in_vpc:
                                nat_nodes = [NAT(n.get("name", "nat")) for n in nats]
                                vpn_nodes = [VPN(v.get("name", "vpn")) for v in vpns]
                                if nat_nodes: router_nodes_in_vpc[0] >> nat_nodes
                                if vpn_nodes: router_nodes_in_vpc[0] >> vpn_nodes

                            network_subnets = [s for s in subnets if s.get("config", {}).get("network", [""])[0].endswith(network_name)]
                            for subnet in network_subnets:
                                with Cluster(f"Subnet: {subnet.get('name', 'subnet')}"):
                                    compute_in_subnet = []
                                    subnet_instances = [GCE(i.get("name", "instance")) for i in instances if i.get("config",{}).get("network_interface",[{}])[0].get("subnetwork","").endswith(subnet.get("name",""))]
                                    compute_in_subnet.extend(subnet_instances)
                                    subnet_gke = [GKE(g.get("name", "gke-cluster")) for g in gke_clusters if g.get("config",{}).get("network",[""])[0].endswith(network_name) and g.get("config",{}).get("subnetwork",[""])[0].endswith(subnet.get("name",""))]
                                    compute_in_subnet.extend(subnet_gke)

                    if firewall_nodes and networks:
                         firewall_nodes[0] >> VPC(networks[0].get("name", "default-vpc"))

            else:
                from diagrams.generic.blank import Blank
                Blank(f"Diagrams for {provider.upper()} not implemented.")

    except Exception as e:
        print(f"DEBUG: Could not generate networking diagram. Error: {e}")
        with Diagram(show=False, filename=output_filename, outformat="png"):
             from diagrams.generic.blank import Blank
             Blank(f"Error: {e}")
            
    return f"{output_filename}.png"