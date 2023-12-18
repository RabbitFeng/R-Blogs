## GitHub 网站访问不了

### 1. 修改hosts文件

- 查询IP

  - [站长工具](https://tool.chinaz.com/dns/github.com) 查询IP地址，如`20.205.243.166`

- `Host`文件追加配置

  - `C:\Windows\System32\drivers\etc\hosts`文件中添加:

    ```
    20.205.243.166 github.com
    ```

    ![image-20231111143420265](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20231111143420265.png)

- 刷新缓存

  `ipconfig/flushdns`

  ![image-20231111144034519](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20231111144034519.png)

## GitHub网站可以访问但是push失败(V2Ray)

- 设置Git代理

  `git config --global http.proxy ***`

  ![image-20231111144122711](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20231111144122711.png)