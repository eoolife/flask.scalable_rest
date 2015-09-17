# 基于Flask、Flask-Restufl上的快速构建Restful风格API的小项目

该项目能让你基于Flask与Flask-Restful之上构建一个良好Restful风格的API，让你快速构建一个能用于生产中的API，并提供良好的Metrics!

## 项目的特性

* 基于Flask/Flask-Restful
* ORM使用SQLAlchemy
* 具有metrics功能，可以方便通过decorator的方式让你随心监控某些API的运行指标
* 可部署在兼容uwsgi协议上的容器中，例如uwsgi与gevent之上，获取更高的性能
* 基于JWT(JSON Web Tokens)授权访问的机制（更多方式可以自己添加）保护API

## 后续开发计划

* 编写完善的API文档，利于新人上手
* 增加一个建议的WebAPP客户端来进行API调用的案例
* 为metrics增加一个可视化的浏览方式？
* metrics的数据使用mysql(mongodb)保存？
* 基于Swagger-UI美化API文档？
    
## 如何使用      

下载下来在对应的 `flask_scalarest/resources/your package name/` 创建python包（当然你也可以将整个项目改名）

更多内容敬请期待！！！


## 联系方式

email: eoolife@163.com

QQ: eoolife@163.com