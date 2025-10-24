FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.2.0 as builder
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 阶段2：生产环境，复制必要的文件
#FROM  ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.2.0
WORKDIR /app
COPY . .

EXPOSE 80

CMD ["python", "app.py"]
