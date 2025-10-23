output "ecs_cluster_id" {
  value = aws_ecs_cluster.diet_app.id
}
output "frontend_service_name" {
  value = aws_ecs_service.frontend_service.name
}
output "backend_service_name" {
  value = aws_ecs_service.backend_service.name
}
