import json
class Field:
    TYPE_MAPPING = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object"
    }

    def __init__(self, field_type, default_value, description, nullable=False):
        self.field_type = field_type
        self.default_value = default_value
        self.description = description
        self.nullable = nullable

    def to_schema(self):
        schema = {
            "type": [self.get_schema_type()] if not self.nullable else [self.get_schema_type(), "null"],
            "default": self.default_value,
            "description": self.description
        }
        return schema

    def get_schema_type(self):
        if self.field_type in self.TYPE_MAPPING:
            return self.TYPE_MAPPING[self.field_type]
        return "string"
# 案例
# class Params:
#     input = Field(str, '', '输入栅格数据')
#     inputDEM = Field(str, '', '输入DEM数据')
#     output = Field(str, '', '输出数据位置', nullable=True)
#     points = Field(list, ['A', 'B', 'C'], '采样点数')

# 生成 JSON Schema
def generate_schema(Params):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            attr_name: attr.to_schema()
            for attr_name, attr in vars(Params).items()
            if isinstance(attr, Field)
        }
    }
    return schema
# def schema(kls, extras={}):
#     res = classdef_to_schema(kls)
#     res['properties'].update(extras)
#     return res
def executor(context, event, run_hook, Params):
    '''
    微服务调用函数
    @param context:上下文状态
    @param event:请求事件状态
    @param run_hook:执行函数
    @param Params:函数参数
    '''
    try:
        return_dict = {"status":"",
                       "stdout":"",
                       "stderr":"",
                       "returns":""}
        context.logger.info(str(event.path.split("/")))
        service_name = event.path.split("/")[-1]
        if event.method == 'GET':
            # 返回schema
            content = generate_schema(Params)
            return context.Response(body=json.dumps(content),
                                    content_type='text/plain',
                                    status_code=200)
        else:
            # 接收json 参数
            if event.headers.get("Content-Type") == "application/json":
                request_data = event.body
                request_data = dict(request_data)
                # 调用函数
                return_data = run_hook(**request_data)
                return_dict["returns"]= str(return_data)
            else:
                stderr = f"{service_name}：没有传入json格式执行参数"
                context.logger.info(stderr)
                raise Exception(stderr)
    except Exception as e:
        stderr = f"ERROR:{service_name},{e}"
        return_dict["stderr"] =stderr
        return_dict["status"] ="failed"
        context.logger.info(stderr)

        return context.Response(body=json.dumps(return_dict),
                                content_type='text/plain',
                                status_code=400)
    return_dict["status"] = "succeed"
    return context.Response(body=json.dumps(return_dict),
                            content_type='text/plain',
                            status_code=200)
