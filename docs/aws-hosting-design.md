

\# Hotel AI Copilot — AWS Hosting Design



\## Goal



Deploy our Dockerized FastAPI application securely

to AWS while keeping costs low.



AWS Region: ap-southeast-2 (Sydney)



\## Proposed Architecture



User / Browser

&#x20;     |

&#x20;     v

Amazon API Gateway (HTTPS)

&#x20;     |

&#x20;     v

AWS Lambda

(FastAPI + Lambda Web Adapter)

&#x20;     |

&#x20;     +----> FAQ Knowledge Base

&#x20;     |

&#x20;     +----> Semantic Retrieval (FastEmbed)

&#x20;     |

&#x20;     +----> Amazon Bedrock (optional)



Supporting Services:



\- Amazon ECR: Stores the application Docker image

\- CloudWatch: Logs, metrics, and alarms

\- IAM: Controls access to AWS services

\- Terraform: Manages infrastructure



\## Deployment Strategy



Stage 1:

Deploy the FAQ API without live AI.



Stage 2:

Test semantic retrieval memory usage and startup time.



Stage 3:

Enable Bedrock using restricted IAM permissions.



Stage 4:

Test the browser chat interface and monitoring.



\## Security Requirements



\- Keep ENABLE\_LIVE\_RAG=false by default.

\- Keep ENABLE\_DEMO\_RAG=false by default.

\- Do not store AWS credentials in Docker images.

\- Use least-privilege IAM roles.

\- Limit public access and protect expensive endpoints.

\- Validate incoming requests.

\- Keep logs free of sensitive information.



\## Cost Controls



\- Use on-demand execution instead of an

&#x20; always-running server where practical.

\- Configure AWS Budget alerts.

\- Monitor Lambda, API Gateway, ECR, Bedrock,

&#x20; and CloudWatch charges.

\- Avoid creating unnecessary NAT Gateways.

\- Remove unused test deployments.



\## Technical Risks



\- FastEmbed requires ONNX Runtime.

\- The embedding model may need downloading.

\- Cold starts could be slow.

\- Lambda memory or image size could be limiting.

\- Public endpoints require abuse protection.



\## Decision



Start with a Lambda feasibility test.



If startup time, memory, or dependency packaging

makes Lambda unsuitable, evaluate ECS Fargate.



No infrastructure deployment is authorized

by this design document.
