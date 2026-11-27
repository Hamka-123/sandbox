# Миграция Stateful-приложения с использованием Velero и Azure

Инструкция по полному циклу миграции Stateful-приложения из локального
кластера Minikube в облачный кластер AKS с использованием Velero и Azure
Blob Storage.

------------------------------------------------------------------------

## 1. Установка локальных инструментов

Если утилиты еще не установлены на вашем компьютере, установите их
(например, через Homebrew на macOS):

``` bash
brew install minikube velero kubectl terraform azure-cli
```

## 2. Авторизация в Azure

Перед началом работы с облаком авторизуйтесь в своей учетной записи
Azure:

``` bash
az login
```

Команда откроет браузер для входа в учетную запись.

## 3. Запуск и настройка локального кластера (Minikube)

Запустите локальный кластер с необходимыми аддонами для поддержки
постоянных томов и снимков томов:

``` bash
minikube start --addons=csi-hostpath-driver,volumesnapshots --driver=docker
```

Проверьте статус кластера:

``` bash
minikube status
kubectl cluster-info --context minikube
```

## 4. Развертывание инфраструктуры через Terraform

Перейдите в директорию с Terraform-конфигурацией:

``` bash
cd velero-aks
```

Инициализируйте Terraform и разверните инфраструктуру:

``` bash
terraform init
terraform apply
```

Убедитесь, что в `terraform.tfvars` корректно указаны ваши параметры,
включая `owner`.

## 5. Применение манифестов приложения в Minikube

Примените манифесты приложения (Namespace, ConfigMap, Deployment,
Service и PVC) в кластере Minikube.

Если манифесты находятся в отдельной директории `manifests/`:

``` bash
kubectl apply -f ../k8s/ --context minikube
```

Или примените файлы по отдельности:

``` bash
# kubectl apply -f namespace.yaml -f configmap.yaml -f deployment.yaml -f service.yaml -f pvc.yaml --context minikube
```

## 6. Установка и проверка Velero в Minikube

Установите Velero с помощью команды, сформированной из Terraform output:

``` bash
$(terraform output -raw velero_install_minikube)
```

Проверьте статус хранилища резервных копий. Ожидаемый статус ---
`Available`:

``` bash
velero backup-location get --kubecontext minikube
```

## 7. Создание резервной копии в Minikube

Создайте резервную копию namespace `migration`:

``` bash
velero backup create migration-backup --include-namespaces migration --kubecontext minikube
```

Убедитесь, что резервная копия содержит необходимые ресурсы и данные
томов:

``` bash
velero backup describe migration-backup --details --kubecontext minikube
```

## 8. Развертывание в AKS и восстановление

Получите учетные данные для подключения к AKS:

``` bash
$(terraform output -raw aks_get_credentials)
```

Установите Velero в кластер AKS:

``` bash
$(terraform output -raw velero_install_aks)
```

Восстановите приложение из резервной копии, созданной в Minikube.

``` bash
velero restore create --from-backup migration-backup --kubecontext $(terraform output -raw kubecontext_aks)
```

## 9. Проверка результатов миграции

### Проверка статуса восстановления

Замените `<restore_name>` именем созданного восстановления:

``` bash
velero restore describe <restore_name> --kubecontext aks-<owner>
```

### Проверка подов и сервисов в AKS

``` bash
kubectl get all -n migration --context aks-<owner>
```

### Проверка данных на постоянном томе

Дата должна совпадать с датой, записанной в Minikube до создания
резервной копии:

``` bash
kubectl exec -it deployment/hellogo-deployment -n migration --context aks-<owner> -- cat /data/date.txt
```

### Проверка веб-интерфейса

Запустите перенаправление порта сервиса:

``` bash
kubectl port-forward svc/hellogo-service 8080:80 -n migration --context aks-<owner>
```

Откройте <http://localhost:8080> в браузере и проверьте, что
отображается приветственное сообщение.

## 10. Полная очистка стенда

После завершения работы удалите созданные ресурсы, чтобы избежать лишних
расходов.

Удалите Velero из Minikube:

``` bash
velero uninstall --kubecontext minikube --force
```

Удалите namespace `migration` из Minikube:

``` bash
kubectl --context minikube delete namespace migration
```

Удалите облачную инфраструктуру с помощью Terraform:

``` bash
cd velero-aks
terraform destroy
```

Удалите контекст AKS из `kubeconfig`:

``` bash
kubectl config delete-context aks-velero-alina
```

Проверьте, что группа ресурсов Azure удалена. Ожидаемый результат ---
`false`:

``` bash
az group exists --name rg-velero-alina
```
