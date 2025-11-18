import requests

BASE_URL = "https://jsonplaceholder.typicode.com/todos"

def get_post(post_id):
    response = requests.get(f"{BASE_URL}/{post_id}")

    print("===== HTTP Response 분석 =====")
    print("1) Status Code:", response.status_code)
    print("2) Headers:", response.headers)
    print("3) Body(text):", response.text)
    print("4) Body(json):", response.json())
    print("==============================")
    return response.json()


def create_todo():
    data = {
        "title": "New Todo created by Python",
        "completed": False,
        "userId": 1
    }

    response = requests.post(BASE_URL, json=data)

    print("\n===== POST Response 분석 =====")
    print("Status Code:", response.status_code)       # 보통 201 Created
    print("Headers:", response.headers)
    print("Body (json):", response.json())
    print("================================")

    return response.json()


def update_todo(todo_id):
    data = {
        "id": todo_id,
        "title": "Updated Todo",
        "completed": True,
        "userId": 1
    }

    response = requests.put(f"{BASE_URL}/{todo_id}", json=data)

    print("\n===== PUT Response 분석 =====")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body (json):", response.json())
    print("================================")

    return response.json()


def delete_todo(todo_id):
    response = requests.delete(f"{BASE_URL}/{todo_id}")

    print("\n===== DELETE Response 분석 =====")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)   # 빈 문자열이거나 {}
    print("================================")

    return response.json()


if __name__ == '__main__':
    response = get_post(1)
    print(response['title'])

    delete_todo(1)