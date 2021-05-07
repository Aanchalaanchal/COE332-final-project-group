
# build all image
# start up new containers / services
# Removes running containers

kube-apply_all-test:
	@echo ""
	@echo "------------APPLY ALL K8S YAML FILES------------"
	@echo ""
	kubectl apply -f ./kubernetes/test/api-deployment.yml
	@echo ""
	kubectl apply -f ./kubernetes/test/api-service.yml
	@echo ""
	kubectl apply -f ./kubernetes/test/db-pvc.yml
	@echo ""
	kubectl apply -f ./kubernetes/test/db-deployment.yml
	@echo ""
	kubectl apply -f ./kubernetes/test/db-service.yml
	@echo ""

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

kube-clear_all-test:
	kubectl delete deployments final-api-deployment-test final-db-deployment-test
	kubectl delete services final-api-service-test final-db-service-test
	kubectl delete pvc final-db-pvc-test

docker-build:
	docker build -t kdnguyen205/coe332-final:1.0 -f ./docker/Dockerfile ./source
	docker push kdnguyen205/coe332-final:1.0
