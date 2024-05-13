from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('input_data.html')

@app.route('/submit_form', methods=['POST'])
def handle_form():
    id_number = request.form.get('id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    email = request.form.get('email')

    # Step 1: 確認身份證號碼長度是否為10。
    if len(id_number)!=10:
        return "身分證號碼應該為10碼", 400

    # Step 2: 確認第一個字元是否為英文字母。
    if not id_number[0].isalpha():
        return "第一個字元應為英文字母", 400
        
    # Step 3: 確認後九個字元是否為數字。
    rest_chars = id_number[1:]
    if not rest_chars.isdigit():
        return "後九個字元應為數字", 400
    
    # Step 4: 將第一個英文字母轉換為對應的數字（A為10，B為11，C為12，...，Z為33）。
    first_char_num = ord(id_number[0].upper()) - 55
    
    # Step 5: 將轉換後的兩位數字分別乘以1和9。
    sum_product = first_char_num * 1 + first_char_num * 9
    
    # Step 6: 將第二個到第九個數字分別乘以8, 7, 6, 5, 4, 3, 2, 1。
    weights = [8, 7, 6, 5, 4, 3, 2, 1]
    for i in range(8):
        sum_product += int(rest_chars[i]) * weights[i]
    
    # Step 7: 將以上所有乘積相加，並加上最後一個數字。
    sum_product += int(rest_chars[-1])
    
    # Step 8: 如果最後的結果可以被10整除，則這個身份證號碼就是正確的
    if sum_product % 10 == 0:
        return True
    else:
        return False

    # Test the function
    id_number = input("請輸入身份證號碼：")
    if validate_id_number(id_number):
        print("這個身份證號碼是正確的。")
    else:
        print("這個身份證號碼是不正確的。")

    # Validate name (assuming it's alphabetic)
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Invalid name", 400

    # Validate gender
    if gender not in ['Male', 'Female']:
        return "Invalid gender", 400

    # Validate email
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Invalid email", 400

    return "All entries are valid", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Listen on all available network interfaces and port 80

