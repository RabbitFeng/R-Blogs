> 本文Typora插入图片选择上传到Github public仓库(私有仓库需要一个`token`，`token`会过期，也有安全风险)

- `Typora`

  - ***偏好设置 - 图像*** 
  - 插入图片时 - 上传图片
  - 上传服务选择`PicGo`

  ![image-20230208172702650](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20230208172702650.png)

- PicGo(图床软件)

  - 使用`GitHub`作为图床仓库（公有仓库）

  ![image-20230208173354609](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20230208173354609.png)



然后在`Typora`中插入本地图片后会自行调起`PicGo`执行图片上传服务。



- `Token`

  `生成token时`需要勾选第一项

  ![image-20230423111007167](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230423111007167.png)

  如果使用`Fine-grained tokens`，需要至少勾选

  - Contents - Read and write
  - Pull requests - Read and write

  ![image-20230423112001178](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230423112001178.png)

  ![image-20230423111930809](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230423111930809.png)

  否则在上传时候会有404问题

  ![image-20230423111043971](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230423111043971.png)

