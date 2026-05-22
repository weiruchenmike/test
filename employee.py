import pandas as pd
df=pd.read_excel("interview_employee_data.xlsx")
# 印出前四筆資料
print(df.head(4))
# 算資料筆數
print(len(df))


import requests
API_URL = "http://localhost:8000/api/employees"

success_rows = []
failed_rows = []

for row in df.itertuples(index=False):
    payload = {
        "employee_id": None if pd.isna(row.employee_id) else str(row.employee_id).strip(),
        "name": None if pd.isna(row.name) else str(row.name).strip(),
        "email": None if pd.isna(row.email) else str(row.email).strip(),
        "department": None if pd.isna(row.department) else str(row.department).strip(),
        "salary": None if pd.isna(row.salary) else row.salary,
        "join_date": None if pd.isna(row.join_date) else str(row.join_date).strip(),
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 201:
            print("成功:", payload["employee_id"], response.status_code)
            success_rows.append({
                "employee_id": payload["employee_id"],
                "status_code": response.status_code,
                "response": response.json()
            })
        else:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = response.text

            print("失敗:", payload["employee_id"], response.status_code)
            print("錯誤原因:", error_detail)

            failed_rows.append({
                "employee_id": payload["employee_id"],
                "status_code": response.status_code,
                "error": error_detail,
                "payload": payload
            })

    except requests.RequestException as e:
        print("連線失敗:", payload["employee_id"])
        print("錯誤原因:", str(e))

        failed_rows.append({
            "employee_id": payload["employee_id"],
            "status_code": None,
            "error": str(e),
            "payload": payload
        })

print("匯入完成")
print(success_rows)
print("="*50)
print(failed_rows)