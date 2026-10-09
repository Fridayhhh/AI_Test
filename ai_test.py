import json
import requests
from openai import OpenAI

client = OpenAI(
     api_key="你的API_KEY",
     base_url="https://api.deepseek.com"
)

interfaces=[
       { 
             "path":"/posts",
             "desc":"帖子接口",
              "fields":["id","title","body"]                  
        },
       { 
             "path":"/comments",
             "desc":"评论接口",
              "fields":["id","email","body"]                  
        },
       { 
             "path":"/users",
             "desc":"用户接口",
              "fields":["id","name","email"]                  
        },
]

BASE_URL="https://jsonplaceholder.typicode.com"

def generate_cases(interface):
       prompt=f"""
       你是资深测试工程师。针对接口GET{BASE_URL}{interface['path']}/{{id}}
       (id为1-100的整数)，生成3条测试用例，覆盖正常、异常、边界。
        严格要求：只返回JSON数组，不要任何解释文字。
        每个用例包括三个字段：
        -case_name: 字符串，用例名称
        -request_id: 整数，请求的id
        -expected_status: 整数，预期HTTP状态码
        """

       resp=client.chat.completions.create(
             model="deepseek-chat",
             messages=[{"role":"user","content":prompt}]
       )
       return json.loads(resp.choices[0].message.content)

def check_fields(response_json,required_fields):
       missing=[]
       for field in required_fields:
              if field not in response_json:
                    missing.append(field)
       return missing

def test_interface(interface):
       print(f"\n{'='*50}")
       print(f"开始测试：{interface['desc']}({interface['path']})")
       print(f"\n{'='*50}")
       cases=generate_cases(interface)
       print(f"AI生成了{len(cases)}条用例")
       passed,failed=0,0
       for case in cases:
            url = f"{BASE_URL}{interface['path']}/{case['request_id']}"
            resp = requests.get(url)
            actual_status = resp.status_code
            expected_status = case["expected_status"]
            status_ok = (actual_status == expected_status)
            missing_fields = []
            if status_ok and actual_status == 200:
                try:
                    body = resp.json()
                    if isinstance(body, list) and len(body) > 0:
                        body = body[0]
                    missing_fields = check_fields(body, interface["fields"])
                except Exception as e:
                    missing_fields = [f"解析失败: {e}"]
            if status_ok and not missing_fields:
                print(f"  [通过] {case['case_name']} (状态码{actual_status})")
                passed += 1
            else:
                reason = []
                if not status_ok:
                    reason.append(f"状态码预期{expected_status}实际{actual_status}")
                if missing_fields:
                    reason.append(f"缺失字段{missing_fields}")
                print(f"  [失败] {case['case_name']} ({'；'.join(reason)})")
                failed += 1

       return passed, failed

total_passed, total_failed = 0, 0

for interface in interfaces:
    p, f = test_interface(interface)
    total_passed += p
    total_failed += f

print(f"\n{'='*50}")
print("最终测试报告")
print(f"{'='*50}")
print(f"通过：{total_passed} 条")
print(f"失败：{total_failed} 条")
print(f"总计：{total_passed + total_failed} 条")
