## Dockerfile

```Dockerfile
FROM node:16 as builder

WORKDIR /build
COPY web/package.json .
RUN npm install
COPY ./web .
COPY ./VERSION .
RUN DISABLE_ESLINT_PLUGIN='true' VITE_REACT_APP_VERSION=$(cat VERSION) npm run build

FROM golang AS builder2

ENV GO111MODULE=on \
    CGO_ENABLED=1 \
    GOOS=linux

WORKDIR /build
ADD go.mod go.sum ./
RUN go mod download
COPY . .
COPY --from=builder /build/dist ./web/dist
RUN go build -ldflags "-s -w -X 'one-api/common.Version=$(cat VERSION)' -extldflags '-static'" -o one-api

FROM alpine

RUN apk update \
    && apk upgrade \
    && apk add --no-cache ca-certificates tzdata \
    && update-ca-certificates 2>/dev/null || true

COPY --from=builder2 /build/one-api /
EXPOSE 3000
WORKDIR /data
ENTRYPOINT ["/one-api"]
```


## Dockerfile 解析

这个 Dockerfile 通过多个阶段构建一个含前端和后端组件的应用。每个阶段使用不同的基础镜像和步骤来完成特定的任务。

### 第一阶段：前端构建（Node.js）

- **基础镜像**:
  - `FROM node:16 as builder`：使用 Node.js 16 版本的官方镜像作为基础镜像，并标记此构建阶段为 `builder`。
- **设置工作目录**:
  - `WORKDIR /build`：将工作目录设置为 `/build`。
- **复制文件**:
  - `COPY web/package.json .`：将前端代码目录下的 `package.json` 文件复制到工作目录中。
- **安装依赖**:
  - `RUN npm install`：根据 `package.json` 安装所需依赖。
- **复制前端代码和版本文件**:
  - `COPY ./web .`：将web文件夹下所有文件复制到工作目录。
  - `COPY ./VERSION .`：将项目版本文件复制到工作目录。
- **构建前端项目**:
  - `RUN DISABLE_ESLINT_PLUGIN='true' VITE_REACT_APP_VERSION=$(cat VERSION) npm run build`：设置环境变量并执行前端构建脚本，生成生产环境用的前端文件。

### 第二阶段：后端构建（Go）

- **基础镜像**:
  - `FROM golang AS builder2`：使用 Go 的官方镜像作为基础，并标记此阶段为 `builder2`。
- **环境变量**:
  - 设置多个环境变量，以支持 Go 的模块系统和确保生成的是适用于 Linux 的静态链接二进制文件。
- **设置工作目录**:
  - `WORKDIR /build`：设置工作目录。
- **添加 Go 模块文件**:
  - `ADD go.mod go.sum ./`：添加 Go 模块定义文件。
- **下载依赖**:
  - `RUN go mod download`：下载 Go 依赖。
- **复制代码和前端构建产物**:
  - `COPY . .`：复制所有后端代码到工作目录。
  - `COPY --from=builder /build/dist ./web/dist`：从第一阶段中复制构建好的前端文件到后端服务目录中。
- **编译应用**:
  - `RUN go build -ldflags "-s -w -X 'one-api/common.Version=$(cat VERSION)' -extldflags '-static'" -o one-api`：使用 Go 编译命令构建应用，设置链接器选项以嵌入版本信息并优化二进制大小。

### 第三阶段：运行环境

- **基础镜像**:
  - `FROM alpine`：使用轻量级的 Alpine Linux 镜像作为基础。
- **安装证书和时区数据**:
  - 运行一系列命令以安装必要的证书和时区数据，确保应用可以处理 HTTPS 连接和正确的时间。
- **复制编译好的应用**:
  - `COPY --from=builder2 /build/one-api /`：从第二阶段复制编译好的应用到根目录。
- **端口和工作目录**:
  - `EXPOSE 3000`：声明容器在运行时会监听 3000 端口。
  - `WORKDIR /data`：设置工作目录，应用可能会使用此目录来存储数据。
- **设置入口点**:
  - `ENTRYPOINT ["/one-api"]`：设置容器启动时执行的命令。

### 总结

此 Dockerfile 首先构建前端资源，然后构建后端服务，并将前端资源集成到后端服务中，最后在一个轻量级容器中运行编译好的二进制文件，实现前后端的自动化构建和部署。
