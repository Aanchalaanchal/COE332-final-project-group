kube-get_all:
	@echo ""
	@echo "------------GETTING ALL K8S TYPES------------"
	@echo ""
	kubectl get pods
	@echo ""
	kubectl get deployments
	@echo ""
	kubectl get services
	@echo ""
	kubectl get pvc
	@echo ""

kube-init: kube-apply_other kube-apply_deployments
kube-restart_deployments: kube-delete_deployments kube-apply_deployments

kube-delete_deployments:
	kubectl delete deployments final-api-deployment-test final-db-deployment-test final-debug-deployment-test
	kubectl delete deployments final-worker-deployment-test final-worker2-deployment-test

kube-apply_deployments:
	kubectl apply -f ./kubernetes/test/db-deployment.yml
	kubectl apply -f ./kubernetes/test/api-deployment.yml
	kubectl apply -f ./kubernetes/test/worker-deployment.yml
	kubectl apply -f ./kubernetes/test/worker2-deployment.yml
	kubectl apply -f ./kubernetes/test/debug-deployment.yml

kube-apply_other:
	kubectl apply -f ./kubernetes/test/api-service.yml
	kubectl apply -f ./kubernetes/test/db-pvc.yml
	kubectl apply -f ./kubernetes/test/db-service.yml

docker-build:
	docker build -t kdnguyen205/coe332-final:1.0 -f ./docker/Dockerfile ./source
	docker push kdnguyen205/coe332-final:1.0
